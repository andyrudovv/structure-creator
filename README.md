# 📁 Textual Project Structure Generator

A Textual-based (TUI - Terminal User Interface) application to quickly generate common project folder structures, with support for pre-defined templates (Python, Flask, FastAPI, Rust, C++, Web) and custom JSON configurations.

---

## ✨ Features

* **Interactive TUI:** A user-friendly terminal interface built with Textual.
* **Pre-defined Templates:** Generate boilerplate structures for:
    * Default Data Science/Python Project
    * Python Flask Web App
    * Python FastAPI API
    * Rust Project
    * C++ Project (CMake-based)
    * Frontend Web Project
* **Custom JSON Support:** Provide your own `.json` file to define a completely custom folder and file structure.
* **File Creation:** Templates can include placeholders for empty files (e.g., `__init__.py`, `.gitignore`, `main.py`).
* **Live Logging:** See real-time feedback on directories and files being created.

---

## 🚀 Installation

### Prerequisites

* Python 3.8+

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/andyrudovv/structure-creator.git
    cd structure-creator
    ```

2.  **Install dependencies(can use venv by yourself):**

    ```cmd
    pip install -r requirements.txt
    ```

3. **Add sc.bat to PATH**

---

### You can build source code main.py by yourself for any platform

## 💡 Usage

### Running the Application

After installation, activate your virtual environment (if not already active) and run:

**Windows (`sc.bat`):**
If you use the provided `sc.bat` script:
```cmd
sc.bat
