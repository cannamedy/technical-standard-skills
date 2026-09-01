#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$repo_dir"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'ERROR: %s is not a Git repository.\n' "$repo_dir" >&2
  exit 1
fi

git pull --ff-only
./install.sh
