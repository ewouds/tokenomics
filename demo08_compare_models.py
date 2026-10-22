"""Demo 8 - Model choice is the biggest lever: same prompt, two models."""
from common import *

banner("DEMO 8 - Large vs small model", "Lowest price per token != lowest total cost")

TASKS = {
    "simple":  "Classify the sentiment of: 'The delivery was late but support was great.' Answer with one word.",
    "complex": "A customer has 3 subscriptions in 2 regions with reserved capacity expiring in different months. "
               "Outline a 5-step plan to consolidate them while minimising downtime and cost. Be concise.",
}
results = []
for task, prompt in TASKS.items():
    print(f"\n{B}{task.upper()} TASK{X}: {prompt[:90]}...")
    for model in (MODEL_LARGE, MODEL_SMALL):
        r, s = chat([{"role": "user", "content": prompt}], model=model)
        print(f"{DIM}{model}: {r.choices[0].message.content[:160]}...{X}")
        u = log_usage(model, r, s)
        results.append((task, model, cost(model, u["prompt"], u["completion"]), s))
    pause()

banner("Summary")
for task, model, c, s in results:
    print(f"{task:<8} {model:<16} {fmt_cost(c):>28} {s:5.1f}s")
print(f"\n{Y}Now show the Foundry model comparison and leaderboard (quality vs cost vs throughput).{X}")
print("Remember: a cheap model that needs 3 retries can cost more than a larger model that gets it right once.")
