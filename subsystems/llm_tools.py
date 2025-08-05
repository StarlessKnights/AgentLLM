from subsystems.tool_functions import search_tools, run_tool, append_to_memory
import json
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

tool_mapping = {
    "search_tools": search_tools,
    "run_tool": run_tool,
    "append_to_memory": append_to_memory,
}

class Tools:
    def __init__(self):
        self.tool_mapping = tool_mapping
        
        print("\033[92mTools initialized successfully\033[0m")

    def run_tool(self, tool_name, **kwargs):
        console.print(
            Panel.fit(
                f"[bold blue]🔧 Running Tool:[/] [cyan]{tool_name}[/cyan]",
                border_style="blue",
            )
        )

        # Pretty print arguments as table
        if kwargs:
            arg_table = Table(title="🔢 Tool Arguments", box=box.SIMPLE, show_edge=False)
            arg_table.add_column("Key", style="green", no_wrap=True)
            arg_table.add_column("Value", style="white")
            for key, value in kwargs.items():
                arg_table.add_row(str(key), str(value))
            console.print(arg_table)
        else:
            console.print("[italic]No arguments provided.[/italic]")

        try:
            result = self.tool_mapping[tool_name](**kwargs)
        except KeyError:
            error_msg = f"[red]❌ Error:[/] Invalid tool name: [bold]{tool_name}[/bold]"
            console.print(Panel(error_msg, border_style="red"))
            return {"status": "error", "message": "Invalid tool name"}

        # Output result
        result_display = str(result).strip() if result else "[dim]No result returned.[/dim]"
        console.print(
            Panel.fit(
                result_display,
                title="✅ Tool Result",
                title_align="left",
                border_style="green",
            )
        )

        console.print("\n")
        return result

    def interpret_response(self, response):
        # remove assistant from the beginning of the response
        # response = response.strip()
        # if response.startswith("assistant"):
        #     response = response[len("assistant"):].strip()
        try:
            tool_call = response.choices[0].message.tool_calls[0] # type: ignore
        except:
            return None, None

        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        return function_name, function_args