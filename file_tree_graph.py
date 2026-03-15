#!/usr/bin/env python3
"""
Скрипт для создания красивого и понятного графа файловой структуры.
Использование: python3 file_tree_graph.py [флаги] [путь]
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Set, Dict

class FileTreeGenerator:
    def __init__(self):
        self.excluded_dirs = set()
        self.show_files = False
        self.recursive = False
        self.output_file = None
        self.max_console_lines = 50
        
    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description='Генератор графа файловой структуры для нейросети',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Примеры использования:
  python3 file_tree_graph.py -r          # Только папки рекурсивно
  python3 file_tree_graph.py -f          # Файлы и папки в текущей директории
  python3 file_tree_graph.py -r -f       # Всё рекурсивно
  python3 file_tree_graph.py -r -e node_modules -e .git  # Исключить папки
  python3 file_tree_graph.py -r -f -o output.txt  # Сохранить в файл
            """
        )
        
        parser.add_argument(
            '-r', '--recursive',
            action='store_true',
            help='Просмотреть все вложенные папки'
        )
        
        parser.add_argument(
            '-f', '--files',
            action='store_true',
            help='Показать файлы (вместе с -r показывает всё рекурсивно)'
        )
        
        parser.add_argument(
            '-e', '--exclude',
            action='append',
            default=[],
            help='Исключить папку (можно использовать несколько раз)'
        )
        
        parser.add_argument(
            '-o', '--output',
            type=str,
            help='Файл для сохранения результата'
        )
        
        parser.add_argument(
            'path',
            nargs='?',
            default='.',
            help='Путь к анализируемой директории (по умолчанию текущая)'
        )
        
        return parser.parse_args()
    
    def should_exclude(self, path: Path, root_path: Path) -> bool:
        """Проверяет, нужно ли исключить директорию"""
        rel_path = path.relative_to(root_path)
        for excluded in self.excluded_dirs:
            if excluded in str(rel_path).split(os.sep):
                return True
        return False
    
    def generate_tree(self, path: Path, prefix: str = "", is_last: bool = True, root_path: Path = None) -> List[str]:
        """Рекурсивно генерирует дерево файловой структуры"""
        if root_path is None:
            root_path = path
        
        lines = []
        
        # Добавляем текущий элемент
        if path == root_path:
            lines.append(f"{prefix}📁 {path.name}/")
        else:
            connector = "└── " if is_last else "├── "
            icon = "📁" if path.is_dir() else "📄"
            lines.append(f"{prefix}{connector}{icon} {path.name}")
        
        # Если это файл или исключенная директория, не идем глубже
        if not path.is_dir() or (self.recursive and self.should_exclude(path, root_path)):
            return lines
        
        # Получаем содержимое директории
        try:
            items = list(path.iterdir())
            
            # Фильтруем: показываем только директории, если не указан флаг -f
            if not self.show_files:
                items = [item for item in items if item.is_dir()]
            
            # Сортируем: сначала директории, потом файлы
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            # Обрабатываем каждый элемент
            for i, item in enumerate(items):
                is_last_item = (i == len(items) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                
                # Если это исключенная директория и мы не рекурсивно её просматриваем
                if item.is_dir() and self.should_exclude(item, root_path):
                    lines.append(f"{new_prefix}{'└── ' if is_last_item else '├── '}📁 {item.name}/ [EXCLUDED]")
                else:
                    lines.extend(self.generate_tree(
                        item, new_prefix, is_last_item, root_path
                    ))
                    
        except PermissionError:
            lines.append(f"{prefix}    🔒 [Permission Denied]")
        except Exception as e:
            lines.append(f"{prefix}    ❌ [Error: {str(e)}]")
        
        return lines
    
    def get_summary_stats(self, path: Path) -> Dict:
        """Собирает статистику по файловой структуре"""
        stats = {
            'directories': 0,
            'files': 0,
            'excluded_dirs': len(self.excluded_dirs),
            'total_size': 0
        }
        
        for root, dirs, files in os.walk(path):
            # Проверяем исключенные директории
            rel_root = Path(root).relative_to(path)
            if any(excluded in str(rel_root).split(os.sep) for excluded in self.excluded_dirs):
                continue
            
            stats['directories'] += 1
            stats['files'] += len(files)
            
            # Считаем размер файлов
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    stats['total_size'] += os.path.getsize(file_path)
                except:
                    pass
        
        # Конвертируем размер в читаемый формат
        size = stats['total_size']
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0 or unit == 'GB':
                stats['size_str'] = f"{size:.1f} {unit}"
                break
            size /= 1024.0
        
        return stats
    
    def ask_output_destination(self, line_count: int) -> str:
        """Спрашивает пользователя куда выводить результат"""
        print(f"\n📊 Найдено {line_count} строк в выводе")
        
        if line_count <= self.max_console_lines:
            print("1. Вывести в консоль")
            print("2. Сохранить в файл")
            print("3. И то, и другое")
            
            while True:
                choice = input("\nВаш выбор (1-3): ").strip()
                if choice in ['1', '2', '3']:
                    break
                print("Пожалуйста, введите 1, 2 или 3")
            
            if choice == '1':
                return 'console'
            elif choice == '2':
                filename = input("Введите имя файла: ").strip()
                return filename
            else:  # choice == '3'
                filename = input("Введите имя файла: ").strip()
                return f"both:{filename}"
        else:
            print(f"Слишком много строк ({line_count}) для вывода в консоль")
            filename = input("Введите имя файла для сохранения: ").strip()
            return filename
    
    def save_to_file(self, content: str, filename: str):
        """Сохраняет результат в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Результат сохранен в {filename}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении файла: {e}")
    
    def run(self):
        """Основной метод запуска скрипта"""
        args = self.parse_arguments()
        
        # Устанавливаем параметры
        self.recursive = args.recursive
        self.show_files = args.files
        self.excluded_dirs = set(args.exclude)
        self.output_file = args.output
        
        # Проверяем путь
        path = Path(args.path).resolve()
        if not path.exists():
            print(f"❌ Ошибка: путь '{path}' не существует")
            sys.exit(1)
        
        if not path.is_dir():
            print(f"❌ Ошибка: '{path}' не является директорией")
            sys.exit(1)
        
        # Генерируем дерево
        print(f"🔍 Анализируем: {path}")
        
        # Получаем статистику
        if self.recursive:
            stats = self.get_summary_stats(path)
            print(f"📈 Статистика: {stats['directories']} папок, {stats['files']} файлов, {stats['size_str']}")
        
        # Генерируем дерево
        tree_lines = self.generate_tree(path)
        
        # Добавляем заголовок
        result = []
        result.append("=" * 60)
        result.append(f"📁 ФАЙЛОВАЯ СТРУКТУРА: {path}")
        result.append("=" * 60)
        result.append(f"Рекурсивно: {'✅' if self.recursive else '❌'}")
        result.append(f"Показывать файлы: {'✅' if self.show_files else '❌'}")
        if self.excluded_dirs:
            result.append(f"Исключенные папки: {', '.join(self.excluded_dirs)}")
        result.append("=" * 60)
        result.append("")
        result.extend(tree_lines)
        result.append("")
        result.append("=" * 60)
        result.append("✅ Граф файловой структуры готов!")
        result.append("")
        
        final_output = "\n".join(result)
        line_count = len(tree_lines)
        
        # Определяем куда выводить результат
        output_dest = None
        
        if self.output_file:
            # Файл указан через флаг
            self.save_to_file(final_output, self.output_file)
        else:
            # Спрашиваем пользователя
            output_dest = self.ask_output_destination(line_count)
            
            if output_dest == 'console':
                print("\n" + final_output)
            elif output_dest.startswith('both:'):
                filename = output_dest[5:]
                print("\n" + final_output)
                self.save_to_file(final_output, filename)
            else:
                self.save_to_file(final_output, output_dest)

def main():
    """Точка входа"""
    try:
        generator = FileTreeGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Операция прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
