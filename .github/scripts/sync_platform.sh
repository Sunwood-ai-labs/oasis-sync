#!/usr/bin/env bash

set -euo pipefail

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Environment variable ${name} is required." >&2
    exit 1
  fi
}

require_env "PLATFORM"
require_env "SOURCE_PREFIX"
require_env "TARGET_REPOSITORY"
require_env "TARGET_BRANCH"
require_env "SYNC_TOKEN"

NORMALIZED_TARGET_REPOSITORY="${TARGET_REPOSITORY#https://github.com/}"
NORMALIZED_TARGET_REPOSITORY="${NORMALIZED_TARGET_REPOSITORY#git@github.com:}"
NORMALIZED_TARGET_REPOSITORY="${NORMALIZED_TARGET_REPOSITORY%.git}"

if [[ -z "${NORMALIZED_TARGET_REPOSITORY}" ]]; then
  echo "Failed to determine target repository from TARGET_REPOSITORY='${TARGET_REPOSITORY}'." >&2
  exit 1
fi

BASE_SHA="${BEFORE_SHA:-}"
if [[ -z "${BASE_SHA}" || "${BASE_SHA}" =~ ^0+$ ]]; then
  if git rev-parse HEAD^ >/dev/null 2>&1; then
    BASE_SHA="$(git rev-parse HEAD^)"
  else
    BASE_SHA="$(git hash-object -t tree /dev/null)"
  fi
fi

mapfile -t FILES < <(
  git diff --name-status "${BASE_SHA}" HEAD -- |
    awk -v prefix="${SOURCE_PREFIX}/" '$1 == "A" && index($2, prefix) == 1 && $2 ~ /\.md$/ {print $2}'
)

if [[ "${#FILES[@]}" -eq 0 ]]; then
  echo "No new ${PLATFORM} articles detected."
  exit 0
fi

REPO_URL="https://x-access-token:${SYNC_TOKEN}@github.com/${NORMALIZED_TARGET_REPOSITORY}"
git clone --depth 1 --branch "${TARGET_BRANCH}" "${REPO_URL}" target

CLEAN_PATH="${TARGET_PATH#./}"
CLEAN_PATH="${CLEAN_PATH#/}"
CLEAN_PATH="${CLEAN_PATH%/}"

TARGET_ROOT="target"
if [[ -n "${CLEAN_PATH}" ]]; then
  TARGET_ROOT="target/${CLEAN_PATH}"
fi

mkdir -p "${TARGET_ROOT}"
MANIFEST="$(mktemp)"

for SOURCE_PATH in "${FILES[@]}"; do
  if [[ ! -f "${SOURCE_PATH}" ]]; then
    echo "Skipping missing file ${SOURCE_PATH}"
    continue
  fi

  REL_PATH="${SOURCE_PATH#"${SOURCE_PREFIX}/"}"
  DEST_PATH="${TARGET_ROOT}/${REL_PATH}"
  mkdir -p "$(dirname "${DEST_PATH}")"
  cp "${SOURCE_PATH}" "${DEST_PATH}"

  if [[ -n "${CLEAN_PATH}" ]]; then
    echo "${CLEAN_PATH}/${REL_PATH}" >>"${MANIFEST}"
  else
    echo "${REL_PATH}" >>"${MANIFEST}"
  fi

  echo "Copied ${SOURCE_PATH} -> ${DEST_PATH}"
done

if [[ ! -s "${MANIFEST}" ]]; then
  echo "No files copied; nothing to commit."
  rm -f "${MANIFEST}"
  exit 0
fi

(
  cd target
  git config user.name "oasis-sync[bot]"
  git config user.email "oasis-sync[bot]@users.noreply.github.com"

  while IFS= read -r PATH_IN_REPO; do
    git add "${PATH_IN_REPO}"
  done <"${MANIFEST}"

  if git diff --cached --quiet; then
    echo "No changes to commit."
    rm -f "${MANIFEST}"
    exit 0
  fi

  COMMIT_MESSAGE="${COMMIT_MESSAGE:-Sync new ${PLATFORM} articles from oasis-sync}"
  git commit -m "${COMMIT_MESSAGE}"
  git push origin HEAD:"${TARGET_BRANCH}"
)

rm -f "${MANIFEST}"
