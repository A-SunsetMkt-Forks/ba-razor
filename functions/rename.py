import os
import re

import click
from colorama import Fore


def rename_momotalk(target_dir: str):
    """把资讯站提供的 momotalk 文件重命名为角色 ID"""
    """重命名前的文件格式为：/\[文件\]\[?角色名\]?五位数ID\s?.ya?ml/i"""
    """e.g.: [待校]切里诺(温泉)20009 .yml"""
    """重命名后的文件名为：角色 ID.yml"""
    """e.g.: 20009.yml"""

    filename_reg = re.compile(r"[^0-9]")
    filename_match_reg = re.compile(r"[0-9]{5}\s?\.ya?ml", re.IGNORECASE)

    file_list = [filename for filename in os.listdir(target_dir) if bool(re.search(filename_match_reg, filename))]

    for file in file_list:
        renamed_basename = re.sub(filename_reg, "", file)
        click.echo(f"{Fore.BLUE}Rename file [{file}] to [{renamed_basename}.yml]{Fore.RESET}")
        os.rename(os.path.join(target_dir, file), os.path.join(target_dir, renamed_basename + ".yml"))


def rename_scenario(target_dir: str):
    """暂时还不确定会不会和资讯站合作，所以先留着"""
    pass
