import json
from pathlib import Path

from flask import Flask, abort

DATASET_DIR = Path("data-files")
EMPLOYEE_DATASET_DIR = DATASET_DIR / Path("employee-list-files")
LEVELS_DIR = DATASET_DIR / Path("levels-files")

app = Flask(__name__)

app.json.ensure_ascii = False
app.url_map.strict_slashes = False

ReturnDict = dict[str, str | float | None]


@app.route("/")
def index() -> list[str]:
    return [rule.rule for rule in app.url_map.iter_rules()]


@app.route("/employees")
def employee_datasets() -> list[ReturnDict]:
    return _list_file_based_endpoint(EMPLOYEE_DATASET_DIR)


@app.route("/employees/<int:dataset_id>")
def employee_datasets_single(dataset_id: int) -> ReturnDict:
    return _serve_file(EMPLOYEE_DATASET_DIR / f"{dataset_id}.json")


@app.route("/levels")
def levels() -> list[ReturnDict]:
    return _list_file_based_endpoint(LEVELS_DIR)


@app.route("/levels/<int:level_id>")
def levels_single(level_id: int) -> ReturnDict:
    return _serve_file(LEVELS_DIR / f"{level_id}.json")


def _list_file_based_endpoint(path: Path) -> list[ReturnDict]:
    return list([{"id": int(f.stem)} for f in path.iterdir()])


def _serve_file(file: Path) -> ReturnDict:
    if not file.is_file():
        abort(404)
    with open(
            file, "r", encoding="UTF-8"
    ) as datafile:
        return json.load(datafile)
