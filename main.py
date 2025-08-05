from subsystems.llm import LLM
from subsystems.llm_tools import Tools
from subsystems.tool_descriptions import tool_descriptions
from subsystems.messages import Messages
from subsystems.loading_icon import LoadingIndicator
from subsystems.logger import Logger
from subsystems.memory import Memory
import json
from enum import Enum
import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()

class Models(Enum):
    PHI4 = "phi-4"
    QWEN3 = "qwen-3"

llm = LLM()
tools = Tools()
loading_icon = LoadingIndicator()
logger = Logger()
messages = Messages()
memory = Memory()

current_datetime = datetime.datetime.now()
model = Models.PHI4.value
logger.setup(current_datetime.strftime("%Y-%m-%d %H:%M:%S"), model)

def run_it(prompt = None):
    global llm, tools, messages, logger, memory

    if prompt is None:
        prompt = Prompt.ask("[bold green]>[/bold green]").strip()
    else:
        prompt = prompt.strip()

    if prompt.strip() == "//r":  # reset memory
        messages = Messages()
        return
    elif prompt.strip() == "//b": # bye
        print("Exiting...")
        exit(0)

    messages.add_message("user", prompt)
    logger.log_user_prompt(prompt)

    context = memory.query(prompt)
    formatted_context = "Memory Context: " + context if context else "No relevant memory found."
    messages.add_message("system", formatted_context)
    logger.log_memory_context(context if context else "No relevant memory found.")

    content = Text(formatted_context.replace("Memory Context: ", ""), style="dim" if not context else "white")

    console.print(
        Panel.fit(
            content,
            title="🧠 Memory Context",
            title_align="left",
            border_style="cyan" if context else "grey50"
        )
    )

    function_name = None
    function_args: dict[str, object | None] = {}

    while True:
        function_name = None
        function_args = None

        try:
            response = llm.generate(
                messages=messages.messages,
                streaming=True,
                tools=tool_descriptions,
            )
        except Exception as e:
            logger._writeln(f"Error generating response: {str(e)}")
            print(f"Error: {str(e)}")
            exit(1)

        full_content = ""
        spinner_active = True

        # Start the spinner outside the streaming loop
        with console.status("[bold green]Thinking...[/bold green]", spinner="aesthetic") as status:
            # stream the response
            for chunk in response:
                if chunk.choices[0].finish_reason is not None:
                    break

                if chunk.choices[0].delta.tool_calls:
                    # Stop spinner when we start showing function calls
                    if spinner_active:
                        status.stop()
                        spinner_active = False
                    
                    # Initialize or update function details
                    if function_name is None:
                        function_name = chunk.choices[0].delta.tool_calls[0].function.name or ""
                        function_args = ""

                        console.print(f"[bold blue]Calling function:[/bold blue] {function_name}")
                        print("Arguments: ", end="", flush=True)

                    if chunk.choices[0].delta.tool_calls[0].function.arguments:
                        arg_chunk = chunk.choices[0].delta.tool_calls[0].function.arguments
                        function_args += arg_chunk
                        print(arg_chunk, end="", flush=True)

                    if function_args:
                        try:
                            function_args = json.loads(function_args)
                            break
                        except json.JSONDecodeError:
                            pass
                    continue

                content = chunk.choices[0].delta.content
                if content:

                    if spinner_active:
                        status.stop()
                        spinner_active = False
                    
                    print(content, end="", flush=True)
                    full_content += content

        if full_content:
            logger.log_model_response(full_content.strip())
        print()

        if not function_name:
            break

        try:
            result = tools.run_tool(function_name, **function_args)
        except Exception as e:
            logger._writeln(f"Error running tool {function_name}: {str(e)}")
            messages.add_message("system", f"Error running tool {function_name}: {str(e)}")
            error_message = f"Error running tool {function_name}: {str(e)}"
            console.print(f"[bold red]Error:[/bold red] {error_message}")
            continue
        logger.log_tool_call(function_name, function_args)
        logger.log_tool_result(json.dumps(result, indent=2))

        messages.add_task_description(function_name, function_args, result)

if __name__ == "__main__":
    while True:
        try:
            run_it()
        except KeyboardInterrupt:
            print("\nExiting...")
            break
