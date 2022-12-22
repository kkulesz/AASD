from utils.cords import Cords
from utils.logger import Logger
from utils.route import Route, Target

from aioxmpp import JID
from typing import Dict, Optional, Set

import numpy as np


class BinModel:
    def __init__(self, cords: Cords, max_volume: float, curr_fill_percentage: float):
        self.cords = cords
        self.max_volume = max_volume
        self.curr_fill_percentage = curr_fill_percentage


class TruckModel:
    def __init__(self, cords: Cords, free_space: float, remaining_distance: float):
        self.cords = cords
        self.free_space = free_space
        self.remaining_distance = remaining_distance


class SupervisorLogic:
    def __init__(self,
                 logger: Logger,
                 ):
        self.logger = logger
        self.bins: Dict[JID, BinModel] = dict()
        self.trucks: Dict[JID, TruckModel] = dict()
        self.pending_routes: Dict[JID, Route] = dict()
        self.current_routes: Dict[JID, Route] = dict()
        self.bins_in_current_routes: Set[JID] = set()
        self.awaiting_response = None
        self.awaiting_first_status = set()

    def register_bin_state(self, jid: JID, cords: Cords, max_volume: float, curr_fill_percentage: float):
        prev_state = self.bins.pop(jid, None)
        if prev_state and prev_state.curr_fill_percentage > curr_fill_percentage and jid in self.bins_in_current_routes:
            self.bins_in_current_routes.remove(jid)
        self.bins[jid] = BinModel(cords, max_volume, curr_fill_percentage)

    def register_truck_state(self, jid: JID, cords: Cords, free_space: float, remaining_distance: float):
        if jid in self.awaiting_first_status:
            self.awaiting_first_status.remove(jid)
        self.trucks[jid] = TruckModel(cords, free_space, remaining_distance)

    def pop_route(self, jid: JID = None):
        if jid:
            route = self.pending_routes.pop(jid)
        else:
            jid, route = self.pending_routes.popitem()
        self.current_routes[jid] = route
        return jid, route

    def peek_route(self):
        jid, route = self.pending_routes.popitem()
        self.pending_routes[jid] = route
        return jid, route

    def process_decline(self):
        pass

    def got_response(self, jid):
        return self.awaiting_response != jid

    def await_response(self, jid):
        self.awaiting_response = jid
        self.awaiting_first_status.add(jid)

    def plan(self):
        target_bins = self._list_target_bins()
        trucks = self._list_available_trucks()
        if not trucks:
            return
        assignments = self._assign_trucks(trucks, target_bins)
        for truck_id in assignments:
            truck_jid = trucks[truck_id][0]
            targets = []
            for bin_id in assignments[truck_id]:
                bin_jid, bin_info = target_bins[bin_id]
                target = Target(jid=bin_jid,
                                est_rubbish_volume=bin_info.max_volume * bin_info.curr_fill_percentage,
                                cords=bin_info.cords)
                targets.append(target)
                self.bins_in_current_routes.add(bin_jid)
            route = Route(targets)
            self.pending_routes[truck_jid] = route

    def _assign_trucks(self, trucks, target_bins):
        adjacency_matrix = self._prepare_adjacency_matrix(target_bins, trucks)
        assignments = dict()
        for bin_id, truck_list in enumerate(np.argsort(adjacency_matrix)):
            for truck_arg in truck_list:
                truck_info = trucks[truck_arg][1]
                if truck_info.free_space > (
                        target_bins[bin_id][1].max_volume * target_bins[bin_id][1].curr_fill_percentage):
                    truck_info.free_space -= target_bins[bin_id][1].max_volume * target_bins[bin_id][
                        1].curr_fill_percentage
                    trucks[truck_arg][1] = truck_info
                    if truck_arg in assignments:
                        assignments[truck_arg].append(bin_id)
                    else:
                        assignments[truck_arg] = [bin_id]
                    break
        return assignments

    def _prepare_adjacency_matrix(self, bins, trucks):
        adjacency_matrix = np.zeros((len(bins), len(trucks)))
        for bin_id, bin in enumerate(bins):
            for truck_id, truck in enumerate(trucks):
                adjacency_matrix[bin_id, truck_id] = bin[1].cords.dist(truck[2])
        return adjacency_matrix

    def _list_available_trucks(self):
        trucks = []
        for truck_jid, truck in self.trucks.items():
            if truck_jid in self.awaiting_first_status:
                continue
            truck_final_position = truck.cords
            if truck_jid in self.current_routes:
                truck_final_position = self.current_routes[truck_jid].last_target().cords
            trucks.append([truck_jid, truck, truck_final_position])
        return trucks

    def _list_target_bins(self):
        target_bins = []
        for bin_jid, bin in self.bins.items():
            if bin_jid not in self.bins_in_current_routes:
                if bin.curr_fill_percentage >= 0.8:
                    target_bins.append((bin_jid, bin))
        return target_bins
