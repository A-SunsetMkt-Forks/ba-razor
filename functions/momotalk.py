import json
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from typing import List

from colorama import Fore

from model import FavorScenario, MomotalkOutput, MomotalkContent
from utils import Localizer


def process_momotalk(resource_path: str | Path) -> List[MomotalkOutput]:
    raw_resource_path = Path(resource_path) if isinstance(resource_path, str) else resource_path
    raw_excel_path = raw_resource_path / "Excel"

    raw_academy_message_data = []
    localizer = Localizer(resource_path)

    academy_message_files = raw_excel_path.glob("AcademyMessanger[0-9]*ExcelTable.json")
    for file in academy_message_files:
        with open(file, encoding="utf8") as fd:
            raw_academy_message_data += json.load(fd)["DataList"]
    raw_academy_message_data = filter(itemgetter("CharacterId"), raw_academy_message_data)

    #  get_favor_schedule_titles
    with open(raw_excel_path / "AcademyFavorScheduleExcelTable.json", encoding="utf8") as fd:
        academy_favor_schedule_data = json.load(fd)["DataList"]
    academy_favor_schedule_data = filter(itemgetter("CharacterId"), academy_favor_schedule_data)

    chained = []
    momotalk_outputs = []
    character_ids = set()

    # 需要先排序，然后才能 groupby
    sorted_academy_message_data = sorted(raw_academy_message_data, key=itemgetter("CharacterId"))
    grouped_academy_message_data = groupby(sorted_academy_message_data, itemgetter("CharacterId"))
    for k, g in grouped_academy_message_data:
        character_ids.add(k)
        chained.append((k, list(g)))

    sorted_academy_favor_schedule_data = sorted(academy_favor_schedule_data, key=itemgetter("CharacterId"))
    grouped_academy_favor_schedule_data = groupby(sorted_academy_favor_schedule_data, itemgetter("CharacterId"))
    for k, g in grouped_academy_favor_schedule_data:
        if k in character_ids:
            chained.append((k, list(g)))
        else:
            print(f"{Fore.BLUE}Unmatched academy_favor_schedule_data: [character_id: {k}]{Fore.RESET}")

    sorted_chained = sorted(chained, key=lambda x: x[0])
    grouped_chained = groupby(sorted_chained, lambda x: x[0])
    for character_id, ((_, academy_messages), (_, favor_schedules)) in grouped_chained:
        print(f"processing momotalk: [character_id: {Fore.GREEN}{character_id}{Fore.RESET}]")
        momotalk_output = MomotalkOutput(CharacterId=character_id, translator='')
        for academy_message in academy_messages:
            momotalk_content = MomotalkContent(**academy_message)
            momotalk_output.content.append(momotalk_content)
        for favor_schedule in favor_schedules:
            favor_scenario = FavorScenario(
                GroupId=favor_schedule["ScenarioSriptGroupId"],  # 棒子程序员拼错了，不需要把 Sript 改成 Script
                FavorScheduleId=favor_schedule["Id"],
                CharacterId=favor_schedule["CharacterId"],
                TextJp=localizer.localize(favor_schedule["LocalizeScenarioId"], "Jp"),
                TextCn=localizer.localize(favor_schedule["LocalizeScenarioId"], "Cn"),
                TextKr=localizer.localize(favor_schedule["LocalizeScenarioId"], "Kr"),
                TextEn=localizer.localize(favor_schedule["LocalizeScenarioId"], "En"),
                TextTh=localizer.localize(favor_schedule["LocalizeScenarioId"], "Th"),
                TextTw=localizer.localize(favor_schedule["LocalizeScenarioId"], "Tw"),
            )
            momotalk_output.title.append(favor_scenario)
        momotalk_outputs.append(momotalk_output)
    return momotalk_outputs
