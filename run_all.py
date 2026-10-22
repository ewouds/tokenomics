from pathlib import Path
import argparse
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

parser = argparse.ArgumentParser(description="Voer demo-scripts vanaf een gekozen nummer uit.")
parser.add_argument("--start", type=int, default=1, help="Demonummer om vanaf te starten (standaard: 1)")
args = parser.parse_args()

numbered_scripts = []
for path in ROOT.glob("demo*.py"):
    match = re.match(r"demo[_-]?(\d+)", path.stem, re.IGNORECASE)
    if match:
        number = int(match.group(1))
        if number >= args.start:
            numbered_scripts.append((number, path))

scripts = [path for _, path in sorted(numbered_scripts)]

if not scripts:
    raise SystemExit(f"Geen demo-scripts gevonden vanaf nummer {args.start}.)")

for script in scripts:
    print(f"\n=== Running {script.name} ===", flush=True)
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)

print("\nAlle geselecteerde demo-scripts zijn uitgevoerd.")