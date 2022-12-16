import os
import click
from colorama import Fore
import re


def rename_momotalk(target_dir: str):
    """把资讯站提供的 momotalk 文件重命名为角色 ID"""
    """重命名前的文件格式为：/\[文件\]\[?角色名\]?五位数ID\s?.ya?ml/i"""
    """e.g.: [待校]切里诺(温泉)20009 .yml"""
    """重命名后的文件只会包含角色 ID，yml 还是 yaml 都可以"""

    file_list = os.listdir(target_dir)
    ignored_files = []

    for file in file_list:
        renamed_basename = re.sub(r"[^0-9]", "", file)
        if len(renamed_basename.strip()) > 0:  # 排除特殊文件，如 .DS_Store
            click.echo(f"{Fore.BLUE}Rename file [{file}] to [{renamed_basename}.yml]{Fore.RESET}")
            os.rename(os.path.join(target_dir, file), os.path.join(target_dir, renamed_basename + ".yml"))
        else:
            ignored_files.append(file)

    if len(ignored_files) > 0:
        click.echo(f"{Fore.RED}Ignored files: {ignored_files}{Fore.RESET}")
