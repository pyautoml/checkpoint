import json
from pathlib import Path
from collections import deque
from datetime import datetime
from unittest.mock import patch
from ..models.file_model import FileModel
from ..models.path_model import PathModel


def test_generate_file_name():
    file_name = "checkpoint.json"
    generated_name = FileModel._FileModel__generate_file_name(file_name)
    assert generated_name.endswith(f"_{file_name}")
    assert datetime.strptime(generated_name.split('_')[0], '%Y%m%d%H%M%S')

def test_prepare_data_to_dump():
    data = deque([
        {"id": "func_1", "value": "a"},
        {"id": "func_2", "value": "b"},
        {"id": "func_1", "value": "c"}
    ])
    expected_output = {
        "func_1": [{"id": "func_1", "value": "a"}, {"id": "func_1", "value": "c"}],
        "func_2": [{"id": "func_2", "value": "b"}]
    }
    result = FileModel._FileModel__prepare_data_to_dump(data, groupby_key="id")
    assert result == expected_output

def test_prepare_data_to_dump_no_groupby_key():
    data = deque([
        {"value": "a"},
        {"value": "b"},
        {"value": "c"}
    ])
    expected_output = {
        "checkpoints": [{"value": "a"}, {"value": "b"}, {"value": "c"}]
    }
    result = FileModel._FileModel__prepare_data_to_dump(data)
    assert result == expected_output

@patch("checkpoint_auto.models.path_model.PathModel.verify_path")
def test_save_as_json(mock_verify_path, tmp_path):
    mock_verify_path.return_value = tmp_path / "testfile.json"
    data = deque([
        {"id": 1, "value": "a"},
        {"id": 2, "value": "b"},
        {"id": 1, "value": "c"}
    ])
    FileModel._save_as_json(
        groupby_key="id",
        data=data,
        path_model=PathModel,
        file=mock_verify_path.return_value,
        indent=2,
        autocreate_path=True
    )
    with open(mock_verify_path.return_value, "r", encoding="UTF-8") as f:
        saved_data = json.load(f)
    expected_output = {
        "1": [{"id": 1, "value": "a"}, {"id": 1, "value": "c"}],
        "2": [{"id": 2, "value": "b"}]
    }
    assert saved_data == expected_output
