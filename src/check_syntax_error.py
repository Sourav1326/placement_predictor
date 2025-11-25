#!/usr/bin/env python3
"""Check syntax error in industry_flask_app.py around line 508"""

def check_lines():
    try:
        with open('industry_flask_app.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("Checking lines around 508...")
        for i in range(505, min(512, len(lines))):
            line_num = i + 1
            line_content = lines[i].rstrip('\n')
            print(f"Line {line_num}: {repr(line_content)}")
        
        print("\nLooking for broken f-string...")
        for i, line in enumerate(lines, 1):
            if "Training error" in line and ("f'" in line or 'f"' in line):
                print(f"Found f-string at line {i}: {repr(line.rstrip())}")
                if i < len(lines):
                    print(f"Next line {i+1}: {repr(lines[i].rstrip())}")
                    
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    check_lines()