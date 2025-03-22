from pathlib import Path
from functools import wraps
from collections import deque
from datetime import datetime
from typing import List, Callable
from .file_model import FileModel
from .path_model import PathModel


class Checkpoint:
    _instances: dict = {}
    _history: deque[dict] = deque()
    _call_stack: deque[dict] = deque()
    _file_model: FileModel = FileModel()
    _path_model: PathModel = PathModel()

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            instance = super().__call__(*args, **kwargs)
            self._instances[self] = instance
        return self._instances[self]

    @classmethod
    def __is_occupied(cls, index: int) -> bool:
        return index < len(cls._call_stack) and cls._call_stack[index] is not None

    @classmethod
    def _insert(cls, index, value):
        if cls.__is_occupied(index):
            raise IndexError(f"Index already occupied. Details: index: {index} value: {value}")
        while len(cls._call_stack) <= index:
            cls._call_stack.append(None)
        cls._call_stack[index] = value

    @classmethod
    def save_track(cls, groupby_key:str = None, file: str | Path = None, autocreate_path: bool = False) -> None:
        cls._file_model._save_as_json(
            groupby_key=groupby_key, 
            path_model=cls._path_model, 
            data=cls._history, 
            file=file, 
            autocreate_path=autocreate_path
        )


def checkpoint(positions: List[int]) -> Callable:
    positions = sorted(positions)

    def decorator(func: Callable) -> Callable:
        for position in positions:
            Checkpoint._insert(position - 1, {"call_no": position, "name": func.__name__, "index": position - 1})
            Checkpoint._history.append(
                {
                    "operation": "append", 
                    "timestamp": str(datetime.now()), 
                    "name": func.__name__, 
                    "call_no": position,
                }
            )

        @wraps(func)
        def wrapper(*args, **kwargs):
            removal_candidate = Checkpoint._call_stack.popleft()
            if removal_candidate:
                if removal_candidate["name"] == func.__name__:
                    Checkpoint._history.append(
                        {
                            "operation": "remove", 
                            "timestamp": str(datetime.now()), 
                            "name": removal_candidate["name"], 
                            "call_no": removal_candidate["call_no"], 
                        }
                    )
                else:
                    error_message: str = f"Expected calling function: {func.__name__}, but called: {removal_candidate['name']}"
                    Checkpoint._history.append(
                        {
                            "operation": "error", 
                            "timestamp": str(datetime.now()), 
                            "name": removal_candidate["name"], 
                            "call_no": removal_candidate["call_no"], 
                        }
                    )
                    raise IndexError(error_message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
