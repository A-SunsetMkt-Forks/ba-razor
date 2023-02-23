import pathlib
from typing import Optional

import click
from colorama import Fore

from functions.amend import amend_momotalk
from functions.momotalk import process_momotalk
from functions.favor_scenario import process_favor_scenario
from functions.rename import rename_momotalk
from utils import save_yaml, save_json


@click.group()
def _root():
    """A tool to razor blue archive momotalk, scenario and more."""
    pass

@_root.command("momotalk")
@click.option("--source", "-s", required=True)
@click.option("--destination", "-d", "--output", "-o", type=str, default="./output/momotalk")
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

@_root.command("favor_scenario")
@click.option("--source", "-s", type=str, required=True)
@click.option("--destination", "-d", "--output", "-o", type=str, default="./output/main_scenario")
def _favor_scenario(source: str, destination: str):
    """razor favor scenario

    :arg dumper: yaml dumper: CDumper(faster) | Dumper | MyDumper(slowest)
    """
    click.echo("Razing momotalk")
    output_resource_path = pathlib.Path(destination)
    output_resource_path.mkdir(parents=True, exist_ok=True)

    favor_scenario_outputs = process_favor_scenario(source)
    for favor_scenario_output in favor_scenario_outputs:
        file_path = output_resource_path / f"{favor_scenario_output.GroupId}.json"
        print(f"{Fore.BLUE}Parse data to yaml and write to file [{file_path}]{Fore.RESET}")
        save_json(favor_scenario_output, file_path)

@_root.command("main_scenario")
@click.option("--source", "-s", type=str, required=True)
@click.option("--destination", "-d", "--output", "-o", type=str, default="./output/favor_scenario")
def _main_scenario(source: str, destination: str):
    """razor favor scenario

    :arg dumper: yaml dumper: CDumper(faster) | Dumper | MyDumper(slowest)
    """
    click.echo("Razing momotalk")
    output_resource_path = pathlib.Path(destination)
    output_resource_path.mkdir(parents=True, exist_ok=True)

    favor_scenario_outputs = process_favor_scenario(source)
    for favor_scenario_output in favor_scenario_outputs:
        file_path = output_resource_path / f"{favor_scenario_output.GroupId}.json"
        print(f"{Fore.BLUE}Parse data to yaml and write to file [{file_path}]{Fore.RESET}")
        save_json(favor_scenario_output, file_path)

@_root.command("amend")
@click.option("--source", "-s", type=str, required=True)
@click.option("--amend", "-a", type=str, required=True)
@click.option("--destination", "-d", "--output", "-o", type=str)
def _amend(source: str, amend: str, destination: Optional[str] = None):
    destination = destination or source
    click.echo("Amending momotalk")
    amend_momotalk(source, amend, destination)


@_root.command("rename")
@click.option("--source", "-s", type=str, default="./resources")
@click.option("--mode", "-m", type=str, default="momotalk")
def _momotalk_rename(source: str, mode: str):
    """rename momotalk files to standard name"""
    output_resource_path = source

    if "momotalk" == mode:
        click.echo("Renaming momotalk")
        rename_momotalk(output_resource_path)


if __name__ == '__main__':
    _root()
