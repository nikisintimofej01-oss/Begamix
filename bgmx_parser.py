import re
import sys

def parse_gtwrite(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nodes = []
    print(f"Читаю файл: {filename} ({len(lines)} строк)")

    for line_num, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('//') or line.startswith('cm!'):
            continue

        # 1. Объявление функции: fun name()
        match_fun = re.match(r'fun\s+(\w+)\(', line)
        if match_fun:
            nodes.append({'type': 'FuncDecl', 'name': match_fun.group(1)})
            continue

        # 2. Объявление переменной (любой): bgmx.var.* или короткое (g:, p: и т.д.)
        # Универсальный паттерн: ищем "var", потом "=" и значение
        match_var = re.search(r'var\.\w+:.*?<<(.*?)>>:', line)
        if not match_var:
            # Пробуем короткие формы (g:, p: и т.д.)
            match_var = re.search(r'(?:g|p|t|l|d):.*?<<(.*?)>>:', line)
            
        if match_var:
            expr = match_var.group(1).strip()
            # Убираем пробелы вокруг "="
            expr = re.sub(r'\s*=\s*', '=', expr)
            if '=' in expr:
                name, val = expr.split('=', 1)
                nodes.append({'type': 'VarDecl', 'name': name, 'value': val})
            continue

        # 3. Вывод: bgmx.bxprint или подобное
        match_print = re.search(r'bxprint:.*?<<(.*?)>>:', line)
        if match_print:
            nodes.append({'type': 'Print', 'value': match_print.group(1)})
            continue

        # 4. Возврат: bex.to.me
        if line.startswith('bex.to.me'):
            nodes.append({'type': 'Return'})
            continue

        # 5. Условия и циклы (пока просто пропускаем, чтобы не ломать парсинг)
        if line.startswith('bgmx.anon') or line.startswith('while') or line.startswith('bgmx.to.ef'):
            nodes.append({'type': 'ControlFlow'})
            continue

        # 6. Любая другая команда bgmx.* или bex.*
        if line.startswith('bgmx.') or line.startswith('bex.'):
            nodes.append({'type': 'GenericCmd', 'cmd': line})
            continue

    print(f"\033[92mSuccessfully Operation — Распарсено {len(nodes)} узлов!\033[0m")
    return nodes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bgmx_parser.py <file.bgmx>")
        sys.exit(1)
    
    nodes = parse_gtwrite(sys.argv[1])
    
    # Выведем первые 10 узлов для проверки
    print("\nПервые 10 узлов:")
    for node in nodes[:10]:
        print(node)
