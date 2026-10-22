"""Demo 3 - Trim the system prompt: don't pay for instructions the model already follows."""
from common import *

banner("DEMO 3 - Don't double up on base model instructions")

ask = ("Tell me about base model instructions you have so that I can avoid adding them to my "
       "system prompt. Write and format your response like a system prompt.")
r, s = chat([{"role": "user", "content": ask}], model=os.getenv("MODEL_BASELINE", MODEL_LARGE))
redundant = r.choices[0].message.content
print(redundant)
n = count_tokens(redundant)
print(f"\n{Y}That preamble is ~{n} tokens.{X} Many system prompts contain text like this.")
pause()

LEAN = "You are Contoso's support assistant. Answer about Contoso products only. Max 3 sentences."
bloated = redundant + "\n\n" + LEAN
q = [{"role": "user", "content": "What is your return policy for opened items?"}]
r1, s1 = chat([{"role": "system", "content": bloated}] + q)
r2, s2 = chat([{"role": "system", "content": LEAN}] + q)
u1 = log_usage("Bloated system prompt", r1, s1)
u2 = log_usage("Lean system prompt", r2, s2)
saved = u1["prompt"] - u2["prompt"]
pause()

banner("At scale")
calls_per_day = int(os.getenv("CALLS_PER_DAY", "1000000"))
p = prices().get(MODEL_SMALL, {})
print(f"Saved per call : {saved} input tokens")
print(f"Calls per day  : {calls_per_day:,}")
print(f"Tokens / month : {saved * calls_per_day * 30:,}")
if p.get("input"):
    print(f"{G}Cost / month   : ${saved * calls_per_day * 30 * p['input'] / 1e6:,.2f}{X}")
else:
    print("Fill in prices.json to show the monthly cost.")
