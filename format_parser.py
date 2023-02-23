import io
import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel
import yaml

class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

T = TypeVar("T", bound=BaseModel)

def load_yaml(model: type[T], source: str | io.StringIO | Path) -> T:
    if isinstance(source, str) or isinstance(source, Path):
        with open(source, "r", encoding="utf8") as fd:
            return model(**yaml.load(fd, Loader=yaml.CLoader))
    else:
        return model(**yaml.load(source, Loader=yaml.CLoader))

def load_json(model: type[T], source: str | io.StringIO | Path) -> T:
    if isinstance(source, str) or isinstance(source, Path):
        with open(source, "r", encoding="utf8") as fd:
            return model(**json.load(fd))
    else:
        return model(**json.load(source))

def save_yaml(model: BaseModel, distinction: str | io.StringIO | Path, dumper: str | Any = MyDumper):
    if isinstance(dumper, str):
        if dumper.lower() == 'cdumper':
            dumper = yaml.CDumper
        elif dumper.lower() == 'mydumper':
            dumper = MyDumper
        else:
            if hasattr(yaml, dumper):
                dumper = getattr(yaml, dumper)

    if isinstance(distinction, str) or isinstance(distinction, Path):
        with open(distinction, "w", encoding="utf8") as fd:
            yaml.dump(model.dict(), fd, sort_keys=False, allow_unicode=True, Dumper=dumper, encoding="utf8")
    else:
        yaml.dump(model.dict(), distinction, sort_keys=False, allow_unicode=True, Dumper=dumper, encoding="utf8")

def save_json(model: BaseModel, distinction: str | io.StringIO | Path):
    if isinstance(distinction, str) or isinstance(distinction, Path):
        with open(distinction, "w", encoding="utf8") as fd:
            json.dump(model.dict(), fd, sort_keys=False, ensure_ascii=False, indent=2)
    else:
        json.dump(model.dict(), distinction, sort_keys=False, ensure_ascii=False, indent=2)

class FormatParser:
    @staticmethod
    def load(model: type[T], source: str | io.StringIO | Path) -> T:
        raise NotImplementedError()

    @staticmethod
    def save(model: T, distinction: str | io.StringIO | Path) -> T:
        raise NotImplementedError()

class JsonParser(FormatParser):
    @staticmethod
    def load(model: type[T], source: str | io.StringIO | Path) -> T:
        return load_json(model, source)

    @staticmethod
    def save(model: T, distinction: str | io.StringIO | Path) -> T:
        return save_json(model, distinction)

class YamlParser(FormatParser):
    @staticmethod
    def load(model: type[T], source: str | io.StringIO | Path) -> T:
        return load_yaml(model, source)

    @staticmethod
    def save(model: T, distinction: str | io.StringIO | Path) -> T:
        return save_yaml(model, distinction)