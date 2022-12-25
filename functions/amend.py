import pathlib
import re
from pathlib import Path

import yaml
from colorama import Fore

from model import FavorScenario, MomotalkOutput, MomotalkContent
from utils import save_yaml


def amend_momotalk(source_path: str | Path, amend_path: str | Path, output_path: str | Path):
    source_path = Path(source_path) if isinstance(source_path, str) else source_path
    amend_path = Path(amend_path) if isinstance(amend_path, str) else amend_path
    output_path = Path(output_path) if isinstance(output_path, str) else amend_path

    source_path.mkdir(parents=True, exist_ok=True)
    amend_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    regex = re.compile(r"[^0-9]")

    def standardize_filename(filename: pathlib.Path) -> pathlib.Path:
        return pathlib.Path(regex.sub("", filename.stem) + filename.suffix)

    for each_source_file in source_path.glob("*.yml"):
        # get source file path
        each_amend_file = amend_path / standardize_filename(each_source_file)
        # get amend file path
        if not each_amend_file.exists() or each_amend_file.is_dir():
            continue
        # get output file path
        output_file = output_path / each_source_file.name

        print(
            f"{Fore.GREEN}Amending [{each_amend_file.name}] -> [{each_source_file.name}] dump to [{output_file}]{Fore.RESET}")

        with open(each_source_file, "r", encoding="utf8") as f:
            source_data = MomotalkOutput(**yaml.load(f, Loader=yaml.CLoader))
        with open(each_amend_file, "r", encoding="utf8") as f:
            amend_data = MomotalkOutput(**yaml.load(f, Loader=yaml.CLoader))

        assert source_data.CharacterId == amend_data.CharacterId

        def __amend_title(a: FavorScenario, b: FavorScenario):
            a.TextJp = b.TextJp if b.TextJp else a.TextJp or ""
            a.TextCn = b.TextCn if b.TextCn else a.TextCn or ""
            a.TextKr = b.TextKr if b.TextKr else a.TextKr or ""
            a.TextEn = b.TextEn if b.TextEn else a.TextEn or ""
            a.TextTh = b.TextTh if b.TextTh else a.TextTh or ""
            a.TextTw = b.TextTw if b.TextTw else a.TextTw or ""

        def __amend_content(a: MomotalkContent, b: MomotalkContent):
            a.MessageKR = b.MessageKR if b.MessageKR else a.MessageKR or ""
            a.MessageJP = b.MessageJP if b.MessageJP else a.MessageJP or ""
            a.MessageCN = b.MessageCN if b.MessageCN else a.MessageCN or ""
            a.MessageEN = b.MessageEN if b.MessageEN else a.MessageEN or ""
            a.MessageTH = b.MessageTH if b.MessageTH else a.MessageTH or ""
            a.MessageTW = b.MessageTW if b.MessageTW else a.MessageTW or ""

        # amend title
        for each_source_momotalk_content in source_data.title:
            for each_amend_momotalk_content in amend_data.title:
                if each_source_momotalk_content.GroupId == each_amend_momotalk_content.GroupId:
                    __amend_title(each_source_momotalk_content, each_amend_momotalk_content)
                    break

        # amend content
        for each_source_momotalk_content in source_data.content:
            for each_amend_momotalk_content in amend_data.content:
                if each_source_momotalk_content.Id == each_amend_momotalk_content.Id:
                    __amend_content(each_source_momotalk_content, each_amend_momotalk_content)
                    break

        save_yaml(source_data, output_file)
