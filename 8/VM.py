import os
import sys

class Parser:
    """負責讀取並解析單一 .vm 檔案的每一行指令"""
    ARITHMETIC_COMMANDS = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}

    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self.commands = []
        for line in lines:
            # 去除註解與前後空白
            clean_line = line.split('//')[0].strip()
            if clean_line:
                self.commands.append(clean_line)
        self.current_index = -1
        self.current_command = None

    def has_more_commands(self):
        return self.current_index + 1 < len(self.commands)

    def advance(self):
        self.current_index += 1
        self.current_command = self.commands[self.current_index]

    def command_type(self):
        tokens = self.current_command.split()
        cmd = tokens[0]
        if cmd in self.ARITHMETIC_COMMANDS:
            return 'C_ARITHMETIC'
        elif cmd == 'push':
            return 'C_PUSH'
        elif cmd == 'pop':
            return 'C_POP'
        elif cmd == 'label':
            return 'C_LABEL'
        elif cmd == 'goto':
            return 'C_GOTO'
        elif cmd == 'if-goto':
            return 'C_IF'
        elif cmd == 'function':
            return 'C_FUNCTION'
        elif cmd == 'return':
            return 'C_RETURN'
        elif cmd == 'call':
            return 'C_CALL'
        raise ValueError(f"未知的指令: {self.current_command}")

    def arg1(self):
        tokens = self.current_command.split()
        if self.command_type() == 'C_ARITHMETIC':
            return tokens[0]
        return tokens[1]

    def arg2(self):
        tokens = self.current_command.split()
        return int(tokens[2])


class CodeWriter:
    """負責將解析後的 VM 指令轉譯為 Hack Assembly (.asm)"""
    SEGMENT_MAP = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT'
    }

    def __init__(self, output_filepath):
        self.file = open(output_filepath, 'w', encoding='utf-8')
        self.filename = ""
        self.current_function = ""
        self.label_counter = 0

    def set_file_name(self, filename):
        self.filename = os.path.splitext(os.path.basename(filename))[0]

    def write(self, lines):
        for line in lines:
            self.file.write(line + '\n')

    def write_init(self):
        """寫入啟動碼 (Bootstrap Code): 設定 SP=256 並呼叫 Sys.init"""
        self.write([
            "// Bootstrap code",
            "@256",
            "D=A",
            "@SP",
            "M=D"
        ])
        self.write_call("Sys.init", 0)

    def write_arithmetic(self, command):
        self.write([f"// {command}"])
        if command in ('add', 'sub', 'and', 'or'):
            op = {'add': '+', 'sub': '-', 'and': '&', 'or': '|'}[command]
            self.write([
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                f"M=M{op}D"
            ])
        elif command in ('neg', 'not'):
            op = {'neg': '-', 'not': '!'}[command]
            self.write([
                "@SP",
                "A=M-1",
                f"M={op}M"
            ])
        elif command in ('eq', 'gt', 'lt'):
            jmp = {'eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}[command]
            true_label = f"TRUE_{self.label_counter}"
            end_label = f"END_{self.label_counter}"
            self.label_counter += 1
            self.write([
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@{true_label}",
                f"D;{jmp}",
                "@SP",
                "A=M-1",
                "M=0",
                f"@{end_label}",
                "0;JMP",
                f"({true_label})",
                "@SP",
                "A=M-1",
                "M=-1",
                f"({end_label})"
            ])

    def write_push_pop(self, command, segment, index):
        self.write([f"// {command} {segment} {index}"])
        if command == 'C_PUSH':
            if segment == 'constant':
                self.write([f"@{index}", "D=A"])
            elif segment in self.SEGMENT_MAP:
                base = self.SEGMENT_MAP[segment]
                self.write([f"@{index}", "D=A", f"@{base}", "A=M+D", "D=M"])
            elif segment == 'temp':
                self.write([f"@{5 + index}", "D=M"])
            elif segment == 'pointer':
                ptr = 'THIS' if index == 0 else 'THAT'
                self.write([f"@{ptr}", "D=M"])
            elif segment == 'static':
                self.write([f"@{self.filename}.{index}", "D=M"])
            
            # 將 D 推入堆疊頂端並 SP++
            self.write([
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ])

        elif command == 'C_POP':
            if segment in self.SEGMENT_MAP:
                base = self.SEGMENT_MAP[segment]
                self.write([
                    f"@{index}",
                    "D=A",
                    f"@{base}",
                    "D=M+D",
                    "@R13",
                    "M=D",
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    "@R13",
                    "A=M",
                    "M=D"
                ])
            elif segment == 'temp':
                self.write([
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    f"@{5 + index}",
                    "M=D"
                ])
            elif segment == 'pointer':
                ptr = 'THIS' if index == 0 else 'THAT'
                self.write([
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    f"@{ptr}",
                    "M=D"
                ])
            elif segment == 'static':
                self.write([
                    "@SP",
                    "AM=M-1",
                    "D=M",
                    f"@{self.filename}.{index}",
                    "M=D"
                ])

    def write_label(self, label):
        self.write([f"({self.current_function}${label})"])

    def write_goto(self, label):
        self.write([
            f"// goto {label}",
            f"@{self.current_function}${label}",
            "0;JMP"
        ])

    def write_if(self, label):
        self.write([
            f"// if-goto {label}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self.current_function}${label}",
            "D;JNE"
        ])

    def write_function(self, function_name, num_locals):
        self.current_function = function_name
        self.write([f"// function {function_name} {num_locals}", f"({function_name})"])
        for _ in range(num_locals):
            self.write_push_pop('C_PUSH', 'constant', 0)

    def write_call(self, function_name, num_args):
        return_label = f"{function_name}$ret.{self.label_counter}"
        self.label_counter += 1
        self.write([f"// call {function_name} {num_args}"])

        # 1. Push return-address
        self.write([f"@{return_label}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
        # 2. Push LCL, ARG, THIS, THAT
        for reg in ('LCL', 'ARG', 'THIS', 'THAT'):
            self.write([f"@{reg}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
        # 3. ARG = SP - num_args - 5
        self.write([
            "@SP",
            "D=M",
            f"@{num_args + 5}",
            "D=D-A",
            "@ARG",
            "M=D"
        ])
        # 4. LCL = SP
        self.write(["@SP", "D=M", "@LCL", "M=D"])
        # 5. goto function_name
        self.write([f"@{function_name}", "0;JMP"])
        # 6. (return-address)
        self.write([f"({return_label})"])

    def write_return(self):
        self.write([
            "// return",
            # FRAME (R13) = LCL
            "@LCL",
            "D=M",
            "@R13",
            "M=D",
            # RET (R14) = *(FRAME - 5)
            "@5",
            "A=D-A",
            "D=M",
            "@R14",
            "M=D",
            # *ARG = pop()
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            # SP = ARG + 1
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D"
        ])
        # 還原 THAT, THIS, ARG, LCL
        for offset, reg in enumerate(['THAT', 'THIS', 'ARG', 'LCL'], start=1):
            self.write([
                "@R13",
                "D=M",
                f"@{offset}",
                "A=D-A",
                "D=M",
                f"@{reg}",
                "M=D"
            ])
        # goto RET
        self.write(["@R14", "A=M", "0;JMP"])

    def close(self):
        self.file.close()


def translate_file(filepath, code_writer):
    parser = Parser(filepath)
    code_writer.set_file_name(filepath)
    while parser.has_more_commands():
        parser.advance()
        ctype = parser.command_type()
        if ctype == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif ctype in ('C_PUSH', 'C_POP'):
            code_writer.write_push_pop(ctype, parser.arg1(), parser.arg2())
        elif ctype == 'C_LABEL':
            code_writer.write_label(parser.arg1())
        elif ctype == 'C_GOTO':
            code_writer.write_goto(parser.arg1())
        elif ctype == 'C_IF':
            code_writer.write_if(parser.arg1())
        elif ctype == 'C_FUNCTION':
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif ctype == 'C_CALL':
            code_writer.write_call(parser.arg1(), parser.arg2())
        elif ctype == 'C_RETURN':
            code_writer.write_return()


def main():
    if len(sys.argv) != 2:
        print("用法: python VMTranslator.py <檔案路徑.vm 或 資料夾路徑>")
        sys.exit(1)

    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        dir_name = os.path.basename(os.path.normpath(input_path))
        output_path = os.path.join(input_path, f"{dir_name}.asm")
        vm_files = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.endswith('.vm')
        ]
        writer = CodeWriter(output_path)
        # 多檔案專案（如 FibonacciElement, StaticsTest）需要寫入 Bootstrap Code
        writer.write_init()
        for vm_file in vm_files:
            translate_file(vm_file, writer)
        writer.close()
    elif os.path.isfile(input_path) and input_path.endswith('.vm'):
        output_path = os.path.splitext(input_path)[0] + '.asm'
        writer = CodeWriter(output_path)
        # 單一測試檔（如 BasicTest, SimpleAdd）通常由測試腳本自行初始化 SP，不需 Bootstrap
        translate_file(input_path, writer)
        writer.close()
    else:
        print("請提供有效的 .vm 檔案或包含 .vm 檔案的資料夾。")
        sys.exit(1)

    print(f"轉譯完成！輸出檔案：{output_path}")


if __name__ == '__main__':
    main()
