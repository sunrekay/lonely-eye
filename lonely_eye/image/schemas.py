from enum import Enum


class Photo(str, Enum):
    jpg: str = "jpg"
    jpeg: str = "jpeg"
    png: str = "png"

    @staticmethod
    def formats() -> list[str]:
        return list(map(lambda x: x.value, list(Photo)))
