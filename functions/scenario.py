"""通用剧情"""

import json

from typing import List
from itertools import groupby
from operator import itemgetter
from icecream import ic

from model import ScenarioContent, ScenarioOutput

def process_scenario(favor_scenario_files: List[str]) -> List[ScenarioOutput]:
    raw_favor_scenario_data = []

    for file in favor_scenario_files:
        with open(file, encoding="utf8") as fd:
            raw_favor_scenario_data += json.load(fd)["DataList"]
    raw_favor_scenario_data = filter(itemgetter("GroupId"), raw_favor_scenario_data)

    sorted_favor_scenario_data = sorted(raw_favor_scenario_data, key=itemgetter("GroupId"))
    grouped_favor_scenario_data = groupby(sorted_favor_scenario_data, itemgetter("GroupId"))

    favor_scenario_outputs = []
    for group_id, favor_secnarios in grouped_favor_scenario_data:
        favoro_scenario_output = ScenarioOutput(GroupId=group_id)

        for each in favor_secnarios:
            favor_scenario = ScenarioContent(**each)
            favoro_scenario_output.content.append(favor_scenario)

        favor_scenario_outputs.append(favoro_scenario_output)
    
    return favor_scenario_outputs
    