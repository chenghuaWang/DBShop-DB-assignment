"""
from pathlib import Path
current_folder = Path(__file__).absolute().parent
os.chdir(str(current_folder))
sys.path.append(str(current_folder.parent))
"""