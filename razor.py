import pathlib

import click
import yaml
from colorama import Fore

from momotalk import process_momotalk
from utils import MyDumper

import git


@click.group()
def _root():
    """A tool to razor blue archive momotalk, scenario and more."""
    pass


@_root.command("momotalk")
@click.option("--source", "-s", type=str, default="./resources")
@click.option("--destination", "-d", "--output", "-o", type=str, default="./output")
def _momotalk(source: str, destination: str):
    """razor momotalk"""
    click.echo("Razing momotalk")
    output_resource_path = pathlib.Path(destination)
    output_resource_path.mkdir(parents=True, exist_ok=True)

    def write_momotalk(src=source):
        momotalk_outputs = process_momotalk(src)
        for momotalk_output in momotalk_outputs:
            file_path = output_resource_path / f"{momotalk_output.CharacterId}.yml"
            print(f"{Fore.BLUE}Parse data to yaml and write to file [{file_path}]{Fore.RESET}")
            with open(file_path, mode="w") as fd:
                yaml.dump(momotalk_output.dict(), fd, sort_keys=False, allow_unicode=True, Dumper=MyDumper)

    # 检查源目录是否是 git 仓库
    try:
        repo = git.repo.Repo(source)
        # 如果是 git 仓库，检查当前分支名
        current_branch = repo.git.rev_parse("--abbrev-ref", "HEAD")
        # 获取所有的分支名
        branch_names = [branch.name for branch in repo.branches]

        # 如果分支名是 jp，直接进行一次写入
        if "jp" == current_branch:
            write_momotalk(source)
            # 如果 global 分支存在，切换到 global 分支，进行一次写入。这样国际服的翻译就能覆盖日服文件的空白字段
            if "global" in branch_names:
                click.echo(f"{Fore.YELLOW}Switch to global branch{Fore.RESET}")
                repo.git.checkout("global")
                write_momotalk(source)
                # 切换回 jp 分支
                click.echo(f"{Fore.YELLOW}Switch back to jp branch{Fore.RESET}")
                repo.git.checkout("jp")
        # 如果分支名是 global 并且 jp 分支存在，切换到 jp 分支，进行一次写入
        elif "global" == current_branch and "jp" in branch_names:
            click.echo(f"{Fore.YELLOW}Switch to jp branch{Fore.RESET}")
            repo.git.checkout("jp")
            write_momotalk(source)
            # 切换回 global 分支
            click.echo(f"{Fore.YELLOW}Switch back to global branch{Fore.RESET}")
            repo.git.checkout("global")
            # 写入
            write_momotalk(source)
    # 如果不是 git 仓库，直接写入
    except (git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError):
        click.echo(f"{Fore.RED}Source is not a git repository: {source}{Fore.RESET}")
        write_momotalk(source)
    except git.GitCommandError as e:  # 提醒添加 git 信任仓库
        if e.status == 128:
            click.echo(f"{Fore.RED}{e.stderr.strip()}{Fore.RESET}")
            click.echo(e.stdout)


@_root.command("scenario")
@click.option("--source", "-s", type=str, default="./output")
@click.option("--distinction", "-d", type=str, default="./output")
def _scenario(source: str, distinction: str):
    """razor scenario"""
    click.echo("Razing scenario (NotImplemented)")


if __name__ == '__main__':
    _root()
