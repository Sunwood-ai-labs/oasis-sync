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

SOURCE_DIR="${SOURCE_PREFIX%/}"
if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Source directory '${SOURCE_DIR}' does not exist. Nothing to sync."
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

if [[ -n "${CLEAN_PATH}" ]]; then
  rm -rf "${TARGET_ROOT}"
  mkdir -p "${TARGET_ROOT}"
  cp -a "${SOURCE_DIR}/." "${TARGET_ROOT}/"
else
  find target -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf {} +
  cp -a "${SOURCE_DIR}/." target/
fi

echo "Copied contents of '${SOURCE_DIR}' to '${TARGET_ROOT}'"

(
  cd target
  git config user.name "oasis-sync[bot]"
  git config user.email "oasis-sync[bot]@users.noreply.github.com"

  if [[ -n "${CLEAN_PATH}" ]]; then
    git add --all "${CLEAN_PATH}"
  else
    git add --all .
  fi

  if git diff --cached --quiet; then
    echo "No ${PLATFORM} article changes to commit."
    exit 0
  fi

  COMMIT_MESSAGE="${COMMIT_MESSAGE:-Sync new ${PLATFORM} articles from oasis-sync}"
  git commit -m "${COMMIT_MESSAGE}"
  git push origin HEAD:"${TARGET_BRANCH}"
)
