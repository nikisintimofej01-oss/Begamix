import sys
import re
from bgmx_parser import parse_gtwrite

def generate_cpp(nodes, code_text):
    cpp_code = [
        "#include <iostream>",
        "#include <string>",
        "",
        "int main() {",
        "    std::cout << \"[Begamix Runtime Started]\" << std::endl;",
        ""
    ]
    
    # Ищем команды в тексте файла (вместо использования AST)
    for line in code_text.split('\n'):
        line = line.strip()
        
        # 1. Вывод: bgmx.bxprint: <<"текст">>: bgmx.print.end
        match_print = re.match(r'bgmx\.bxprint:\s*<<(.*?)>>:\s*bgmx\.print\.end', line)
        if match_print:
            text = match_print.group(1).strip('"')
            cpp_code.append(f'    std::cout << "{text}" << std::endl;')
            continue
            
        # 2. Простой вывод (для теста)
        match_simple = re.match(r'console\.log\.begamix\("(.*)"\)', line)
        if match_simple:
            text = match_simple.group(1)
            cpp_code.append(f'    std::cout << "{text}" << std::endl;')
            continue
            
    cpp_code.append("")
    cpp_code.append("    return 0;")
    cpp_code.append("}")
    return "\n".join(cpp_code)

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    filename = sys.argv[1]
    
    with open(filename, 'r', encoding='utf-8') as f:
        code_text = f.read()
        
    nodes = parse_gtwrite(filename)
    cpp_code = generate_cpp(nodes, code_text)
    
    out_filename = filename.replace('.bgmx', '_generated.cpp')
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(cpp_code)
    print(f"\033[92mSuccessfully Operation — Generated C++ for {filename}!\033[0m")
