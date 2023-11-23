import json
from typing import Any
from tbcml import core


class JsonFile:
    def __init__(self, data: "core.Data"):
        self.json = json.loads(data.data)

    @staticmethod
    def from_path(path: "core.Path") -> "JsonFile":
        return JsonFile(path.read())

    @staticmethod
    def from_object(js: Any) -> "JsonFile":
        return JsonFile(core.Data(json.dumps(js)))

    @staticmethod
    def from_data(data: "core.Data") -> "JsonFile":
        return JsonFile(data)

    def to_data(self) -> "core.Data":
        return core.Data(json.dumps(self.json, indent=4))

    def to_data_request(self) -> "core.Data":
        return core.Data(json.dumps(self.json)).replace(core.Data(" "), core.Data(""))

    def save(self, path: "core.Path") -> None:
        path.write(self.to_data())

    def get_json(self) -> Any:
        return self.json

    def get(self, key: str) -> Any:
        return self.json[key]

    def set(self, key: str, value: Any) -> None:
        self.json[key] = value

    def __str__(self) -> str:
        return str(self.json)

    def __getitem__(self, key: str) -> Any:
        return self.json[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.json[key] = value
