# 🌳 File Tree Graph

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![OS: Linux/macOS](https://img.shields.io/badge/OS-Linux%20|%20macOS-lightgrey.svg)](https://github.com/yourusername/file-tree-graph)

**Красивый и понятный граф файловой структуры для документации и нейросетей.**


```bash
git clone https://github.com/HoratiiMagnifica/file-tree-graph.git
cd file-tree-graph
chmod +x install.sh
./install.sh
```
```
usage: file-tree-graph [-h] [-r] [-f] [-e EXCLUDE] [-o OUTPUT] [path]

Генератор графа файловой структуры для нейросети

positional arguments:
  path                  Путь к анализируемой директории (по умолчанию текущая)

options:
  -h, --help            show this help message and exit
  -r, --recursive       Просмотреть все вложенные папки
  -f, --files           Показать файлы (вместе с -r показывает всё рекурсивно)
  -e EXCLUDE, --exclude EXCLUDE
                        Исключить папку (можно использовать несколько раз)
  -o OUTPUT, --output OUTPUT
                        Файл для сохранения результата

Примеры использования:
  python3 file_tree_graph.py -r          # Только папки рекурсивно
  python3 file_tree_graph.py -f          # Файлы и папки в текущей директории
  python3 file_tree_graph.py -r -f       # Всё рекурсивно
  python3 file_tree_graph.py -r -e node_modules -e .git  # Исключить папки
  python3 file_tree_graph.py -r -f -o output.txt  # Сохранить в файл
```


```
🔍 Анализируем: /var/www/file-tree-graph
📈 Статистика: 18 папок, 32 файлов, 52.5 KB

📊 Найдено 18 строк в выводе
1. Вывести в консоль
2. Сохранить в файл
3. И то, и другое

Ваш выбор (1-3): 1

============================================================
📁 ФАЙЛОВАЯ СТРУКТУРА: /var/www/file-tree-graph
============================================================
Рекурсивно: ✅
Показывать файлы: ❌
============================================================

📁 file-tree-graph/
    └── 📁 .git
        ├── 📁 branches
        ├── 📁 hooks
        ├── 📁 info
        ├── 📁 logs
        │   └── 📁 refs
        │       ├── 📁 heads
        │       └── 📁 remotes
        │           └── 📁 origin
        ├── 📁 objects
        │   ├── 📁 info
        │   └── 📁 pack
        └── 📁 refs
            ├── 📁 heads
            ├── 📁 remotes
            │   └── 📁 origin
            └── 📁 tags

============================================================
✅ Граф файловой структуры готов!

```  
