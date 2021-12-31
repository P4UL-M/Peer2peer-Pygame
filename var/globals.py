from pathlib import Path
import sys


PATH = Path("/".join(sys.argv[0].split("/")[:-1]) or "\\".join(sys.argv[0].split("\\")[:-1])).absolute()

FONT = PATH / "assets" / "novem___.ttf"