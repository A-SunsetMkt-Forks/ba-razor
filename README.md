# ba-razor

[![Auto release](https://github.com/ba-archive/ba-razor/actions/workflows/ci.yml/badge.svg)](https://github.com/ba-archive/ba-razor/actions/workflows/ci.yml)

> A tool to razor blue archive momotalk, scenario and more.

## Usage

**1. Create poetry virtual environment and activate it**

```shell
poetry install
poetry shell
```

**2. Input the command to get help**

```shell
python razor.py --help
```

**3. Use `process_all.sh` to razor and amend all the thing**

```
GIT_PATH="<you_git_path>" bash process_all.sh
```

## Examples

### i) Razor momotalk

**1. Razor scenario from source `./ba-data` to directory `output/momotalk_jp`**

```shell
python razor.py scenario -d "./output/momotalk_jp" -s "./ba-data"
```

### ii) Amend momotalk

1. Amend `output/momotalk_gl` to `output/momotalk_jp` dump to output/momotalk_amend

```shell
python razor.py amend_momotalk -s "output/momotalk_jp" -a "output/momotalk_gl" -o momotalk_amend
```

### ii) Amend scenario

1. Amend `output/scenario_gl` to `output/scenario_jp`  dump to output

```shell
python razor.py amend_scenario -s "output/scenario_jp" -a "output/scenario_gl" -o output
```

## Milestones

- [x] razor momotalk
- [x] amend momotalk
- [x] razor favor scenario
- [x] razor main scenario
- [x] more friendly console line interface (CLI)
