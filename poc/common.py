import hashlib
import json
import re
from datetime import datetime, timezone


class Rejected(ValueError):
    """Safe, fixed diagnostic suitable for CI output."""


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def binding(envelope):
    return digest(canonical(envelope).encode())


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", value):
        raise Rejected("invalid identifier")
    return value


def oracle_identifier(value):
    # Deliberately bounded; preserves case for double-quoted Oracle identifiers.
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_$#]{0,127}", value):
        raise Rejected("unsupported Oracle identifier")
    return value


def require_actor(policy, role, actor):
    identifier(actor)
    if actor not in policy.get(role, []):
        raise Rejected("actor is not authorized for this action")


def expectations(value):
    if not isinstance(value, dict) or set(value) != {"objects", "effects", "invocations"}:
        raise Rejected("invalid verification contract")
    if not value["objects"]:
        raise Rejected("at least one expected object is required")
    supported = {"FUNCTION", "PROCEDURE", "PACKAGE", "PACKAGE BODY", "TRIGGER", "TABLE", "VIEW", "SEQUENCE"}
    for obj in value["objects"]:
        if set(obj) != {"name", "type"} or obj["type"] not in supported:
            raise Rejected("unsupported expected object")
        oracle_identifier(obj["name"])
    for effect in value["effects"]:
        if set(effect) != {"table", "key_column", "key", "expected_count"}:
            raise Rejected("unsupported data-effect assertion")
        oracle_identifier(effect["table"])
        oracle_identifier(effect["key_column"])
        if type(effect["key"]) is not int or type(effect["expected_count"]) is not int:
            raise Rejected("effect assertions require integer keys/counts")
    for call in value["invocations"]:
        if set(call) != {"function", "clob_input", "expected_number"}:
            raise Rejected("unsupported function invocation")
        oracle_identifier(call["function"])
        if not isinstance(call["clob_input"], str) or len(call["clob_input"]) > 4000:
            raise Rejected("invalid deterministic CLOB input")
        if type(call["expected_number"]) is not int:
            raise Rejected("invocation requires an integer result")
        if {"name": call["function"], "type": "FUNCTION"} not in value["objects"]:
            raise Rejected("invoked function must be an expected object")
    return value
