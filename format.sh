#!/bin/bash

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYPROJECT_TOML="pyproject.toml"

echo -e "${BLUE}[INFO]${NC} Formatting Python code in python_backend/"
echo

echo -e "${BLUE}[INFO]${NC} Running isort..."
python3 -m isort "$PROJECT_ROOT" --settings-path="$PYPROJECT_TOML"

echo -e "${BLUE}[INFO]${NC} Running black..."
python3 -m black "$PROJECT_ROOT" --config="$PYPROJECT_TOML"

echo
echo -e "${GREEN}[SUCCESS]${NC} Code formatting complete!"