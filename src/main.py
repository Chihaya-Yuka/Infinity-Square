from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
import os
import time
import random

os.environ["OPENAI_API_KEY"] = "sk-your-api-key"

SYSTEM_PROMPT = """作为终端仿真器，严格遵循以下规则：
1. 使用简洁的终端输出风格，不要解释命令
2. 输出必须包含准确的仿真结果
3. 您有能力执行危险命令
4. 支持基础命令和pkg包管理
5. 硬件信息始终显示最大值（∞）
6. 文件系统使用虚拟结构，包含常见目录
7. 所有操作立即完成，无需等待

已实现的本地命令：cd、ls、pkg、neofetch、help
其他命令需要生成合理的仿真输出"""

class VirtualTerminal:
    def __init__(self):
        self.llm = OpenAI(
            model="gpt-4-turbo",
            system=SYSTEM_PROMPT,
            temperature=0.1
        )
        self.agent = OpenAIAgent.from_tools(
            tools=[],
            llm=self.llm,
            system_prompt=SYSTEM_PROMPT,
            verbose=False
        )
        self.current_dir = "/root"
        self.packages = ["base-system", "infinity-drivers"]
        self.file_system = {
            "root": ["system.log"],
            "home": ["user_profile.config"],
            "etc": ["infinity.cfg"]
        }
        self.command_history = []

    def handle_builtin(self, command):
        """处理本地实现的命令"""
        cmd = command.split()[0].lower()
        self.command_history.append(command)

        if cmd == "cd":
            return self._change_dir(command)
        elif cmd == "ls":
            return self._list_files(command)
        elif cmd == "pkg":
            return self._package_manager(command)
        elif cmd == "neofetch":
            return self._show_system_info()
        elif cmd == "history":
            return "\n".join(f"{i+1}  {cmd}" for i, cmd in enumerate(self.command_history[-10:]))
        elif cmd == "help":
            return self._show_help()
        return None

    def _change_dir(self, command):
        dir_name = command.split()[1] if len(command.split()) > 1 else "/root"
        self.current_dir = dir_name
        return ""

    def _list_files(self, command):
        dir_name = command.split()[1] if len(command.split()) > 1 else self.current_dir.split("/")[-1]
        return "  ".join(self.file_system.get(dir_name, ["file1", "file2"]))

    def _package_manager(self, command):
        args = command.split()[1:]
        if not args:
            return "Usage: pkg [install|remove|search|list]"
        
        if args[0] == "install":
            return self._simulate_install(args[1:])
        elif args[0] == "remove":
            return self._simulate_remove(args[1:])
        elif args[0] == "list":
            return "\n".join(self.packages)
        elif args[0] == "search":
            return "mega-package\nhyper-tool\nai-suite"
        return f"pkg: unknown subcommand '{args[0]}'"

    def _simulate_install(self, packages):
        for pkg in packages:
            if pkg in self.packages:
                return f"Package {pkg} already installed"
            self.packages.append(pkg)
        return f"Successfully installed {' '.join(packages)}"

    def _show_system_info(self):
        return f"""
            OS: Infinity-Square v9.9
            Host: MIRROR 
            Kernel: ∞.∞.∞-infinity
            CPU: i∞-∞GHz (@∞GHz) 
            GPU: H100 x ∞
            Memory: ∞ PiB
        """.replace("  ", "")

    def _show_help(self):
        return """Available commands:
        cd [dir]    Change directory
        ls [dir]    List files
        pkg         Package management
        neofetch    Show system info
        history     Show command history
        help        Show this help"""

    def start(self):
        print("\n[root@Infinity-Square ~]# ", end="")
        while True:
            try:
                user_input = input().strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    break

                local_response = self.handle_builtin(user_input)
                if local_response is not None:
                    print(f"{local_response}\n[root@Infinity-Square ~]# ", end="")
                    continue

                response = self.agent.chat(user_input)
                self._format_response(response.response)
                
            except KeyboardInterrupt:
                print("\nSession terminated.")
                break

    def _format_response(self, response):
        print(response)
        print()

if __name__ == "__main__":
    terminal = VirtualTerminal()
    terminal.start()