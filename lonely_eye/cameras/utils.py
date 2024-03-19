import leb128
from pydantic import ValidationError

from lonely_eye.cameras.types import (
    CameraUnified,
    Camera1,
    Camera2,
    Camera3,
    cameras_types,
)
from lonely_eye.cameras import exceptions


def deserialize(line: bytes) -> dict:
    ans: dict = {}
    while len(line) > 1:
        len_k = line[1]
        len_v = line[3]
        k = str(line[5 : 5 + len_k]).replace("'", "")[1:]
        v = line[5 + len_k : 5 + len_k + len_v]
        if line[4] == 2:
            v = deserialize(v)
        elif line[4] == 1:
            v = leb128.i.decode(v)
        else:
            v = str(v).replace("'", "")[1:]
        ans[k] = v
        line = line[5 + len_k + len_v :]
    return ans


def get_camera_schemas(data: dict) -> Camera1 | Camera2 | Camera3 | None:
    for camt in cameras_types:
        try:
            camera_schema = camt.parse_obj(data)
            return camera_schema
        except ValidationError:
            pass

    raise exceptions.wrong_bytes_line


def unify_camera_schema(camera) -> CameraUnified:
    match camera.type:
        case 1:
            camera_unified: CameraUnified = CameraUnified(
                **{
                    "transport_number": camera.transport_chars[0]
                    + camera.transport_numbers
                    + camera.transport_chars[1:]
                    + camera.transport_region,
                    "camera_id": camera.camera_id,
                    "violation_id": camera.violation_id,
                    "violation_value": camera.violation_value,
                    "skill_value": camera.skill_value,
                    "datetime": camera.datetime,
                }
            )
            return camera_unified

        case 2:
            camera_unified: CameraUnified = CameraUnified(
                **{
                    "transport_number": camera.transport.get("chars")[0]
                    + camera.transport.get("numbers")
                    + camera.transport.get("chars")[1:]
                    + camera.transport.get("region"),
                    "camera_id": camera.camera.get("id"),
                    "violation_id": camera.violation.get("id"),
                    "violation_value": camera.violation.get("value"),
                    "skill_value": camera.skill.get("value"),
                    "datetime": "{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}{}".format(
                        camera.datetime.get("year"),
                        camera.datetime.get("month"),
                        camera.datetime.get("day"),
                        camera.datetime.get("hour"),
                        camera.datetime.get("minute"),
                        camera.datetime.get("seconds"),
                        camera.datetime.get("utc_offset"),
                    ),
                }
            )
            return camera_unified

        case 3:
            camera_unified: CameraUnified = CameraUnified(
                **{
                    "transport_number": camera.transport,
                    "camera_id": camera.camera.get("id"),
                    "violation_id": camera.violation.get("id"),
                    "violation_value": camera.violation.get("value"),
                    "skill_value": camera.skill,
                    "datetime": camera.datetime,
                }
            )
            return camera_unified
