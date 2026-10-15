# Day 1 — Python Environment Notes

## 1. Project Environment

* **Project:** AI Inference Engineering
* **Component:** track1-client
* **Python version:** Python 3.14
* **Virtual environment:** `.venv`
* **Package configuration:** `pyproject.toml`

The virtual environment isolates this project's Python packages from other Python projects on the computer.

To activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

To check the Python version:

```powershell
python --version
```

To find the Python interpreter currently being used:

```powershell
python -c "import sys; print(sys.executable)"
```

The interpreter path should point inside this project's `.venv` directory.

## 2. Standard Output (stdout)

`stdout` is the standard output stream. Programs typically use it to display normal results.

Example:

```python
print("Inference model ready.")
```

Redirect stdout to a file in PowerShell:

```powershell
python .\hello_inference.py > stdout.txt 2> stderr.txt
```

The normal message is saved in `stdout.txt`.

## 3. Standard Error (stderr)

`stderr` is the standard error stream. Programs commonly use it for diagnostic messages, warnings, and errors.

Example:

```python
import sys

print("Notice: No GPU detected, using CPU.", file=sys.stderr)
```

In the command above, the diagnostic message is saved in `stderr.txt`.

**Note:** This message is simulated for learning. The script does not actually detect a GPU.

## 4. Exit Codes

An exit code indicates how a program finished.

* `0` generally means successful execution.
* A nonzero exit code generally indicates failure.

In PowerShell, check the exit code of the last native program:

```powershell
$LASTEXITCODE
```

Run this immediately after the program you want to inspect.

On Linux, the equivalent shell variable is:

```bash
echo $?
```

The value must be checked immediately after the command whose result matters.

## 5. Why Separate stdout and stderr?

Separating normal output from diagnostics makes programs easier to debug and operate.

For example, an inference service might send its results to one stream and diagnostic messages to another. These streams can then be captured or processed separately.

## 6. Day 1 Progress

* [x] Created the `track1-client` project directory.
* [x] Created a Python virtual environment.
* [x] Created `pyproject.toml`.
* [x] Installed the project in editable mode.
* [x] Created and executed `hello_inference.py`.
* [x] Redirected stdout and stderr into separate files.
* [x] Checked the program's exit code.
* [x] Documented the Python environment and output streams.