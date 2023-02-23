"""主线剧情"""

import json

from typing import List
from pathlib import Path
from functions.scenario import process_scenario

from model import ScenarioOutput

def process_main_scenario(resource_path: str | Path) -> List[ScenarioOutput]:
    raw_resource_path = Path(resource_path) if isinstance(resource_path, str) else resource_path
    raw_excel_path = raw_resource_path / "Excel"
    favor_scenario_files = raw_excel_path.glob("ScenarioScriptMain[0-9]*ExcelTable.json")
    print(favor_scenario_files)
    return process_scenario(favor_scenario_files)