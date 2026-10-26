"""Execute the saved notebook from a fresh kernel in the project root."""
import os
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
for name in ["ipython", "jupyter", "matplotlib"]:
    (RUNTIME / name).mkdir(parents=True, exist_ok=True)
os.environ["IPYTHONDIR"] = str(RUNTIME / "ipython")
os.environ["JUPYTER_RUNTIME_DIR"] = str(RUNTIME / "jupyter")
os.environ["MPLCONFIGDIR"] = str(RUNTIME / "matplotlib")
os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")

path = ROOT / "hillstrom_email_analysis.ipynb"
nb = nbformat.read(path, as_version=4)
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None
client = NotebookClient(nb, timeout=300, startup_timeout=30, kernel_name="python3",
                        allow_errors=False, resources={"metadata": {"path": str(ROOT)}})
progress = [0]
def report(cell, cell_index, **kwargs):
    progress[0] += 1
    if progress[0] % 10 == 0:
        print("Completed", progress[0], "code cells", flush=True)
client.on_cell_executed = report
print("Starting fresh-kernel execution:", sum(c.cell_type == "code" for c in nb.cells),
      "code cells", flush=True)
try:
    client.execute()
except Exception:
    nbformat.write(nb, RUNTIME / "failed_execution.ipynb")
    raise
nbformat.validate(nb)
nbformat.write(nb, path)
print("Execution complete:", path.name, flush=True)
