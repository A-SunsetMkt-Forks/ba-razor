#!/bin/bash
set -e

git_url="https://github.com/electricgoat/ba-data"

script_dir="$(pwd)"

if [ $GIT_URL ]; then
    git_url=$GIT_URL
fi
if [ ! $GIT_PATH ]; then
    echo "GIT_PATH is not specified" && exit 1
else
    git_path=$GIT_PATH
fi

if [ ! -e $git_path ]; then
    echo "Create directory: ${git_path}"
    mkdir -p $git_path
fi

cd "${git_path}"
if [ ! -e ".git" ]; then
    git init
    git config --global --add safe.directory "$(pwd)"
    git remote add origin "${git_url}"
    git fetch origin
    git checkout -b master --track --force origin/master
    git reset origin/master
fi
cd "${script_dir}"


exit

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

# jp
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
