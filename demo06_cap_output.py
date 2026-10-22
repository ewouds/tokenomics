"""Demo 6 - Cap output tokens AND tell the model about the cap."""
from common import *

banner("DEMO 6 - Output is the expensive side: cap it (the right way)")

CAP = int(os.getenv("OUTPUT_CAP", "200"))
# GPT-5 family: max_completion_tokens also covers hidden reasoning tokens -> keep reasoning low for this demo.
extra = {"reasoning_effort": os.environ["REASONING_EFFORT"]} if os.getenv("REASONING_EFFORT") else {}
question = {"role": "user", "content": "Explain how Azure prompt caching works."}

runs = [
    ("A) Unrestricted", [question], {}),
    ("B) Cap only", [question], {"max_completion_tokens": CAP}),
    ("C) Cap + matching instruction", [{"role": "system", "content":
        f"Answer in at most 80 words (hard limit {CAP} tokens). Finish your last sentence."}, question],
        {"max_completion_tokens": CAP}),
]
for label, msgs, kw in runs:
    r, s = chat(msgs, **kw, **extra)
    text = r.choices[0].message.content or ""
    print(f"\n{B}{label}{X}\n{DIM}...{text[-220:]}{X}")
    log_usage(label, r, s)
    fr = r.choices[0].finish_reason
    print(f"finish_reason = {R if fr == 'length' else G}{fr}{X}"
          + ("   <- cut off mid-sentence: bad user experience" if fr == "length" else ""))
    pause()
print(f"\n{Y}Rule:{X} max_completion_tokens is the safety net; the instruction makes the answer FIT.")
