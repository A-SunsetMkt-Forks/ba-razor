import pathlib

import click
import yaml
from colorama import Fore

from momotalk import process_momotalk
from utils import MyDumper


@click.group()
def _root():
    """A tool to razor blue archive momotalk, scenario and more."""
    pass


@_root.command("momotalk")
@click.option("--source", "-s", type=str, default="./resources")
@click.option("--distinction", "-d", type=str, default="./output")
def _momotalk(source: str, distinction: str):
    """razor momotalk"""
    click.echo("Razing momotalk")
    output_resource_path = pathlib.Path(distinction)

    momotalk_outputs = process_momotalk(source)
    for momotalk_output in momotalk_outputs:
        file_path = output_resource_path / f"{momotalk_output.CharacterId}.yaml"
        print(f"{Fore.BLUE}Parse data to yaml and write to file [{file_path}]{Fore.RESET}")
        with open(file_path, mode="w") as fd:
            yaml.dump(momotalk_output.dict(), fd, sort_keys=False, allow_unicode=True, Dumper=MyDumper)


@_root.command("scenario")
@click.option("--source", "-s", type=str, default="./output")
@click.option("--distinction", "-d", type=str, default="./output")
def _scenario(source: str, distinction: str):
    """razor scenario"""
    click.echo("Razing scenario (NotImplemented)")


if __name__ == '__main__':
    _root()
