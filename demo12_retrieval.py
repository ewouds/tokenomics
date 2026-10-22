"""Demo 12 - Retrieval quality drives total cost: send the relevant chunks, not the whole document."""
from common import *

banner("DEMO 12 - Whole document vs. relevant chunks", "Bad retrieval = more tokens, more retries, worse answers")

sections = {f"Section {i}": f"Contoso travel policy section {i}. " + " ".join(
    f"Rule {i}.{j}: employees travelling for {['training', 'customer visits', 'events', 'internal meetings'][j % 4]} "
    f"must {'book economy' if j % 2 else 'get manager approval'} when the trip exceeds {j * 100} km." for j in range(1, 15))
    for i in range(1, 16)}
sections["Section 7"] += " Rail is mandatory for trips between Brussels and Paris, Amsterdam or London."
document = "\n\n".join(f"{k}\n{v}" for k, v in sections.items())
question = "Can I fly from Brussels to Paris?"

def top_k(q, k=2):  # toy keyword retrieval; Azure AI Search / Foundry IQ do this properly
    words = set(w.strip("?.,").lower() for w in q.split() if len(w) > 3)
    score = lambda t: sum(w in t.lower() for w in words)
    return sorted(sections.items(), key=lambda kv: score(kv[1]), reverse=True)[:k]

chunks = "\n\n".join(f"{k}\n{v}" for k, v in top_k(question))
for label, ctx in [("Whole document", document), ("Top-2 chunks", chunks)]:
    r, s = chat([{"role": "system", "content": "Answer from the context only, one sentence.\n\n" + ctx},
                 {"role": "user", "content": question}])
    print(f"{DIM}{r.choices[0].message.content}{X}")
    log_usage(label, r, s)
print(f"\n{Y}Foundry IQ:{X} one endpoint over many knowledge sources; a small model plans the query, "
      "splits it and routes each part to the right source before returning context to the agent.")
