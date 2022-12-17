from abc import ABC, abstractmethod
from typing import Dict, Union, Set, TypeVar
import json
from aioxmpp import JID
from spade.message import Message as SpadeMessage
from pydantic import BaseModel

import consts

T = TypeVar("T")


class Typable(ABC):
    @classmethod
    def all_subclasses(cls: T) -> Set[T]:
        subclasses = set(cls.__subclasses__())
        subsubclasses = set()
        for subclass in subclasses:
            subsubclasses |= subclass.all_subclasses()
        return subclasses | subsubclasses

    @classmethod
    def for_type(cls: T, type: str) -> T:
        subclass_mapping = {
            subclass.type(): subclass for subclass in cls.all_subclasses()
        }
        return subclass_mapping[type]


class BaseMessage(Typable, BaseModel):
    @classmethod
    def parse(cls, message: SpadeMessage):
        subclass = cls.for_type(message.metadata["type"])
        params = json.loads(message.body)
        return subclass.__call__(**params)

    @classmethod
    @abstractmethod
    def get_performative(cls) -> str:
        pass

    @classmethod
    def get_metadata(cls) -> Dict[str, str]:
        return {
            "ontology": consts.ONTOLOGY,
            "language": consts.LANGUAGE,
            "performative": cls.get_performative(),
            "type": cls.type()
        }

    @classmethod
    def type(cls) -> str:
        return cls.__name__

    def to_spade(self, to: Union[str, JID], sender: Union[str, JID]) -> SpadeMessage:
        return SpadeMessage(
            to=to,
            sender=str(sender),
            metadata=self.get_metadata(),
            body=self.json()
        )
