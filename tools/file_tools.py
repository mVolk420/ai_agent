from langchain_core.tools import tool
import os

@tool
def read_file(filename: str) -> str:
    """Liest den Inhalt einer Textdatei."""
    if not os.path.isfile(filename):
        return f"Datei '{filename}' nicht gefunden."
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

@tool
def find_file(filename: str, search_dir: str = ".") -> str:
    """Sucht nach einer Datei im angegebenen Verzeichnis (rekursiv) und gibt den Pfad zurück."""
    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    return f"Datei '{filename}' wurde nicht gefunden."
