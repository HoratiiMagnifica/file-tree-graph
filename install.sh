#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}📁 File Tree Graph Installer${NC}"
echo -e "${BLUE}================================${NC}"

if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Запуск от root. Установка будет в /usr/local/bin${NC}"
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
fi

mkdir -p "$INSTALL_DIR"
mkdir -p "$HOME/.config/file-tree-graph"

echo -e "\n${BLUE}📦 Копирование файлов...${NC}"
cp file_tree_graph.py "$INSTALL_DIR/file-tree-graph"
cp file_tree.sh "$INSTALL_DIR/ftg" 2>/dev/null || echo -e "${YELLOW}⚠️  file_tree.sh не найден, пропускаем${NC}"

chmod +x "$INSTALL_DIR/file-tree-graph" 2>/dev/null
chmod +x "$INSTALL_DIR/ftg" 2>/dev/null

echo -e "\n${BLUE}🔍 Проверка Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 не найден${NC}"
    echo "Установите Python: https://python.org"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✅ Python $PY_VERSION найден${NC}"

if (( $(echo "$PY_VERSION < 3.6" | bc -l 2>/dev/null) )); then
    echo -e "${YELLOW}⚠️  Рекомендуется Python 3.6 или выше (у вас $PY_VERSION)${NC}"
    echo "Некоторые функции могут не работать"
fi

# Добавление в PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "\n${YELLOW}⚠️  Директория $INSTALL_DIR не в PATH${NC}"
    
    SHELL_CONFIG="$HOME/.bashrc"
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    fi
    
    echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_CONFIG"
    echo -e "${GREEN}✅ Добавлено в $SHELL_CONFIG${NC}"
    echo -e "${YELLOW}🔄 Перезапустите терминал или выполните: source $SHELL_CONFIG${NC}"
fi

cat > "$HOME/.config/file-tree-graph/config.json" << EOF
{
    "max_console_lines": 50,
    "default_recursive": false,
    "default_show_files": false
}
EOF

echo -e "\n${GREEN}✅ Установка завершена!${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "📁 Использование:"
echo -e "   ${YELLOW}file-tree-graph${NC}        # Полное имя"
if [ -f "$INSTALL_DIR/ftg" ]; then
    echo -e "   ${YELLOW}ftg${NC}                   # Короткая команда"
fi
echo -e "   ${YELLOW}file-tree-graph -r -f${NC}  # Всё рекурсивно"
echo -e "   ${YELLOW}file-tree-graph -h${NC}     # Помощь"
echo -e "${BLUE}================================${NC}"

echo -e "\n${BLUE}🚀 Проверка установки...${NC}"
if command -v file-tree-graph &> /dev/null; then
    file-tree-graph --help
else
    echo -e "${YELLOW}⚠️  Перезапустите терминал или используйте:${NC}"
    echo "   $INSTALL_DIR/file-tree-graph --help"
fi
