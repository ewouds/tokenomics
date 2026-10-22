"""Demo 2 - Context window creep: stateless models resend everything, every turn."""
from common import *

banner("DEMO 2 - Context window creep", "Models are stateless: system prompt + full history are resent on every turn")

messages = [{"role": "system", "content": "You are a helpful geography assistant. Answer briefly."}]
for turn, question in enumerate(["What is the capital of France?", "And Italy?", "What about California?"], 1):
    messages.append({"role": "user", "content": question})
    r, s = chat(messages)
    answer = r.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print(f"\n{B}Turn {turn}{X} user: {question}\n       bot : {answer}")
    log_usage(f"Turn {turn}", r, s)
    print(f"{DIM}       messages sent this turn: {len(messages) - 1}{X}")
    pause()

print(f"\n{B}What was actually sent on the last turn:{X}")
print(json.dumps(messages[:-1], indent=2))
print(f"\n{Y}The user typed 3 words, but we paid for the whole conversation again.{X}")
print("Tool outputs, RAG documents and metadata are ALSO input tokens.")
