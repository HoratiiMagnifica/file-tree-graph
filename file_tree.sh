#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/file-tree-graph"

RED='\033[0;31m'
NC='\033[0m'

if [ -f "$SCRIPT_DIR/file_tree_graph.py" ]; then
    PYTHON_SCRIPT="$SCRIPT_DIR/file_tree_graph.py"
elif [ -f "/usr/local/bin/file-tree-graph" ]; then
    PYTHON_SCRIPT="/usr/local/bin/file-tree-graph"
elif [ -f "$HOME/.local/bin/file-tree-graph" ]; then
    PYTHON_SCRIPT="$HOME/.local/bin/file-tree-graph"
else
    echo -e "${RED}❌ Ошибка: file-tree-graph не найден${NC}"
    echo "Запустите install.sh для установки"
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$@"