"""Demo 7b (optional) - Explicit cache_control (Claude models in Microsoft Foundry).

Some models need you to MARK what to cache. Each static block gets
cache_control={"type": "ephemeral"}: the first request pays a cache WRITE,
later requests with the same prefix pay a cache READ (roughly 10% of normal input).

Env: ANTHROPIC_FOUNDRY_BASE_URL (your Foundry Claude endpoint), ANTHROPIC_FOUNDRY_API_KEY, CLAUDE_MODEL
"""
import os
from anthropic import Anthropic
from common import banner, B, G, Y, X, pause

banner("DEMO 7b - Explicit cache_control (ephemeral)")
c = Anthropic(base_url=os.environ["ANTHROPIC_FOUNDRY_BASE_URL"], api_key=os.environ["ANTHROPIC_FOUNDRY_API_KEY"])
policy = "\n".join(f"Policy {i}: category {i} returns within {14 + i % 3 * 7} days with receipt." for i in range(1, 400))

system = [
    {"type": "text", "text": "You are Contoso's returns assistant. One sentence answers."},
    {"type": "text", "text": policy, "cache_control": {"type": "ephemeral"}},   # <- cache this block
]
for i, q in enumerate(["Category 7 after 20 days?", "Category 12?"], 1):
    r = c.messages.create(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5"), max_tokens=100,
                          system=system, messages=[{"role": "user", "content": q}])
    u = r.usage
    print(f"{B}Call {i}{X} input={u.input_tokens} cache_write={Y}{u.cache_creation_input_tokens}{X} "
          f"cache_read={G}{u.cache_read_input_tokens}{X} output={u.output_tokens}")
    pause()
