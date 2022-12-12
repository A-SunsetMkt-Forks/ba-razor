import json
from pathlib import Path

import yaml


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


class Localizer:
    def __init__(self, resource_path: str):
        raw_resource_path = Path(resource_path)
        localize_scenario_excel_path = raw_resource_path / "Excel" / "LocalizeScenarioExcelTable.json"

        self.hash_map = dict()
        with open(localize_scenario_excel_path) as fd:
            localize_scenario_data = json.load(fd)["DataList"]
        for each in localize_scenario_data:
            self.hash_map[each["Key"]] = each

    def localize(self, key: int, lang: str = "Jp") -> str:
        """Excel/LocalizeScenarioExcelTable.json"""
        return self.hash_map[key][lang] if lang in self.hash_map[key] else ""
