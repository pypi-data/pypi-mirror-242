from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import get_args, get_origin

from llama_prompter.types import Concat


class BNF(ABC):
    BASE_TYPES: dict[type, tuple[str, str]]

    @classmethod
    def type_name(cls, type_: type) -> str:
        if type_ in cls.BASE_TYPES:
            return cls.BASE_TYPES[type_][0]
        origin = get_origin(type_)
        if origin:
            return f"{origin.__name__.lower()}" + "".join([cls.type_name(a).title() for a in get_args(type_)])
        return type_.__name__.lower()

    @classmethod
    @abstractmethod
    def definition(cls, type_: type) -> str:
        pass

    @staticmethod
    @abstractmethod
    def rule(name: str, definition: str) -> str:
        pass


class EBNF(BNF):
    BASE_TYPES = {
        bool: ("boolean", r'"true" / "false"'),
        float: ("float", r"~'-?[0-9]*(.[0-9]*)?'"),
        int: ("integer", r"~'-?[0-9]+'"),
        str: ("string", r"~'\"[0-9 a-z]*\"'i"),
    }

    @classmethod
    def definition(cls, type_: type) -> str:
        if type_ in cls.BASE_TYPES:
            return cls.BASE_TYPES[type_][1]
        elif get_origin(type_) == Concat:
            return ' " " '.join([cls.type_name(a) for a in get_args(get_args(type_)[0])])
        elif get_origin(type_) == list:
            arg = cls.type_name(get_args(type_)[0])
            return f'"[" ({arg} ("," {arg})*)? "]"'
        elif get_origin(type_) == tuple:
            return '"[" ' + ' "," '.join([cls.type_name(a) for a in get_args(type_)]) + ' "]"'
        elif get_origin(type_) == dict:
            k_type, v_type = get_args(type_)
            kv = f'{cls.type_name(k_type)} ":" {cls.type_name(v_type)}'
            return f'"{{" ({kv} ("," {kv})*)? "}}"'
        elif issubclass(type_, BaseModel):
            return '"{" ' + ' "," '.join([f'"\\"{n}\\":" {cls.type_name(f.annotation)}' for n, f in type_.model_fields.items() if f.annotation]) + ' "}"'
        assert False, f"Unable to return bnf definition for type {type_.__name__}"

    @staticmethod
    def rule(name: str, definition: str) -> str:
        return f"{name} = {definition}"


class GBNF(BNF):
    BASE_TYPES = {
        bool: ("boolean", '("true" | "false")'),
        float: ("float", '("-"? ([0-9]*) ("." [0-9]+))'),
        int: ("integer", '("-"? ([0-9]+))'),
        str: ("string", '"\\"" ([^"\\\\] | "\\\\" (["\\\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]))* "\\""'),
    }

    @classmethod
    def definition(cls, type_: type) -> str:
        if type_ in cls.BASE_TYPES:
            return cls.BASE_TYPES[type_][1]
        else:
            return EBNF.definition(type_)

    @staticmethod
    def rule(name: str, definition: str) -> str:
        return f"{name} ::= {definition}"
