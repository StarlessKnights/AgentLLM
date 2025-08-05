import hashlib
import time
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_file = None
        self.session_id = None
        print("\033[92m✅ Logger initialized successfully\033[0m")

    def setup(self, current_date=None, model="Unknown"):
        if not current_date:
            current_date = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        timestamp = str(time.time())
        self.session_id = hashlib.md5((current_date + timestamp).encode()).hexdigest()[:12]

        file_path = f"logs/log-{current_date}.md"
        self.log_file = open(file_path, "w", encoding="utf-8")

        self._writeln(f"# 🧾 Session ID: `{self.session_id}`")
        self._writeln(f"**🕒 Timestamp:** {current_date}")
        self._writeln(f"**🤖 Model:** {model}")
        self._writeln("---")

    def _writeln(self, line=""):
        self.log_file.write(line + "\n")
        self.log_file.flush()

    def log_user_prompt(self, message):
        self._writeln("### 🙋‍♂️ User Prompt")
        self._writeln(f"> {message}\n")

    def log_tool_call(self, tool_name, args):
        self._writeln(f"### 🧰 Tool Call: `{tool_name}`")
        self._writeln("**Arguments:**")
        for key, value in args.items():
            self._writeln(f"- `{key}`: {value}")
        self._writeln()

    def log_tool_result(self, result):
        self._writeln("### 📦 Tool Result")
        self._writeln("```text")
        self._writeln(result.strip())
        self._writeln("```\n")

    def log_model_response(self, response):
        self._writeln("### 🤖 Model Response")
        self._writeln("```text")
        self._writeln(response.strip())
        self._writeln("```\n")

    def log_memory_context(self, context):
        self._writeln("### 🧠 Memory Context")
        self._writeln("```text")
        self._writeln(context.strip())
        self._writeln("```\n")

    def close(self):
        if self.log_file:
            self._writeln(f"_End of session `{self.session_id}`_")
            self.log_file.close()
            self.log_file = None
