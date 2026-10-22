"""Demo 5 - Store state externally; retrieve only what this turn needs.

Runs on SQLite so it works anywhere. In production use PostgreSQL (the video uses PostgreSQL),
Cosmos DB, Redis... The pattern is the same: write every turn, read only the relevant slice.
"""
import sqlite3
from common import *

banner("DEMO 5 - External conversation state", "Write everything, retrieve only what's relevant")

db = sqlite3.connect(":memory:")  # PostgreSQL: psycopg.connect(os.environ["PG_CONN"])
db.execute("CREATE TABLE memory (session TEXT, kind TEXT, topic TEXT, content TEXT)")
facts = [
    ("profile", "user", "User is called Ewoud, works in Zaventem, prefers answers in English."),
    ("fact", "travel", "User has a dog (a labrador) and travels by train."),
    ("fact", "travel", "User wants a dog-friendly beach near Bruges."),
    ("fact", "work", "User is preparing a tokenomics session for the STU team on Monday."),
    ("fact", "work", "User needs code examples for prompt caching and Model Router."),
    ("fact", "food", "User is vegetarian."),
]
db.executemany("INSERT INTO memory VALUES ('s1', ?, ?, ?)", facts)

def retrieve(session, topics):
    q = f"SELECT content FROM memory WHERE session=? AND (kind='profile' OR topic IN ({','.join('?'*len(topics))}))"
    return [row[0] for row in db.execute(q, (session, *topics))]

question, topics = "Which restaurant should I book after the beach?", ["travel", "food"]
everything = [r[0] for r in db.execute("SELECT content FROM memory WHERE session='s1'")]
relevant = retrieve("s1", topics)

for label, mem in [("Send ALL memory", everything), ("Send RELEVANT memory", relevant)]:
    msgs = [{"role": "system", "content": "You are a helpful assistant. Max 2 sentences.\nKnown about user:\n- "
             + "\n- ".join(mem)}, {"role": "user", "content": question}]
    r, s = chat(msgs)
    print(f"\n{DIM}{r.choices[0].message.content}{X}")
    log_usage(label, r, s)
print(f"\n{Y}With 6 facts the gap is small; with 6 months of history it is the whole bill.{X}")
