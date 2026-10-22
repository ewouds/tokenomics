"""Demo 4 - Summarize and dedupe history instead of resending the raw transcript."""
from common import *

banner("DEMO 4 - Rolling summary vs. full history", "Same conversation, two memory strategies")

SYSTEM = {"role": "system", "content": "You are a travel assistant. Be brief (max 3 sentences)."}
QUESTIONS = ["Which beaches in Belgium are dog friendly?",
             "Are dogs allowed there in summer?",
             "Any of them close to Bruges?",
             "Which one has the best restaurant nearby?"]
KEEP_LAST = 1  # keep the last N question/answer pairs verbatim

def summarize(pairs):
    text = "\n".join(f"{m['role']}: {m['content']}" for m in pairs)
    r, _ = chat([{"role": "system", "content": "Summarize this conversation in max 50 words. "
                  "Keep facts, places and user preferences. Drop repetition."},
                 {"role": "user", "content": text}], model=MODEL_SMALL)
    return r.choices[0].message.content, r

full, recent, summary = [], [], ""
rows = []
for i, q in enumerate(QUESTIONS, 1):
    # Strategy A - full history
    full.append({"role": "user", "content": q})
    ra, _ = chat([SYSTEM] + full)
    full.append({"role": "assistant", "content": ra.choices[0].message.content})

    # Strategy B - summary + last turn(s)
    ctx = [SYSTEM]
    if summary:
        ctx.append({"role": "system", "content": f"Conversation summary so far: {summary}"})
    rb, _ = chat(ctx + recent + [{"role": "user", "content": q}])
    recent += [{"role": "user", "content": q}, {"role": "assistant", "content": rb.choices[0].message.content}]
    sum_cost = 0
    if len(recent) > 2 * KEEP_LAST:
        old, recent = recent[:-2 * KEEP_LAST], recent[-2 * KEEP_LAST:]
        summary, rs = summarize(([{"role": "system", "content": summary}] if summary else []) + old)
        sum_cost = rs.usage.prompt_tokens + rs.usage.completion_tokens
    rows.append((i, ra.usage.prompt_tokens, rb.usage.prompt_tokens, sum_cost))
    print(f"\n{B}Turn {i}:{X} {q}\n  {DIM}full   :{X} {ra.choices[0].message.content[:110]}...\n"
          f"  {DIM}summary:{X} {rb.choices[0].message.content[:110]}...")

banner("Input tokens per turn")
print(f"{'Turn':<6}{'Full history':>14}{'Summary':>10}{'(summarizer cost)':>20}")
for i, a, b, sc in rows:
    print(f"{i:<6}{a:>14}{G}{b:>10}{X}{DIM}{sc:>20}{X}")
print(f"\nCurrent summary: {summary}")
print(f"{Y}Tip:{X} the summarizer is a cheap small-model call; the saving grows with every turn.")
