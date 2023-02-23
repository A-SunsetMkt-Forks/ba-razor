#!/bin/bash
set -e

git_url="https://github.com/electricgoat/ba-data"
git_path="/home/notnotype/CodeRepositories/GitHub/ba-data/"
script_dir="$(pwd)"
echo $script_dir

# global
# razing momotalk
cd "${git_path}"
git fetch
git switch global
git reset --hard HEAD
cd "${script_dir}"
python razor.py momotalk -s "${git_path}" -o "./output/momotalk_gl"
# favor scenario
python razor.py favor_scenario -s "${git_path}" -o "./output/favor_scenario_gl"
# main scenario
python razor.py main_scenario -s "${git_path}" -o "./output/main_scenario_gl"

cd "${git_path}"
git switch jp
git reset --hard HEAD
cd "${script_dir}"
python razor.py momotalk -s "${git_path}" -o "./output/momotalk_jp"
# favor scenario
python razor.py favor_scenario -s "${git_path}" -o "./output/favor_scenario_jp"
# main scenario
python razor.py main_scenario -s "${git_path}" -o "./output/main_scenario_jp"

# amend
python razor.py amend_momotalk -s "./output/momotalk_jp" -a "./output/momotalk_gl"
python razor.py amend_scenario -s "./output/main_scenario_jp" -a "./output/main_scenario_gl"
python razor.py amend_scenario -s "./output/favor_scenario_jp" -a "./output/favor_scenario_gl"