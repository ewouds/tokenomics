"""Offline cost calculator for the closing slide. No API calls. Edit the numbers live with the audience."""
import sys
from common import prices, banner, B, G, Y, X, MODEL_SMALL

model = sys.argv[1] if len(sys.argv) > 1 else MODEL_SMALL
p = prices().get(model, {})
if p.get("input") is None:
    sys.exit(f"Fill in prices for {model} in prices.json first.")
cached_price = p["cached_input"] if p.get("cached_input") is not None else p["input"] * 0.1

calls = 1_000_000 * 30          # calls per month
base = dict(system=800, history=1500, tools=4700, user=40, output=600)

def monthly(system, history, tools, user, output, cache_ratio=0.0):
    static = system + tools
    inp = static * (1 - cache_ratio) * p["input"] + static * cache_ratio * cached_price + (history + user) * p["input"]
    return calls * (inp + output * p["output"]) / 1e6

scenarios = [
    ("Baseline", base, 0.0),
    ("+ lean system prompt (-300)", {**base, "system": 500}, 0.0),
    ("+ summarized history", {**base, "system": 500, "history": 300}, 0.0),
    ("+ capped output", {**base, "system": 500, "history": 300, "output": 200}, 0.0),
    ("+ prompt caching (90% hit)", {**base, "system": 500, "history": 300, "output": 200}, 0.9),
    ("+ Toolbox (4,700 -> 467)", {**base, "system": 500, "history": 300, "output": 200, "tools": 467}, 0.9),
]
banner(f"Monthly cost at {calls:,} calls - {model}")
first = None
for name, s, cr in scenarios:
    c = monthly(**s, cache_ratio=cr)
    first = first or c
    print(f"{name:<32} ${c:>14,.0f}   {G}-{100 * (1 - c / first):4.0f}%{X}")
print(f"\n{Y}Illustrative token sizes - replace them with numbers from the customer's own logs.{X}")
