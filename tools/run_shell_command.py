from parent_classes.tool import Tool
import subprocess
import shlex

class RunShellCommand(Tool):
    name = "run_shell_command"
    description = "Executes a shell command. Some dangerous commands are banned for security."
    parameters = {
        "command": "Shell command to execute"
    }
    
    BANNED_COMMANDS = [
        "rm -rf /",
        "rm -rf /*",
        ":(){ :|:& };:",  # Fork bomb
        "dd if=/dev/zero",
        "mkfs",
        "format",
        "fdisk",
        "shutdown",
        "reboot",
        "halt",
        "poweroff",
        "init 0",
        "init 6",
        "killall",
        "pkill -9",
        "kill -9",
        "chmod 777 /",
        "chown -R",
        "passwd",
        "su -",
        "sudo su",
        "nc -l",  # netcat listener
        "python -m http.server",
        "python3 -m http.server",
        "> /dev/sda",
        "> /dev/sdb",
        "curl | sh",
        "wget | sh",
        "eval",
        "exec"
    ]
    
    @staticmethod
    def _is_command_banned(command):
        command_lower = command.lower().strip()
        
        for banned in RunShellCommand.BANNED_COMMANDS:
            if banned.lower() in command_lower:
                return True
                
        dangerous_patterns = [
            "rm -rf",
            "/dev/sd",
            "/dev/hd",
            ">/dev/",
            "| sh",
            "| bash",
            "&& rm",
            "; rm",
            "curl.*|.*sh",
            "wget.*|.*sh"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                return True
                
        return False
    
    @staticmethod
    def run(command):
        # Security check
        if RunShellCommand._is_command_banned(command):
            return {
                "status": "error", 
                "message": "Command contains banned/dangerous operations and cannot be executed."
            }
        
        risky_patterns = ["rm ", "mv ", "cp ", "chmod ", "chown ", "sudo ", "git reset --hard"]
        is_risky = any(pattern in command.lower() for pattern in risky_patterns)
        
        if is_risky:
            print(f"\033[91mLLM is requesting to run this potentially risky command: {command}\033[0m")
            confirmation = ""
            while confirmation not in ["yes", "no"]:
                confirmation = input("Do you want to execute this command? (yes/no): ")
            
            if confirmation == "no":
                return {"status": "denied", "message": "Command execution was denied by user."}
        
        try:
            args = shlex.split(command)
            
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                check=False
            )
            
            return {
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": "Command timed out after 30 seconds."
            }
        except FileNotFoundError:
            return {
                "status": "error", 
                "message": f"Command not found: {args[0] if args else command}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing command: {str(e)}"
            }
