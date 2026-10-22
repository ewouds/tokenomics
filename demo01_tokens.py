"""Demo 1 - The currency: what is a token, and why output costs more."""
from common import *

banner("DEMO 1 - Tokens are the new AI currency", "A token = a word, part of a word, punctuation or whitespace")

for text in ["Tokenomics", "Hello, world!", "Zaventem   is   in   Belgium.", "Supercalifragilisticexpialidocious"]:
    print(f"\n{B}{text!r}{X}")
    n = show_tokens(text)
    print(f"-> {Y}{n} tokens{X}")
pause()

prompt = "Explain in 3 bullet points why AI costs grow when adoption scales."
messages = [{"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": prompt}]
print(f"\nPrompt: {prompt}")
r, s = chat(messages)
print(f"\n{r.choices[0].message.content}\n")
u = log_usage("One call", r, s)

p = prices().get(r.model.split("-20")[0]) or prices().get(MODEL_SMALL, {})
if p.get("input") and p.get("output"):
    print(f"\nOutput is {p['output']/p['input']:.1f}x the price of input for this model.")
    print(f"Input cost : ${u['prompt']*p['input']/1e6:.6f}")
    print(f"Output cost: ${u['completion']*p['output']/1e6:.6f}  <- you pay for what the model WRITES")
else:
    print("\nFill in prices.json to show the input vs output price split (output is typically 3-5x input).")
