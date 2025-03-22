from pathlib import Path

class PathModel:
    @staticmethod
    def __create_path(path: str | Path) -> Path:
        path = Path(path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path
    
    @classmethod
    def __add_json_suffix(cls, path_to_file: str | Path) -> Path:
        if not str(path_to_file).endswith(".json"):
            path_to_file: str = f"{path_to_file}.json"
        return Path(path_to_file)

    @classmethod
    def verify_path(cls, path_to_file: Path | str, autocreate_path: bool) -> Path:
        path_to_file: Path = cls.__add_json_suffix(path_to_file)

        if not path_to_file.parent.exists():
            if autocreate_path:
                cls.__create_path(path_to_file.parent)
            else:
                raise FileNotFoundError(f"Path {path_to_file.parent} does not exist.")
        return path_to_file
