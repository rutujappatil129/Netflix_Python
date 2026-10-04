from pathlib import Path
import runpy


dashboard = Path(__file__).with_name("app.py")
runpy.run_path(str(dashboard), run_name="__main__")
