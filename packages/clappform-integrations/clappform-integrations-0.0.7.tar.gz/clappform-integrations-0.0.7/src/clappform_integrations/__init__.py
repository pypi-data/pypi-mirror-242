from pathlib import Path
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

import clappform_ijsseldal.src as ijsseldal
import clappform_itsperfect.src as itsperfect
import clappform_rudholm.src as rudholm
