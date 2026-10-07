import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def sample_payload(variables, base=20.0):
    times = [f"2026-10-01T{h:02d}:00" for h in range(24)]
    hourly = {"time": times}
    for i, v in enumerate(variables):
        hourly[v] = [base + i + h * 0.1 for h in range(24)]
    hourly[variables[0]][3] = None  # exercise null handling
    return {"hourly": hourly}
