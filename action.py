import os
import re
import subprocess

def get_ui_file_name(py_file_path):
    with open(py_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    match = re.search(r'# loadUI: (.+\.ui)', content)
    if match:
        return match.group(1)
    else:
        raise ValueError("UI file name not found in the specified Python file.")

def convert_ui_to_py(ui_file_path, output_py_file_path):
    command = f"/usr/bin/pyuic5 {ui_file_path} -o {output_py_file_path}"
    subprocess.run(command, shell=True, check=True)

def format_py_file(py_file_path):
    with open(py_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove the initial comments and import statements (remove 12 lines)
    start_index = 13

    formatted_lines = lines[start_index:]

    # Replace QtWidgets.QAction with qaction
    formatted_lines = [line.replace('QtWidgets.QAction', 'qaction') for line in formatted_lines]

    return ''.join(formatted_lines)

def insert_formatted_code(py_file_path, formatted_code):
    with open(py_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the comment line to insert the formatted code after
    insert_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('# loadUI:'):
            insert_index = i + 1
            break

    new_content = lines[:insert_index] + [formatted_code] + lines[insert_index:]

    return ''.join(new_content)

def main():
    py_file_path = 'playblast_ffmpeg.py'
    ui_file_name = get_ui_file_name(py_file_path)
    ui_file_path = os.path.join(os.path.dirname(py_file_path), ui_file_name)
    output_py_file_path = 'temp_ui.py'

    convert_ui_to_py(ui_file_path, output_py_file_path)
    formatted_code = format_py_file(output_py_file_path)
    new_content = insert_formatted_code(py_file_path, formatted_code)

    # Save the result to builded.py
    with open('builded.py', 'w', encoding='utf-8') as file:
        file.write(new_content)

    # Clean up temporary file
    os.remove(output_py_file_path)

if __name__ == "__main__":
    main()