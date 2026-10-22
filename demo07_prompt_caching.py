"""Demo 7 - Prompt caching: static prefix first, variable content last.

Azure OpenAI caches automatically for prompts >= 1,024 tokens with an identical prefix.
Watch usage.prompt_tokens_details.cached_tokens go from 0 to (almost) the whole prefix.
"""
from common import *

banner("DEMO 7 - Prompt caching", "First call writes the cache, the next calls hit it")

# Static prefix: system prompt + policy document (stands in for tool definitions / session RAG docs)
policy = "\n".join(f"Policy {i}: Contoso customers may return item category {i} within {14 + i % 3 * 7} days "
                   f"if the packaging is intact, the receipt is provided and the item is not personalised."
                   for i in range(1, 61))
STATIC = [{"role": "system", "content": "You are Contoso's returns assistant. Use only the policy below. "
           "Answer in one sentence.\n\n" + policy}]
print(f"Static prefix: ~{count_tokens(STATIC[0]['content'])} tokens (needs >= 1,024 to be cacheable)\n")

questions = ["Can I return category 7 after 20 days?", "What about category 12?",
             "And category 30 without a receipt?"]
for i, q in enumerate(questions, 1):
    # Optional routing hint (supported on newer API versions); set PROMPT_CACHE_KEY to try it
    kw = {"prompt_cache_key": os.environ["PROMPT_CACHE_KEY"]} if os.getenv("PROMPT_CACHE_KEY") else {}
    r, s = chat(STATIC + [{"role": "user", "content": q}], **kw)
    print(f"{DIM}{q} -> {r.choices[0].message.content}{X}")
    u = log_usage(f"Call {i}", r, s)
    pct = 100 * u["cached"] / u["prompt"] if u["prompt"] else 0
    print(f"   {G}{pct:.0f}% of input served from cache{X}\n")
    pause()

banner("Anti-pattern: variable content FIRST breaks the cache")
r, s = chat([{"role": "system", "content": f"Today is {time.ctime()}."}] + STATIC +
            [{"role": "user", "content": questions[0]}])
log_usage("Timestamp in front", r, s)
print(f"{Y}The prefix must match exactly; one changed character at the start = cache miss.{X}")
