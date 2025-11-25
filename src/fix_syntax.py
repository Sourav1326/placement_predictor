#!/usr/bin/env python3
"""Fix the syntax error in industry_flask_app.py line 508"""

def fix_syntax_error():
    try:
        with open('industry_flask_app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the broken f-string on line 508
        # The broken pattern: 'message': f'Training error: {str(e)}'})
        # Should be: 'message': f'Training error: {str(e)}'})
        
        # Look for the specific broken pattern and fix it
        broken_pattern = "'message': f'Training error: {str(e)}')"
        fixed_pattern = "'message': f'Training error: {str(e)}'})"
        
        if broken_pattern in content:
            content = content.replace(broken_pattern, fixed_pattern)
            print(f"Fixed broken pattern: {broken_pattern}")
        else:
            print("Pattern not found, trying alternative fixes...")
            # Alternative: Look for the specific broken line structure
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "Training error" in line and "message" in line and "')" in line and "'})" not in line:
                    print(f"Found problematic line {i+1}: {repr(line)}")
                    # Fix missing closing brace
                    if line.endswith("')"):
                        lines[i] = line[:-2] + "'})"
                        print(f"Fixed to: {repr(lines[i])}")
                        content = '\n'.join(lines)
                        break
        
        # Write the fixed content back
        with open('industry_flask_app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("File has been fixed!")
        
        # Test the syntax
        try:
            compile(content, 'industry_flask_app.py', 'exec')
            print("✓ Syntax check passed!")
        except SyntaxError as e:
            print(f"✗ Syntax error still exists: {e}")
            
    except Exception as e:
        print(f"Error fixing file: {e}")

if __name__ == "__main__":
    fix_syntax_error()