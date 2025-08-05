class Tool:
    name = "Tool"
    description = "This is a tool"
    parameters = {}

    @staticmethod
    def run(*args, **kwargs):
        return {"status": "error", "message": "Tool run method not implemented"}
