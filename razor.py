import pathlib
from typing import Optional

import click
from colorama import Fore

from functions.momotalk import process_momotalk
from functions.amend import amend_momotalk
from utils import save_yaml

import git


@click.group()
def _root():
    """A tool to razor blue archive momotalk, scenario and more."""
    pass


@_root.command("momotalk")
@click.option("--source", "-s", required=True)
@click.option("--destination", "-d", "--output", "-o", type=str, default="./output")
@click.option("--dumper", "-D", type=str, default="MyDumper")
def _momotalk(source: str, destination: str, dumper: str):
    """razor momotalk

    :arg dumper: yaml dumper: CDumper(faster) | Dumper | MyDumper(slowest)
    """
    click.echo("Razing momotalk")
    output_resource_path = pathlib.Path(destination)
    output_resource_path.mkdir(parents=True, exist_ok=True)

    momotalk_outputs = process_momotalk(source)
    for momotalk_output in momotalk_outputs:
        file_path = output_resource_path / f"{momotalk_output.CharacterId}.yml"
        print(f"{Fore.BLUE}Parse data to yaml and write to file [{file_path}]{Fore.RESET}")
        save_yaml(momotalk_output, file_path, dumper=dumper)


@_root.command("scenario")
@click.option("--source", "-s", type=str, required=True)
@click.option("--destination", "-d", "--output", "-o", type=str, default="./output")
@click.option("--dumper", "-D", type=str, default="MyDumper")
def _scenario(source: str, destination: str, dumper: str):
    """razor scenario

    :arg dumper: yaml dumper: CDumper(faster) | Dumper | MyDumper(slowest)
    """
    click.echo("Razing scenario (NotImplemented)")


@_root.command("amend")
@click.option("--source", "-s", type=str, required=True)
@click.option("--amend", "-a", type=str, required=True)
@click.option("--destination", "-d", "--output", "-o", type=str)
def _amend(source: str, amend: str, destination: Optional[str] = None):
    destination = destination or source
    click.echo("Amending momotalk")
    amend_momotalk(source, amend, destination)


if __name__ == '__main__':
    _root()
