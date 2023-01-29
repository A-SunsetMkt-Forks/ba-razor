"""好感剧情"""

import os
import json
import yaml

from colorama import Fore, Back, Style
from typing import Optional, List, Iterable
from pathlib import Path
from itertools import groupby, chain
from operator import itemgetter, getitem
from pydantic import BaseModel, validator
from icecream import ic

from model import FavorScenarioContent, FavorScenarioOutput
from utils import Localizer

def process_favor_scenario(resource_path: str | Path) -> List[FavorScenarioOutput]:
    raw_resource_path = Path(resource_path) if isinstance(resource_path, str) else resource_path
    raw_excel_path = raw_resource_path / "Excel"

    raw_favor_scenario_data = []

    favor_scenario_files = raw_excel_path.glob("ScenarioScriptFavor[0-9]*ExcelTable.json")
    for file in favor_scenario_files:
        with open(file, encoding="utf8") as fd:
            raw_favor_scenario_data += json.load(fd)["DataList"]
    raw_favor_scenario_data = filter(itemgetter("GroupId"), raw_favor_scenario_data)

    sorted_favor_scenario_data = sorted(raw_favor_scenario_data, key=itemgetter("GroupId"))
    grouped_favor_scenario_data = groupby(sorted_favor_scenario_data, itemgetter("GroupId"))

    favor_scenario_outputs = []
    for group_id, favor_secnarios in grouped_favor_scenario_data:
        favoro_scenario_output = FavorScenarioOutput(GroupId=group_id)

        for each in favor_secnarios:
            favor_scenario = FavorScenarioContent(**each)
            favoro_scenario_output.content.append(favor_scenario)

        favor_scenario_outputs.append(favoro_scenario_output)
    
    return favor_scenario_outputs
    