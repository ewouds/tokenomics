"""Demo 7c - Semantic cache: answer similar questions without calling the LLM.

Trade: a little embedding + storage cost instead of a full LLM call. Great for FAQs.
"""
import numpy as np
from common import *

banner("DEMO 7c - Semantic cache for FAQs")
THRESHOLD = float(os.getenv("SEMANTIC_THRESHOLD", "0.85"))
cache = []  # list of (embedding, question, answer) - use Azure AI Search / Redis / Cosmos DB in production

def embed(text):
    v = np.array(client().embeddings.create(model=EMBEDDING_MODEL, input=text).data[0].embedding)
    return v / np.linalg.norm(v)

def ask(q):
    e = embed(q)
    if cache:
        sims = [float(e @ ce) for ce, _, _ in cache]
        best = int(np.argmax(sims))
        if sims[best] >= THRESHOLD:
            print(f"{G}CACHE HIT{X} ({sims[best]:.2f} ~ '{cache[best][1]}') -> 0 LLM tokens\n  {cache[best][2]}")
            return
        print(f"{DIM}best similarity {sims[best]:.2f} < {THRESHOLD}{X}")
    r, s = chat([{"role": "system", "content": "Answer in one sentence."}, {"role": "user", "content": q}])
    answer = r.choices[0].message.content
    cache.append((e, q, answer))
    print(f"{Y}CACHE MISS{X} -> LLM call\n  {answer}")
    log_usage("  LLM", r, s)

for q in ["How do I reset my password?", "I forgot my password, how can I reset it?",
          "What are your opening hours?", "When are you open?", "How do I reset my password?"]:
    print(f"\n{B}Q: {q}{X}")
    ask(q)
