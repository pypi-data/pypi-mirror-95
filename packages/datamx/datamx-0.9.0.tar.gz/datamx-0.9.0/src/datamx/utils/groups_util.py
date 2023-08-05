import json
from datetime import datetime
from pathlib import Path

from datamx.cache.file_process_cache import FileProcessCache
from datamx.models.values import Groups, GroupsSchema


def read_json_dict_from_file(path):
    with open(path, mode='r', newline=None) as json_file:
        json_inst = json.load(json_file)
    return json_inst


def load_groups(input_file: Path) -> Groups:
    json_dict = read_json_dict_from_file(input_file)
    return GroupsSchema().load(json_dict)


def add_groups_to_cache(groups: Groups, cache_dir: Path, completed_dir: Path):
    write_groups_with_dated_filename(groups, cache_dir)
    cache = FileProcessCache(cache_dir, completed_dir)
    cache.load_cache()
    return cache


def write_groups_with_dated_filename(groups: Groups, output_dir: Path):
    name = create_dated_filename(read=groups.datetime)
    models_str = GroupsSchema().dumps(groups, sort_keys=True, indent=3)
    output_file = Path(output_dir, name)
    with open(output_file, 'w') as output:
        output.write(models_str)
    return output_file


def create_dated_filename(prefix: str = "reading", read: datetime = None):
    reading_time = read if read is not None else datetime.now()
    epoch_seconds = int(reading_time.timestamp())
    date_str = reading_time.strftime("%Y-%m-%d_%H-%M-%S")
    return prefix + "_" + str(epoch_seconds) + "_" + date_str + ".json"
