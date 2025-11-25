"""
Analyze all Python files to extract dependencies
"""
import ast
import os
import sys

def extract_imports(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        
        return imports
    except Exception as e:
        print(f'Skipping {file_path}: {str(e)[:50]}...')
        return set()

# Get all Python files
python_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and not file.startswith('__'):
            python_files.append(os.path.join(root, file))

all_imports = set()
for file_path in python_files:
    imports = extract_imports(file_path)
    all_imports.update(imports)

# Filter to external packages (not built-in)
builtin_modules = {
    'sys', 'os', 'json', 'datetime', 'time', 'random', 'math', 'collections',
    'itertools', 'functools', 'operator', 'copy', 'pickle', 'sqlite3', 
    'urllib', 'http', 'email', 'html', 'xml', 'csv', 'configparser',
    'logging', 'threading', 'multiprocessing', 'subprocess', 'shutil',
    'tempfile', 'pathlib', 'glob', 're', 'string', 'textwrap', 'unicodedata',
    'difflib', 'hashlib', 'hmac', 'secrets', 'ssl', 'socket', 'ipaddress',
    'base64', 'binascii', 'struct', 'codecs', 'io', 'typing', 'enum',
    'dataclasses', 'abc', 'contextlib', 'warnings', 'weakref', 'gc',
    'inspect', 'importlib', 'pkgutil', 'modulefinder', 'ast', 'dis',
    'traceback', 'pdb', 'profile', 'pstats', 'timeit'
}

external_imports = sorted([imp for imp in all_imports if imp not in builtin_modules])

print("External dependencies found:")
for imp in external_imports:
    print(f"  {imp}")

print(f"\nTotal external dependencies: {len(external_imports)}")