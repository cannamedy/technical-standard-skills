#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
agents_skills_dir="${HOME}/.agents/skills"

skills=(
  technical-specification-guide
  engineering-contract-spec
  machine-contract-spec
  conformance-specification
  contract-implementation-planner
  contract-driven-coding
  technical-document-publisher
  assessment-question-designer
)

mkdir -p -- "$agents_skills_dir"

for skill in "${skills[@]}"; do
  source_dir="$repo_dir/$skill"
  target_path="$agents_skills_dir/$skill"

  if [[ ! -d "$source_dir" ]]; then
    printf 'ERROR: missing Skill directory: %s\n' "$source_dir" >&2
    exit 1
  fi

  if [[ -L "$target_path" ]]; then
    resolved_target="$(readlink -f -- "$target_path" || true)"
    if [[ "$resolved_target" == "$source_dir" ]]; then
      printf 'OK: existing symlink retained: %s -> %s\n' "$target_path" "$source_dir"
      continue
    fi

    printf 'ERROR: target exists as an incorrect symlink: %s\n' "$target_path" >&2
    printf '       expected: %s\n' "$source_dir" >&2
    printf '       refusing to remove or replace it.\n' >&2
    exit 1
  fi

  if [[ -e "$target_path" ]]; then
    printf 'ERROR: target exists and is not a symlink: %s\n' "$target_path" >&2
    printf '       refusing to remove or replace it.\n' >&2
    exit 1
  fi

  ln -s -- "$source_dir" "$target_path"
  printf 'OK: symlink created: %s -> %s\n' "$target_path" "$source_dir"
done

printf 'Installation complete.\n'
