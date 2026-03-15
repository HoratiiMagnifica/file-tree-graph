#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}📁 File Tree Graph Installer${NC}"
echo -e "${BLUE}================================${NC}"

# Проверка прав (не требует root, но предупреждаем)
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Запуск от root. Установка будет в /usr/local/bin${NC}"
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
fi

# Создание директории установки
mkdir -p "$INSTALL_DIR"
mkdir -p "$HOME/.config/file-tree-graph"

# Копирование файлов
echo -e "\n${BLUE}📦 Копирование файлов...${NC}"
cp file_tree_graph.py "$INSTALL_DIR/file-tree-graph"
cp file_tree.sh "$INSTALL_DIR/ftg"  # короткий алиас

# Делаем исполняемыми
chmod +x "$INSTALL_DIR/file-tree-graph"
chmod +x "$INSTALL_DIR/ftg"

# Проверка Python
echo -e "\n${BLUE}🔍 Проверка зависимостей...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 не найден${NC}"
    echo "Установите Python: https://python.org"
    exit 1
fi

# Проверка версии Python
PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$PY_VERSION < 3.6" | bc -l) )); then
    echo -e "${RED}❌ Требуется Python 3.6 или выше (у вас $PY_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $PY_VERSION найден${NC}"

# Добавление в PATH (если нужно)
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

# Создание конфига
cat > "$HOME/.config/file-tree-graph/config.json" << EOF
{
    "max_console_lines": 50,
    "default_recursive": false,
    "default_show_files": false
}
EOF

# Финальное сообщение
echo -e "\n${GREEN}✅ Установка завершена!${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "📁 Использование:"
echo -e "   ${YELLOW}ftg${NC}              # Текущая директория"
echo -e "   ${YELLOW}ftg -r${NC}           # Рекурсивно (только папки)"
echo -e "   ${YELLOW}ftg -r -f${NC}        # Всё рекурсивно"
echo -e "   ${YELLOW}ftg /путь/к/папке${NC} # Указать путь"
echo -e "   ${YELLOW}file-tree-graph${NC}   # Полное имя"
echo -e "${BLUE}================================${NC}"

# Тестовый запуск
echo -e "\n${BLUE}🚀 Тестовый запуск...${NC}"
if command -v ftg &> /dev/null; then
    ftg --help
else
    echo -e "${YELLOW}⚠️  Перезапустите терминал для доступа к команде 'ftg'${NC}"
    echo "Или используйте: $INSTALL_DIR/ftg"
fi