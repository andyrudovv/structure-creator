from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static, Label
from textual.widgets import Log, Select
from textual.containers import Container
from textual.reactive import reactive
import os
import json

DEFAULT_PYTHON_PROJECT_STRUCTURE = {
    "data": {"raw": {}, "processed": {}},
    "models": {},
    "scripts": {"preprocessing": {}, "training": {}},
    "results": {"plots": {}, "metrics": {}},
    "src": {
        "__init__.py": {},
        "main.py": {}
    },
    "tests": {},
    "docs": {},
    "venv": {},
    ".gitignore": {},
    "requirements.txt": {}
}

FLASK_PROJECT_STRUCTURE = {
    "app": {
        "__init__.py": {},
        "routes.py": {},
        "models.py": {},
        "static": {
            "css": {},
            "js": {},
            "images": {}
        },
        "templates": {
            "index.html": {},
            "layout.html": {}
        }
    },
    "instance": {},
    "migrations": {},
    "tests": {},
    "venv": {},
    ".env": {},
    ".gitignore": {},
    "requirements.txt": {},
    "config.py": {},
    "run.py": {}
}

FASTAPI_PROJECT_STRUCTURE = {
    "app": {
        "main.py": {},
        "api": {
            "__init__.py": {},
            "v1": {
                "__init__.py": {},
                "endpoints": {
                    "items.py": {},
                    "users.py": {}
                }
            }
        },
        "core": {
            "__init__.py": {},
            "config.py": {},
            "security.py": {}
        },
        "db": {
            "__init__.py": {},
            "session.py": {},
            "models.py": {}
        },
        "schemas": {
            "item.py": {},
            "user.py": {}
        }
    },
    "tests": {
        "api": {}
    },
    "venv": {},
    ".env": {},
    ".gitignore": {},
    "requirements.txt": {},
    "Dockerfile": {},
    "README.md": {}
}

RUST_PROJECT_STRUCTURE = {
    "src": {
        "main.rs": {}
    },
    "target": {},
    ".gitignore": {},
    "Cargo.toml": {},
    "Cargo.lock": {},
    "README.md": {}
}

C_PLUS_PLUS_PROJECT_STRUCTURE = {
    "src": {
        "main.cpp": {},
        "header.h": {},
        "source.cpp": {}
    },
    "include": {},
    "build": {},
    "bin": {},
    "lib": {},
    "docs": {},
    ".gitignore": {},
    "CMakeLists.txt": {},
    "README.md": {}
}

WEB_PROJECT_STRUCTURE = {
    "public": {
        "index.html": {},
        "favicon.ico": {},
        "images": {},
        "css": {
            "style.css": {}
        },
        "js": {
            "main.js": {}
        }
    },
    "src": {
        "components": {},
        "pages": {},
        "App.js": {},
        "index.js": {}
    },
    "node_modules": {},
    "package.json": {},
    "package-lock.json": {},
    ".gitignore": {},
    "README.md": {}
}

TEMPLATES = {
    "Default Data Science/Python": DEFAULT_PYTHON_PROJECT_STRUCTURE,
    "Python - Flask Web App": FLASK_PROJECT_STRUCTURE,
    "Python - FastAPI API": FASTAPI_PROJECT_STRUCTURE,
    "Rust Project": RUST_PROJECT_STRUCTURE,
    "C++ Project (CMake)": C_PLUS_PLUS_PROJECT_STRUCTURE,
    "Frontend Web Project": WEB_PROJECT_STRUCTURE,
    "Custom JSON File": None
}

class FolderInput(Static):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Base path (e.g. ./my_project)", id="base_path")
        yield Label("Select Project Template:")
        yield Select(
            options=[(name, name) for name in TEMPLATES.keys()],
            prompt="Choose a template",
            id="template_select"
        )
        yield Input(placeholder="JSON structure file (optional, overrides template)", id="structure_file")

class StructGenApp(App):
    CSS_PATH = None
    base_path = reactive("")
    structure_file = reactive("")
    selected_template_name = reactive("")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(FolderInput(), id="inputs")
        yield Button("Create Structure", id="create", variant="success")
        yield Log(id="log", highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#template_select", Select).value = list(TEMPLATES.keys())[0]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.base_path = self.query_one("#base_path", Input).value.strip()
        self.structure_file = self.query_one("#structure_file", Input).value.strip()
        self.selected_template_name = self.query_one("#template_select", Select).value

        if not self.base_path:
            self.query_one(Log).write("[red]❌ Base path is required.")
            return

        structure = {}
        try:
            if self.structure_file:
                if not os.path.exists(self.structure_file):
                    self.query_one(Log).write(f"[red]❌ Error: Custom JSON file '{self.structure_file}' not found.")
                    return
                with open(self.structure_file, "r") as f:
                    structure = json.load(f)
                self.query_one(Log).write(f"[blue]Loading structure from custom JSON file: '{self.structure_file}'")
            elif self.selected_template_name and self.selected_template_name != "Custom JSON File":
                structure = TEMPLATES[self.selected_template_name]
                self.query_one(Log).write(f"[blue]Using '{self.selected_template_name}' template structure.")
            else:
                self.query_one(Log).write("[red]❌ Please select a template or provide a custom JSON file path.")
                return


            self.create_structure(self.base_path, structure)
            self.query_one(Log).write(f"Folder structure created in '{self.base_path}'")
        except json.JSONDecodeError as e:
            self.query_one(Log).write(f"Error parsing JSON file: {e}")
        except Exception as e:
            self.query_one(Log).write(f"Error: {e}")

    def create_structure(self, base, structure):
        for item_name, sub in structure.items():
            path = os.path.join(base, item_name)
            if isinstance(sub, dict):
                os.makedirs(path, exist_ok=True)
                self.query_one(Log).write(f"Created directory: {path}")
                if sub:
                    self.create_structure(path, sub)
            else:
                try:
                    with open(path, 'a'):
                        os.utime(path, None)
                    self.query_one(Log).write(f"Created file: {path}")
                except Exception as e:
                    self.query_one(Log).write(f"[red]❌ Failed to create file {path}: {e}")

if __name__ == "__main__":
    StructGenApp().run()