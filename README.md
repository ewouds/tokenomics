# Tokenomics demo kit
**Recommended: open Tokenomics-Demo.ipynb** in VS Code or Jupyter. It has the full storyline, live code, charts for every demo, the numbers from the video, talk-track callouts and Foundry UI cards (save your screenshots in `img/`).

The standalone scripts below are a backup for running from the terminal. [docs/DEMO-SCRIPT.md](docs/DEMO-SCRIPT.md) has the same storyline as a written script.

| File | Demo |
|---|---|
| common.py | Shared client, token counting and cost logging |
| prices.json | **Fill in current prices** (USD per 1M tokens) |
| demo01_tokens.py | Tokens, input vs output pricing |
| demo02_context_creep.py | History resent every turn |
| demo03_system_prompt.py | Redundant base instructions |
| demo04_summarize_history.py | Rolling summary vs full history |
| demo05_external_state.py | External state (SQLite stand-in for PostgreSQL) |
| demo06_cap_output.py | max_completion_tokens with and without a matching instruction |
| demo07_prompt_caching.py | Automatic prefix caching (cached_tokens) |
| demo07b_cache_control.py | Explicit cache_control "ephemeral" (Claude, optional) |
| demo07c_semantic_cache.py | Semantic cache for FAQs |
| demo08_compare_models.py | Large vs small model |
| demo09_model_router.py | Model Router distribution |
| demo10_tool_bloat.py | Cost of tool definitions, routed vs all |
| demo11_agent_optimizer.md | azd ai agent optimize walkthrough |
| demo12_retrieval.py | Whole document vs relevant chunks |
| cost_calculator.py | Closing slide: savings by option at scale |

## Other project files
- `docs/` contains the written talk track and idea notes with their images.
- `web/` contains the HTML presentation, theme and animation previews, and their assets.
- `web/archive/` contains earlier HTML presentation versions.
