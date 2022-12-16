import io
import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel
import yaml


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


class Localizer:
    def __init__(self, resource_path: str):
        raw_resource_path = Path(resource_path)
        localize_scenario_excel_path = raw_resource_path / "Excel" / "LocalizeScenarioExcelTable.json"

        self.hash_map = dict()
        with open(localize_scenario_excel_path, encoding="utf8") as fd:
            localize_scenario_data = json.load(fd)["DataList"]
        for each in localize_scenario_data:
            self.hash_map[each["Key"]] = each

    def localize(self, key: int, lang: str = "Jp") -> str:
        """Excel/LocalizeScenarioExcelTable.json"""
        return self.hash_map[key][lang] if lang in self.hash_map[key] else ""


def save_yaml(model: BaseModel, distinction: str | io.StringIO | Path, dumper: str | Any = MyDumper):
    if isinstance(dumper, str):
        if dumper.lower() == 'cdumper':
            dumper = yaml.CDumper
        elif dumper.lower() == 'mydumper':
            dumper = MyDumper
        else:
            if hasattr(yaml, dumper):
                dumper = getattr(yaml, dumper)

    if isinstance(distinction, str) or isinstance(distinction, Path):
        with open(distinction, "w", encoding="utf8") as fd:
            yaml.dump(model.dict(), fd, sort_keys=False, allow_unicode=True, Dumper=dumper, encoding="utf8")
    else:
        yaml.dump(model.dict(), distinction, sort_keys=False, allow_unicode=True, Dumper=dumper, encoding="utf8")
