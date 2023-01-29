# ba-razor

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

## Examples

### i) Razor momotalk

**1. Razor momotalk to directory `output` using yaml CDumper**

```shell
python razor.py momotalk -d "./output" -D CDumper
```

**2. Razor scenario from source `./resources` to directory `output`**

> :exclamation: The feature of razoring scenario is still not implemented.

```shell
python razor.py scenario -d "./output" -s "./resources"
```

### ii) Amend momotalk

1. Amend output_jp to output_gl dump to output

```shell
python razor.py amend -s output_jp -a output_gl -o output
```

## Milestones

- [x] razor momotalk
- [x] amend momotalk
- [x] razor favor scenario
- [ ] razor main scenario
- [x] more friendly console line interface (CLI)
