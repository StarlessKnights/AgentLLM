

tool_descriptions = [
    {
        "type": "function",
        "function": {
            "name": "search_tools",
            "description": (
                "Searches a large database tools related to a general query"
                "query: The query to search for"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_tool",
            "description": (
                "Runs the given tool"
                "tool_id: The ID of the tool to run"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tool_id": {"type": "string"},
                    "kwargs": {"type": "object"}
                },
                "required": ["tool_id", "kwargs"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_to_memory",
            "description": (
                "Appends the given text to memory"
                "text: The text to append to memory"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        }
    }
]