from parent_classes.tool import Tool
import re
import os

class GraphEquation(Tool):
    name = "graph_equation"
    description = "exports png of a graph of an equation"
    parameters = {
        "title": "nonoptional title of the graph",
        "equation": "nonoptional equation to graph",
        "open_afterwards": "optional boolean to open the graph after generating",
    }
    
    @staticmethod
    def run(title: str, equation: str, open_afterwards: bool = False):
        def convert_equation(equation: str):
            equation = re.sub(r'^\s*[a-zA-Z]\s*=', '', equation).strip()

            equation = equation.replace('^', '**')
            equation = re.sub(r'(?<![a-zA-Z0-9_])([0-9]+)([a-zA-Z])', r'\1*\2', equation)

            functions = [
                'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan',
                'sinh', 'cosh', 'tanh', 'exp', 'log', 'log10', 'sqrt', 'abs'
            ]
            for func in functions:
                equation = re.sub(rf'\b{func}\b', f'np.{func}', equation)

            equation = re.sub(r'(?<![a-zA-Z0-9_])e(?![a-zA-Z0-9_])', 'np.e', equation)
            equation = re.sub(r'(?<![a-zA-Z0-9_])pi(?![a-zA-Z0-9_])', 'np.pi', equation)

            return equation
    
        equation = convert_equation(equation)

        code = f"""
import matplotlib.pyplot as plt
import numpy as np
import re

x = np.linspace(-10, 10, 100)
y = {equation}
plt.plot(x, y)
plt.title("{title}")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.savefig("graph.png")
"""
        
        if os.path.exists("temp/graph.png"):
            os.remove("temp/graph.png")

        if os.path.exists("temp/graph.py"):
            os.remove("temp/graph.py")

        with open("temp/graph.py", "w") as f:
            f.write(code)

        if not os.path.exists("temp/graph.py"):
            return {"status": "error", "message": "Failed to create python file"}

        os.system(".conda/bin/python temp/graph.py")

        os.remove("temp/graph.py")

        if not os.path.exists("temp/graph.png"):
            return {"status": "error", "message": "Failed to create graph.png file"}
        
        if open_afterwards:
            os.system("open temp/graph.png")

        return {"status": "success", "message": f"Graph generated successfully{' and opened.' if open_afterwards else ''}", "path": "graph.png"}