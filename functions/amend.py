import pathlib
from pathlib import Path

import yaml
from colorama import Fore

from model import FavorSchedule, MomotalkOutput, MomotalkContent, I18Text, I18Message, Amendable, AmendableOutput
from format_parser import FormatParser, save_yaml


def amend_momotalk(
    source_path: str | Path, amend_path: str | Path, output_path: str | Path, parser: FormatParser,
    model: type[AmendableOutput], glob_str: str = "*", 
):
    source_path = Path(source_path) if isinstance(source_path, str) else source_path
    amend_path = Path(amend_path) if isinstance(amend_path, str) else amend_path
    output_path = Path(output_path) if isinstance(output_path, str) else amend_path

    source_path.mkdir(parents=True, exist_ok=True)
    amend_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)


    for each_source_file in source_path.glob(glob_str):
        # get output file path
        output_file = output_path / each_source_file.name

        # get amend file path
        each_amend_file = amend_path / each_source_file.name
        
        # 如果没有对应的amend文件，直接输出原文件
        if not each_amend_file.exists() or each_amend_file.is_dir():
            print(f"{Fore.BLUE}Copying  [{each_amend_file.name}] -> [{output_file}]{Fore.RESET}")
            source_data = parser.load(model, each_source_file)
            parser.save(source_data, output_file)
            continue

        print(
            f"{Fore.GREEN}Amending [{each_amend_file.name}] -> [{each_source_file.name}] dump to [{output_file}]{Fore.RESET}")

        source_data = parser.load(model, each_source_file)
        amend_data = parser.load(model, each_amend_file)

        # amend
        source_data.amend(amend_data)
        
        parser.save(source_data, output_file)
