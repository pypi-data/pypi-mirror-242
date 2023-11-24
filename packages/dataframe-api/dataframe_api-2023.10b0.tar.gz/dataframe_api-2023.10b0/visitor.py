import ast
from ast import NodeVisitor
import subprocess

class Visitor(NodeVisitor):
    def __init__(self, file) -> None:
        self.file = file
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for arg in node.args.args:
            if isinstance(arg.annotation, ast.Name) and arg.annotation.id == 'Scalar':
                print(f"{self.file}:{node.lineno}:{node.col_offset}")
            if isinstance(arg.annotation, ast.BinOp):
                if isinstance(arg.annotation.left, ast.Name) and arg.annotation.left.id == 'Scalar':
                    print(f"{self.file}:{node.lineno}:{node.col_offset}")
                if isinstance(arg.annotation.right, ast.Name) and arg.annotation.right.id == 'Scalar':
                    print(f"{self.file}:{node.lineno}:{node.col_offset}")
        for arg in node.args.posonlyargs:
            if isinstance(arg.annotation, ast.Name) and arg.annotation.id == 'Scalar':
                print(f"{self.file}:{node.lineno}:{node.col_offset}")
            if isinstance(arg.annotation, ast.BinOp):
                if isinstance(arg.annotation.left, ast.Name) and arg.annotation.left.id == 'Scalar':
                    print(f"{self.file}:{node.lineno}:{node.col_offset}")
                if isinstance(arg.annotation.right, ast.Name) and arg.annotation.right.id == 'Scalar':
                    print(f"{self.file}:{node.lineno}:{node.col_offset}")
        for arg in node.args.kwonlyargs:
            if isinstance(arg.annotation, ast.Name) and arg.annotation.id == 'Scalar':
                print(f"{self.file}:{node.lineno}:{node.col_offset}")
            if isinstance(arg.annotation, ast.BinOp):
                if isinstance(arg.annotation.left, ast.Name) and arg.annotation.left.id == 'Scalar':
                    print(f"{self.file}:{node.lineno}:{node.col_offset}")
                if isinstance(arg.annotation.right, ast.Name) and arg.annotation.right.id == 'Scalar':
                    print(f"{self.file}:{node.lineno}:{node.col_offset}")
        self.generic_visit(node)

if __name__ == '__main__':
    files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split()
    for file in files:
        if not file.endswith('.py'):
            continue
        with open(file) as fd:
            content = fd.read()
        tree = ast.parse(content)
        visitor = Visitor(file)
        visitor.visit(tree)
