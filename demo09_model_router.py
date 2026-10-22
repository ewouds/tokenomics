"""Demo 9 - Model Router: one endpoint, a model is picked per prompt.

Deploy 'model-router' from the Foundry model catalog and choose a routing mode
(Balanced / Quality / Cost) on the deployment. The response tells you which model answered.
"""
from collections import Counter
from common import *

banner("DEMO 9 - Model Router", f"Deployment: {MODEL_ROUTER}")

PROMPTS = [
    "Translate 'good morning' to Dutch.",
    "What is 17 * 23?",
    "Write a haiku about Brussels traffic.",
    "Compare three architectures for multi-tenant RAG on Azure with trade-offs in cost, latency and isolation.",
    "Prove that the square root of 2 is irrational, step by step.",
    "Summarize: 'Tokens are billed per million; output costs more than input.'",
]
used = Counter()
for p in PROMPTS:
    r, s = chat([{"role": "user", "content": p}], model=MODEL_ROUTER)
    used[r.model] += 1
    print(f"\n{B}{p[:70]}{X}")
    log_usage("routed", r, s)  # r.model = the underlying model that answered

banner("Routing distribution")
for m, n in used.most_common():
    print(f"{m:<30} {'#' * n} {n}")
print(f"\n{Y}Switch the routing mode (Balanced -> Cost -> Quality) on the deployment and run again.{X}")
