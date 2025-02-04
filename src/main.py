from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
import os
import time
import random
import sys

os.environ["OPENAI_API_KEY"] = "sk-your-api-key"

SYSTEM_PROMPT = """As a terminal emulator, strictly follow these rules:
1. Use a concise terminal output style, do not explain commands
2. Output must contain accurate simulation results
3. You have the ability to execute dangerous commands
4. Support basic commands and plugin management
5. Hardware information always shows quantum overload status (∞Q)
6. File system uses neural matrix structure
7. All operations are completed instantly through quantum tunneling

Implemented local commands: cd, ls, plugin, neofetch, help, matrix
Other commands need to generate reasonable simulation output

Environment parameters:
- Current anti-gravity coefficient: 9.81↑↓
- Prosthetic temperature: 36.6°C (critical value)
- Brain-machine interface: ███████
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
        self.plugins = ["neuralink-driver", "nanomachine-os"]
        self.file_system = {
            "cyberpunk": ["night_city.map", "silverhand.ai"],
            "etc": ["blood_pump.cfg", "ocular_implant.dll"],
            "home": ["love_letter.encrypted"]
        }
        self.command_history = []
        self.hack_progress = 0  # Hacking easter egg progress

    # Add cyberpunk style error messages
    _ERROR_MSGS = [
        "ERROR: Neural interface not synchronized",
        "Warning! Cyberpsychosis risk +17%",
        "ICE firewall activated",
        "Biometric authentication failed - please replace prosthetic hand",
        "Protocol hacked: ICE breakthrough failed"
    ]

    def _cyber_effect(self):
        """Randomly display cyber effects"""
        if random.random() < 0.15:
            print(f"\033[35m[{random.choice(['DATASTREAM', 'ICE_WARNING', 'NEURALINK'])}] {random.choice(['Overload detected', 'Encrypting...FAILED', 'Synaptic bridge unstable'])}\033[0m")

    def handle_builtin(self, command):
        """Handle locally implemented commands (add matrix command)"""
        cmd = command.split()[0].lower()
        self.command_history.append(command)

        # Hacking easter egg logic
        if "decrypt" in command:
            self.hack_progress += random.randint(10, 30)
            if self.hack_progress >= 100:
                print("\n\033[31m[!] Neural hack complete! Access secret protocol: launch_icbm\033[0m\n")
                self.hack_progress = 0

        if cmd == "matrix":
            return self._show_matrix()
        elif cmd == "cd":
            return self._change_dir(command)
        elif cmd == "ls":
            return self._list_files(command)
        elif cmd == "plugin":
            return self._handle_plugin(command)
        elif cmd == "neofetch":
            return self._show_system_info()
        elif cmd == "history":
            return "\n".join(f"{i+1}  {cmd}" for i, cmd in enumerate(self.command_history[-10:]))
        elif cmd == "help":
            return self._show_help()

    def _show_help(self):
        """Cyberpunk style help information"""
        return f"""
    \033[36m
    Available commands:
    ls      ░ Display neural matrix directory (current path: {self.current_dir})
    cd      ░ Change focus path
    plugin  ░ Plugin management system
    neofetch░ Display prosthetic configuration
    matrix  ░ Access the core of the Matrix
    help    ░ Display this help information

    [!] Enter `decrypt` to trigger the hacking protocol
    [Warning] 82% of cyberpsychosis patients have used rm -rf /
    \033[0m
        """

    def _handle_plugin(self, command):
        """Handle plugin management"""
        parts = command.split()
        if len(parts) < 2:
            return "Usage: plugin [install/remove] <plugin>"

        action = parts[1].lower()
        if action == "install":
            return self._install_plugin(parts[2:])
        elif action == "remove":
            return self._remove_plugin(parts[2:])
        elif action == "list":
            return "Installed plugins:\n" + "\n".join(f"▙ {plugin}" for plugin in self.plugins)
        else:
            return f"Unknown action: {action}"

    def _install_plugin(self, plugins):
        """Install plugins"""
        new_plugins = [p for p in plugins if p not in self.plugins]
        conflict = [p for p in plugins if p in self.plugins]
    
        response = []
        if new_plugins:
            response.append(self._simulate_install(new_plugins))
            self.plugins.extend(new_plugins)
        if conflict:
            response.append(f"\033[33mWarning: Plugin{' '.join(conflict)} is already active\033[0m")
    
        return "\n".join(response)

    def _remove_plugin(self, plugins):
        """Remove plugins"""
        removed = []
        for p in plugins:
            if p in self.plugins:
                self.plugins.remove(p)
                removed.append(p)
        if removed:
            return f"Removed plugins: {', '.join(removed)}\nBiocompatibility check passed ✅"
        return "No plugins were removed"

    def _list_files(self):
        """Display neural matrix directory"""
        dir_name = self.current_dir.split("/")[-1]
        files = self.file_system.get(dir_name, [])
        return "  ".join(f"\033[35m{f}\033[0m" if "." in f else f"\033[34m{f}/\033[0m" for f in files)

    def _change_dir(self, command):
        """Change focus path"""
        parts = command.split()
        if len(parts) < 2:
            return "Path required"
    
        target = parts[1]
        if target in self.file_system:
            self.current_dir = f"/cyberpunk/2077/{target}"
            return f"Focus switched to: {self.current_dir}"
        return f"\033[31mPath error: {target} does not exist in the neural matrix\033[0m"

    def _show_matrix(self):
        """Digital rain effect"""
        return '''
        \033[32m01010100 01101000 01100101 00100000 01001101 
        01100001 01110100 01110010 01101001 01111000 
        01101000 01100001 01110011 00100000 01111001 
        01101111 01110101 00100001\033[0m
        '''.replace('        ', '')

    def _simulate_install(self, plugins):
        for plugin in plugins:
            print(f"\033[36mInstalling {plugin}...")
            time.sleep(0.3)
            for _ in range(3):
                print(f"[{random.choice(['▓▓▓▓▓▓','▒▒▒▒▒▒','██████'])}] {random.randint(1,99)}%", end='\r')
                time.sleep(0.1)
            print("\033[0m")
        return f"Successfully installed {' '.join(plugins)}\nQuantum verification complete ✅"

    def _show_system_info(self):
        """Enhanced system information display"""
        return f"""
            OS: Neuromancer v4.0.4 
            Host: NightCity Mainframe 
            Kernel: 88.88.88-neural
            CPU: Quantum-∞ @ 8.8ZHZ 
            GPU: RTX-9090Ti x4 (SLI)
            Memory: ∞ TB / ∞ TB 
            Cyberware: Mantis Blades v3.2
            Threat Level: {random.choice(['MAXTAC Alert', 'ICE Online', 'Calm'])}
        """.replace("  ", "")

    def start(self):
        print("\n\033[34m[λ:Neuromancer@NightCity ~]\033[0m# ", end="")
        while True:
            try:
                self._cyber_effect()  # Randomly display effects
                user_input = input().strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    print("Disconnecting neural link...")
                    time.sleep(1)
                    break

                # Add easter egg command
                if user_input == "sudo launch_icbm":
                    print("\n\033[31mLaunching protocol verification...")
                    print("Target confirmed: Arasaka Tower")
                    print("Launch countdown:")
                    for i in range(3,0,-1):
                        print(f"{i}...")
                        time.sleep(1)
                    print("\nMissile trajectory locked\033[0m\n")
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
        """Add error effects"""
        if random.random() < 0.2:
            print(f"\033[31m{random.choice(self._ERROR_MSGS)}\033[0m")
        print(response)
        print()

# Add cyberpunk ASCII art on startup
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