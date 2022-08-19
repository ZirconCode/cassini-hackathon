from pathlib import Path

BOUNDS = {
    "west": 8.258889841,
    "north": 47.562982412,
    "south": 47.235039561,
    "east": 8.738077426,
}

DATA_DIR = Path(__file__).parent.parent.absolute() / "data"
HEATMAP = DATA_DIR / "prelim_heatmap.npy"
