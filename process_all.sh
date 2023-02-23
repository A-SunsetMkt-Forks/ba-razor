#!/bin/bash
set -e

git_url="https://github.com/electricgoat/ba-data"
git_path="/home/notnotype/CodeRepositories/GitHub/ba-data/"
script_dir="$(pwd)"
echo $script_dir

# razing momotalk
cd "${git_path}"
git fetch
git switch global
git reset --hard HEAD
cd "${script_dir}"
python razor.py momotalk -s "${git_path}" -o "./output/momotalk_gl"

cd "${git_path}"
git switch jp
git reset --hard HEAD
cd "${script_dir}"
python razor.py momotalk -s "${git_path}" -o "./output/momotalk_jp"

# amend
python razor.py amend -s "./output/momotalk_jp" -a "./output/momotalk_gl"