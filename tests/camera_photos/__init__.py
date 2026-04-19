import leb128

d1: dict = {
    "transport_chars": "ABC",
    "transport_numbers": "254",
    "transport_region": "797",
    "camera_id": "afa54296-2b2e-4101-8dbb-352a7b48d6fd",
    "violation_id": "1009cdcc-196b-45b1-baec-5e330cd213af",
    "violation_value": "13km/h",
    "skill_value": 1,
    "datetime": "2024-01-01T00:00:00+00:00",
}


d2: dict = {
    "transport": {
        "chars": "ABC",
        "numbers": "254",
        "region": "797",
    },
    "camera": {
        "id": "afa54296-2b2e-4101-8dbb-352a7b48d6fd",
    },
    "violation": {
        "id": "1009cdcc-196b-45b1-baec-5e330cd213af",
        "value": "13km/h",
    },
    "skill": {
        "value": 1,
    },
    "datetime": {
        "year": 2024,
        "month": 1,
        "day": 1,
        "hour": 0,
        "minute": 0,
        "seconds": 0,
        "utc_offset": "+00:00",
    },
}


d3: dict = {
    "transport": "A254BC797",
    "camera": {
        "id": "afa54296-2b2e-4101-8dbb-352a7b48d6fd",
    },
    "violation": {
        "id": "1009cdcc-196b-45b1-baec-5e330cd213af",
        "value": "13km/h",
    },
    "skill": 1,
    "datetime": 1704067200,
}


test_camera_types: list = [d1, d2, d3]


def _serialize_value(value) -> tuple[bytes, int]:
    """Возвращает (encoded_bytes, type_code).
    type_code: 0=string, 1=int(leb128), 2=nested dict
    """
    if isinstance(value, dict):
        inner = b""
        for k, v in value.items():
            inner += _serialize_entry(k, v)
        return inner, 2
    elif isinstance(value, int):
        return leb128.i.encode(value), 1
    else:
        return str(value).encode("utf-8"), 0


def _serialize_entry(key: str, value) -> bytes:
    key_bytes = key.encode("utf-8")
    val_bytes, val_type = _serialize_value(value)
    # формат: [0][len_k][0][len_v][val_type][key...][val...]
    return bytes([0, len(key_bytes), 0, len(val_bytes), val_type]) + key_bytes + val_bytes


def serialize(data: dict) -> bytes:
    """Сериализует dict в бинарный формат с 2 байтами заголовка."""
    result = b"\x00\x00"
    for k, v in data.items():
        result += _serialize_entry(k, v)
    return result
