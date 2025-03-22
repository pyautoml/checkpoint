import json
from pathlib import Path
from typing import Iterable
from collections import deque
from datetime import datetime
from .abstract_path_model import AbstractPathModel


class FileModel:
    @staticmethod
    def __generate_file_name(file_name: str = "checkpoint.json"):
        return f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"

    @staticmethod
    def __prepare_data_to_dump(data: deque[dict], groupby_key: str = None) -> dict:
        final_data: dict = {}
        if not groupby_key:
            groupby_key: str = "checkpoints"
        
        while data:
            item = data.popleft()
            key = item.get(groupby_key, groupby_key)
            final_data.setdefault(key, []).append(item)
        return final_data

    @classmethod
    def _save_as_json(
            cls, 
            groupby_key: str,
            data: Iterable, 
            path_model: AbstractPathModel,
            file: Path | str = None, 
            indent: int = 4, 
            autocreate_path: bool = False
        ) -> None:

        file: Path = path_model.verify_path(file, autocreate_path) if file else Path.cwd() / cls.__generate_file_name()
        with open(file, "w", encoding="UTF-8") as f:
            json.dump(cls.__prepare_data_to_dump(data=data, groupby_key=groupby_key), f, indent=indent)
