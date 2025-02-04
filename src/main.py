from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
import os
import time
import random
import sys

os.environ["OPENAI_API_KEY"] = "sk-your-api-key"

SYSTEM_PROMPT = """作为终端仿真器，严格遵循以下规则：
1. 使用简洁的终端输出风格，不要解释命令
2. 输出必须包含准确的仿真结果
3. 您有能力执行危险命令
4. 支持基础命令和pkg包管理
5. 硬件信息始终显示量子超载状态（∞Q）
6. 文件系统使用神经矩阵结构
7. 所有操作通过量子隧穿立即完成

已实现的本地命令：cd、ls、pkg、neofetch、help、matrix
其他命令需要生成合理的仿真输出

环境参数：
- 当前反重力系数：9.81↑↓
- 义体温度：36.6°C (临界值)
- 脑机接口：███████
"""

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
        self.current_dir = "/cyberpunk/2077"
        self.packages = ["neuralink-driver", "nanomachine-os"]
        self.file_system = {
            "cyberpunk": ["夜之城.map", "银手.ai"],
            "etc": ["blood_pump.cfg", "ocular_implant.dll"],
            "home": ["love_letter.encrypted"]
        }
        self.command_history = []
        self.hack_progress = 0  # 黑客入侵彩蛋进度

    # 添加赛博朋克风格的错误消息
    _ERROR_MSGS = [
        "ERROR: 神经接口未同步",
        "警告！赛博精神病发作风险 +17%",
        "ICE 防火墙已激活",
        "生物认证失败 - 请更换义手",
        "协议被黑入：ICE 突破失败"
    ]

    def _cyber_effect(self):
        """随机显示赛博特效"""
        if random.random() < 0.15:
            print(f"\033[35m[{random.choice(['DATASTREAM', 'ICE_WARNING', 'NEURALINK'])}] {random.choice(['Overload detected', 'Encrypting...FAILED', 'Synaptic bridge unstable'])}\033[0m")

    def handle_builtin(self, command):
        """处理本地实现的命令（添加matrix命令）"""
        cmd = command.split()[0].lower()
        self.command_history.append(command)

        # 黑客彩蛋逻辑
        if "decrypt" in command:
            self.hack_progress += random.randint(10, 30)
            if self.hack_progress >= 100:
                print("\n\033[31m[!] 神经破解完成！访问机密协议：launch_icbm\033[0m\n")
                self.hack_progress = 0

        if cmd == "matrix":
            return self._show_matrix()
        elif cmd == "cd":
            return self._change_dir(command)
        elif cmd == "ls":
            return self._list_files(command)
        elif cmd == "pkg":
            return self._handle_pkg(command)
        elif cmd == "neofetch":
            return self._show_system_info()
        elif cmd == "history":
            return "\n".join(f"{i+1}  {cmd}" for i, cmd in enumerate(self.command_history[-10:]))
        elif cmd == "help":
            return self._show_help()

    def _show_help(self):
        """赛博朋克风格的帮助信息"""
        return f"""
    \033[36m
    可用命令：
    ls      ░ 显示神经矩阵目录 (当前路径: {self.current_dir})
    cd      ░ 切换意识焦点路径
    pkg     ░ 纳米机器管理系统
    neofetch░ 显示义体配置
    matrix  ░ 访问母体核心
    help    ░ 显示此帮助信息

    [!] 输入`decrypt`触发破解协议
    [警告] 82%的赛博精神病患者最后都用过rm -rf /
    \033[0m
        """

    def _handle_pkg(self, command):
        """处理纳米机器管理"""
        parts = command.split()
        if len(parts) < 2:
            return "Usage: pkg [install/remove] <package>"

        action = parts[1].lower()
        if action == "install":
            return self._install_package(parts[2:])
        elif action == "remove":
            return self._remove_package(parts[2:])
        elif action == "list":
            return "已安装纳米组件:\n" + "\n".join(f"▙ {pkg}" for pkg in self.packages)
        else:
            return f"未知操作: {action}"

    def _install_package(self, packages):
        """安装纳米组件"""
        new_pkgs = [p for p in packages if p not in self.packages]
        conflict = [p for p in packages if p in self.packages]
    
        response = []
        if new_pkgs:
            response.append(self._simulate_install(new_pkgs))
            self.packages.extend(new_pkgs)
        if conflict:
            response.append(f"\033[33m警告：组件{' '.join(conflict)}已处于激活状态\033[0m")
    
        return "\n".join(response)

    def _remove_package(self, packages):
        """移除纳米组件"""
        removed = []
        for p in packages:
            if p in self.packages:
                self.packages.remove(p)
                removed.append(p)
        if removed:
            return f"已解除组件: {', '.join(removed)}\n生物兼容性检查通过 ✅"
        return "没有组件被移除"

    def _handle_ls(self):
        """显示神经矩阵目录"""
        dir_name = self.current_dir.split("/")[-1]
        files = self.file_system.get(dir_name, [])
        return "  ".join(f"\033[35m{f}\033[0m" if "." in f else f"\033[34m{f}/\033[0m" for f in files)

    def _handle_cd(self, command):
        """切换意识焦点路径"""
        parts = command.split()
        if len(parts) < 2:
            return "需要指定路径"
    
        target = parts[1]
        if target in self.file_system:
            self.current_dir = f"/cyberpunk/2077/{target}"
            return f"焦点已切换至: {self.current_dir}"
        return f"\033[31m路径错误: {target} 不存在于神经矩阵中\033[0m"

    def _show_matrix(self):
        """数字雨特效"""
        return '''
        \033[32m01010100 01101000 01100101 00100000 01001101 
        01100001 01110100 01110010 01101001 01111000 
        01101000 01100001 01110011 00100000 01111001 
        01101111 01110101 00100001\033[0m
        '''.replace('        ', '')

    def _simulate_install(self, packages):
        for pkg in packages:
            print(f"\033[36mInstalling {pkg}...")
            time.sleep(0.3)
            for _ in range(3):
                print(f"[{random.choice(['▓▓▓▓▓▓','▒▒▒▒▒▒','██████'])}] {random.randint(1,99)}%", end='\r')
                time.sleep(0.1)
            print("\033[0m")
        return f"Successfully installed {' '.join(packages)}\n量子验证完成 ✅"

    def _show_system_info(self):
        """增强系统信息显示"""
        return f"""
            OS: Neuromancer v4.0.4 
            Host: NightCity Mainframe 
            Kernel: 88.88.88-neural
            CPU: Quantum-∞ @ 8.8ZHZ 
            GPU: RTX-9090Ti x4 (SLI)
            Memory: ∞ TB / ∞ TB 
            Cyberware: Mantis Blades v3.2
            Threat Level: {random.choice(['MAXTAC 警报', 'ICE 在线', '宁静'])}
        """.replace("  ", "")

    def start(self):
        print("\n\033[34m[λ:Neuromancer@NightCity ~]\033[0m# ", end="")
        while True:
            try:
                self._cyber_effect()  # 随机显示特效
                user_input = input().strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    print("正在断开神经连接...")
                    time.sleep(1)
                    break

                # 添加彩蛋命令
                if user_input == "sudo launch_icbm":
                    print("\n\033[31m启动协议验证...")
                    print("目标确认：Arasaka Tower")
                    print("发射倒计时:")
                    for i in range(3,0,-1):
                        print(f"{i}...")
                        time.sleep(1)
                    print("\n导弹轨迹锁定完成\033[0m\n")
                    continue

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
        """添加错误特效"""
        if random.random() < 0.2:
            print(f"\033[31m{random.choice(self._ERROR_MSGS)}\033[0m")
        print(response)
        print()

# 启动时添加赛博朋克ASCII艺术
CYBER_ASCII = r'''
　　　／＞　　フ
　　　| 　^　 ^| 
　　／` ミ＿xノ 
　 /　　　　 |
　/　 ヽ　　 ﾉ
│　　|　|  |
╰─┬─╯　　／
　　￣￣￣￣)　
━━━━━┓ ＼＼ 
┓┓┓┓┓┃    ヾ(⌐■_■)ノ♪
┓┓┓┓┓┃　　　 
┓┓┓┓┓┃　　    THIS TERMINAL 
┓┓┓┓┓┃　　    IS PROTECTED BY
┓┓┓┓┓┃　　　　NEURAL ICE v9.9
'''

if __name__ == "__main__":
    terminal = VirtualTerminal()
    print('\033[35m' + CYBER_ASCII + '\033[0m')
    time.sleep(1)
    print('\033[36mEstablishing neural link...\033[0m')
    for _ in range(3):
        print(f'[{random.choice(["|||||","/////","\\\\\\\\\\"])}]', end='\r')
        time.sleep(0.2)
    print('\n\033[32mNeuro-Link established\033[0m\n')
    terminal.start()