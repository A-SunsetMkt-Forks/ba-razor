# ba-razor

> A tool to razor blue archive momotalk, scenario and more.

## Usage

**1. Create Poetry virtual environment and activate it**

```shell
poetry install
poetry shell
```

**2. Input the command to get help**

```shell
python razor.py --help
```

## Examples

**1. Razor momotalk to directory `output` using yaml CDumper**

```shell
python razor.py momotalk -d "./output" -D CDumper
```

**2. Razor scenario from source `./resources` to directory `output`**

> :exclamation: The feature of razoring scenario is still not implemented.

```shell
python razor.py scenario -d "./output" -s "./resources"
```

## Milestones

- [x] razor momotalk
- [ ] razor scenario
- [ ] more friendly console line interface (CLI)