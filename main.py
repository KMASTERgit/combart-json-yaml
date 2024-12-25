import eel
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
import yaml

from python_dir.convartClass import convert as cc

@eel.expose
def save_file_dialog(default_name):
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # 隠す
    file_path = filedialog.asksaveasfilename(
        initialfile=default_name,
        filetypes=[("YAML files", "*.yaml"), ("JSON files", "*.json")]
    )
    return file_path if file_path else None

@eel.expose
def save_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

@eel.expose
def open_file_dialog():
    Tk().withdraw()  # Tkinter GUIを非表示にする
    file_path = askopenfilename(
        filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml")]
    )
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.endswith('.json'):
                content = json.load(file)
            elif file_path.endswith('.yaml'):
                content = yaml.safe_load(file)
            else:
                return {"error": "Unsupported file format"}
        return {"file_name": file_path.split("/")[-1], "content": content}
    return {"error": "No file selected"}

@eel.expose
def process_file_content(file_name, content):
    print(f"Processing file: {file_name}")
    print(f"Content: {content}")
    # 仮の処理結果（Python側で処理するコードを書く場所）

    file_content = file_name.split(".")[1]
    converted = cc(file_content,content)
    processed_content = converted
    return processed_content

def main():
    eel.init("web")
    eel.start("main.html", size=(1024, 768), port=8080)


if __name__ == "__main__":
    main()