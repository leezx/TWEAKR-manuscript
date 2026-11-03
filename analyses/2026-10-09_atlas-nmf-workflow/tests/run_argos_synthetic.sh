#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
ENV=/home/zz950/softwares/miniforge3/envs/argos-codex
export PATH="$ENV/bin:$PATH"
export R_LIBS_USER="$ENV/lib/R/user-library"
exec > >(tee "$1") 2>&1
date -u
hostname
printf 'Environment: %s\nSynthetic tests only; no real Atlas input\n' "$ENV"
find "$ROOT/code" "$ROOT/tests" -type f \( -name '*.py' -o -name '*.R' -o -name '*.sh' \) -print0 | sort -z | xargs -0 sha256sum
"$ENV/bin/python" -m unittest discover -s "$ROOT/tests" -v
"$ENV/bin/Rscript" "$ROOT/tests/test_preprocessing.R" "$ROOT/code/02_prepare_seurat_nmf.R"
printf 'ALL SYNTHETIC TESTS PASSED\n'
