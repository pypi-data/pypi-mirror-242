import json
import re

from pydantic import BaseModel
from typing import Any, Callable, Optional, TypeVar, Union, get_args, get_origin

from llama_prompter.bnf import BNF, EBNF
from llama_prompter.types import Concat


def parse_type(bnf: type[BNF], rules: dict[str, str], type_: type) -> str:
    type_name = bnf.type_name(type_)
    if type_name in rules:
        return type_name
    rules[type_name] = bnf.definition(type_)
    if get_origin(type_) == Concat:
        for x in get_args(get_args(type_)[0]):
            parse_type(bnf, rules, x)
    elif get_origin(type_) in [dict, list, tuple]:
        for x in get_args(type_):
            parse_type(bnf, rules, x)
    elif issubclass(type_, BaseModel):
        for _, f in type_.model_fields.items():
            if f.annotation:
                parse_type(bnf, rules, f.annotation)
    return type_name


def type_to_grammar(type_: type, bnf: type[BNF] = EBNF) -> str:
    rules: dict[str, str] = {}
    rules["root"] = parse_type(bnf, rules, type_)
    return "\n".join([bnf.rule(n, r) for n, r in rules.items()])


BASE_TYPES_RE: dict[type, tuple[re.Pattern[str], Callable[[str], Any]]] = {
    bool: (re.compile(r"(true|false)"), lambda x: x == "true"),
    float: (re.compile(r"(\-?[0-9]*\.[0-9]+)"), float),
    int: (re.compile(r"(\-?[0-9]+)"), int),
    str: (re.compile(r'"((?:\\.|[^"\\])*)"'), str),
}

LIST_TYPE_RE = re.compile(r"\[\]")

T = TypeVar("T")


def decode_type(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
    if type_ in BASE_TYPES_RE:
        regex, cast_func = BASE_TYPES_RE[type_]
        m = regex.match(payload)
        if not m:
            return None, 0
        return cast_func(m.group(1)), len(m.group(0))
    elif get_origin(type_) == Concat:
        # queue.extend(get_args(get_args(type_)[0]))
        pass
    elif get_origin(type_) == list:
        start = 1  # skip first "["
        result = []
        arg_type = get_args(type_)[0]
        while payload[start - 1] != "]":
            if start >= len(payload):
                return None, 0
            arg, i = decode_type(payload[start:], arg_type)
            if arg is None:
                return None, 0
            result.append(arg)
            start += i + 1  # skip comma ","
        return list(result), start  # type: ignore
    elif get_origin(type_) == tuple:
        start = 1  # skip first "["
        result = []
        for arg_type in get_args(type_):
            if start >= len(payload):
                return None, 0
            arg, i = decode_type(payload[start:], arg_type)
            if arg is None:
                return None, 0
            result.append(arg)
            start += i + 1  # skip comma ","
        return tuple(result), start  # type: ignore
    elif issubclass(type_, BaseModel):
        d, i = json.JSONDecoder().raw_decode(payload)
        return type_(**d), i  # type: ignore
    return None, 0


def deserialize(payload: str, type_: type[T]) -> T:
    obj, i = decode_type(payload, type_)
    if obj is None:
        raise Exception("Could not decode payload")
    return obj
