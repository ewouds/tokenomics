# Tokenomics: The New AI Currency & Your Options Explained
**Hands-on demo script · STU Collective · Monday 26 October 2026, 10:00–12:00**
Presenter: Ewoud Smets · About 75 min of demos plus Q&A · Based on the Microsoft Mechanics episode of the same name

> Storyline: **Part 1** shows how the currency works (what a token costs and where the money goes).
> **Part 2** goes through five options for spending less. Every demo is a short Python script you run live in
> VS Code. The numbers in quotes are what the video showed, so you can compare them with your own results.

---

## 0. Setup (do this Friday)

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com"
export AZURE_OPENAI_API_KEY="<key>"
export MODEL_LARGE="gpt-5.4"  MODEL_SMALL="gpt-5.4-mini"  MODEL_ROUTER="model-router"
export EMBEDDING_MODEL="text-embedding-3-small"
export REASONING_EFFORT="low"   # optional: keeps hidden reasoning tokens small on GPT-5 models
```

- [ ] Fill in **prices.json** with current list prices for your region. Every cost column depends on it.
- [ ] Deploy the large, small, router and embedding models in your Foundry project (https://ai.azure.com).
- [ ] Create two agents in the Foundry playground, one **without Toolbox** and one **with Toolbox**, for Demo 10B.
- [ ] Configure evaluations on one agent and **start `azd ai agent optimize` beforehand** for Demo 11.
- [ ] Rehearse once and screenshot each terminal output to use as a backup.
- [ ] Use a large terminal font, a dark theme and a split screen with code on the left and the terminal on the right.

Every script pauses at the important points, so press Enter to continue. Set `DEMO_NO_PAUSE=1` for a dry run.

---

## Opening (3 min): "AI has a currency now"

**Say:** "When a pilot becomes a product, the AI bill doesn't grow in a straight line. It's not mainly about
*how often* we call the model. It's about how we *design* the experience: prompt length, how much context we
send, and which model we use. Today I'll show you the currency and then your options for spending less."

---

# PART 1: THE NEW AI CURRENCY

## Demo 1: What a token is worth (6 min) · `python demo01_tokens.py`

| Show | Point |
|---|---|
| Token split of `"Tokenomics"`, punctuation and extra spaces | A token can be a word, part of a word, punctuation or whitespace. Each model family has its own tokenizer, and OpenAI models use tiktoken. |
| One live call with input and output token counts | Input is everything you send, including instructions. Output is everything the model generates. |
| Input cost vs output cost | Prices are per million tokens, and **output usually costs 3–5× more**, because generating text needs more compute than reading it. |

**Main point:** "You pay for every token the model reads and writes, not just what the user types."

## Demo 2: Where the money goes, context window creep (6 min) · `python demo02_context_creep.py`

Run the three turns: *capital of France?* → *And Italy?* → *What about California?*

**Say:** "The model has no memory. The only way it understands 'And Italy?' is that we send the whole
conversation again. The user asks shorter questions, but we pay more each time."

**Video numbers:** turn 1 = **34**, turn 2 = **52**, turn 3 = **71** prompt tokens.
After the run, the script prints exactly what was sent on the last turn.
**Also mention:** tool outputs, retrieved RAG documents and hidden metadata are also input tokens. Even though
input is cheaper per token, it can make up most of the bill.

**Transition:** "Now that we've seen where the money goes, let's look at the options."

---

# PART 2: YOUR OPTIONS EXPLAINED

## Option 1: Spend less on each call (18 min)

### Demo 3: Trim the system prompt · `python demo03_system_prompt.py`
1. The script asks the model which base instructions it already follows, written as a system prompt (the video used GPT-4o).
2. It counts that text. **The video found about 300 tokens**, which is the kind of text many teams paste into their system prompts.
3. It compares a bloated and a lean system prompt on the same question, then scales the difference to a month
   (`CALLS_PER_DAY`, default 1M).

**Say:** "Don't repeat instructions the model already follows. 300 tokens on every turn can cost thousands per billing cycle."

### Demo 4: Summarize and dedupe history · `python demo04_summarize_history.py`
Four questions about dog-friendly beaches. **Strategy A** sends the full history. **Strategy B** sends a rolling summary
plus the last turn. The table shows input tokens per turn for each strategy, plus the cost of the summarizer.
**Video number:** with a summary at turn 3, input was **118 tokens**.
**Say:** "Keep the meaning and drop the full transcript. The summarizer is a cheap call on a small model."

### Demo 5: Store state externally · `python demo05_external_state.py`
The script stores every fact in a database and retrieves only the profile and the facts relevant to the question.
It runs on SQLite, and **the video used PostgreSQL**. **Say:** "Write everything to storage and read only the slice this turn needs."

### Demo 6: Cap the output, and say so in the prompt · `python demo06_cap_output.py`
| Run | Result |
|---|---|
| A) Unrestricted | Long answer and expensive output |
| B) `max_completion_tokens=200` only | `finish_reason=length`, so the answer is **cut off mid-sentence** |
| C) Cap plus matching instruction | Short and complete |

**Video numbers:** **93** tokens restricted vs **675** unrestricted (Foundry playground, GPT-5.4 mini).
**Say:** "The cap is the safety net. The instruction is what makes the answer fit. Use evaluations to choose the limit."
*Gotcha:* on GPT-5 models, the cap also includes hidden reasoning tokens, so keep `REASONING_EFFORT` low.

## Option 2: Use the discount (prompt caching) (8 min)

### Demo 7: Automatic prefix caching · `python demo07_prompt_caching.py`
- The static prefix (a system prompt plus a policy document of about 2,000 tokens) goes **first**, and the question goes **last**.
- Watch `cached_tokens` go from **0 on call 1** to most of the prefix on calls 2 and 3.
- Anti-pattern: put a timestamp in front of the prefix, and the cache misses.

**Say:** "The first call pays to write the cache. Later calls pay **about 10% of the normal input price**
for the cached part. But the prefix has to match exactly."

### Demo 7b (optional): Explicit `cache_control` · `python demo07b_cache_control.py`
This is the pattern the video showed: each static block (system prompt, tool definitions, session RAG documents) is marked
`"cache_control": {"type": "ephemeral"}`. Show `cache_creation_input_tokens` on call 1 and `cache_read_input_tokens`
on call 2. *It needs a Claude deployment in Foundry, so skip it if you don't have one.*

### Demo 7c: Semantic cache for FAQs · `python demo07c_semantic_cache.py`
Similar questions (*"forgot my password"*) are answered from the cache with **0 LLM tokens**.
**Say:** "You trade compute for storage, and storage is almost always cheaper. Mention the downsides too:
latency as history grows, and exact-match requirements for prompt caching."

## Option 3: Compare prices (choose the right model) (12 min)

### Demo 8: Large vs small model · `python demo08_compare_models.py`
The same simple and complex task runs on both models, with a cost and latency summary.
Then **switch to the Foundry portal**, go to **Model catalog**, open **Compare**, and select GPT-5.4 vs GPT-5.4 mini.
**Video numbers:** quality **0.81 vs 0.67**, and mini is **72% cheaper**.
Open the **leaderboard** to show the quality vs cost and latency vs complexity trade-offs.
**Say:** "The lowest price per token isn't always the lowest total cost. A cheap model that needs retries can cost more."

### Demo 9: Model Router · `python demo09_model_router.py`
Six prompts, from 'translate good morning' to 'prove √2 is irrational', all go to **one endpoint**. `r.model` shows
which model answered, and a bar chart shows the distribution.
Then change the routing mode on the deployment (**Balanced → Cost → Quality**) and run it again.

## Option 4: Stop sending what isn't needed (tools) (8 min)

### Demo 10A: Measure tool bloat in code · `python demo10_tool_bloat.py`
30 tool definitions are sent with every call, compared with a router that sends only the relevant ones. Both agents
choose `list_products`, and the input tokens drop sharply.

### Demo 10B: Foundry Toolbox (portal)
Run *"Show me our product catalog."* in two playground agents, **A without Toolbox** and **B with Toolbox**,
then open **agent run details** for each.
**Video numbers:** **about 4,700 vs 467 tokens**, roughly **90% fewer input tokens** with no loss in quality
(the toolbox in the video had 30 tools plus 3 Azure Functions).
**Say:** "Toolbox works like a router for tools: it sends only what the request needs."

## Option 5: Invest to improve (10 min)

### Demo 11: Agent Optimizer · see `demo11_agent_optimizer.md`
Run `azd ai agent optimize` in the VS Code terminal. It iterates over prompt, model and tool configurations against
your evaluators. Show the finished results.
**Video number:** **70% → 90% pass rate**, plus a new agent version built for testing.
**Cost angle:** better prompts and tools can let you move to a **smaller model** at the same quality.

### Demo 12: Data and retrieval quality · `python demo12_retrieval.py`
Ask the same question with the whole document as context and then with only the top 2 chunks: fewer tokens and the same answer.
Then show **Foundry IQ**: one endpoint over several knowledge sources. A small model plans the query, splits it
and routes each part to the right source.
**Also mention:** infrastructure that doesn't use tokens (containers, VMs, databases, storage, networking) also adds to the cost.

---

## Close (5 min): Your options summary · `python cost_calculator.py`

The calculator adds each option one at a time to a baseline at 30M calls per month and shows the cumulative saving.

| Option | Lever | Video result | Question to ask customers |
|---|---|---|---|
| 1. Spend less on each call | Lean prompt, summary, external state, output cap | 300-token preamble; 675 → 93 output | "Do you know your average input tokens per turn, and does it grow?" |
| 2. Use the discount | Prompt and semantic caching | Cache hits at about 10% of input cost | "Is your static content first in the prompt?" |
| 3. Compare prices | Compare, leaderboard, Model Router | Mini 72% cheaper; quality 0.81 vs 0.67 | "Is every request going to your largest model?" |
| 4. Stop sending what isn't needed | Toolbox | 4,700 → 467 tokens | "How many tools does each agent send on every call?" |
| 5. Invest to improve | Agent Optimizer, Foundry IQ | 70% → 90% pass rate | "How do you evaluate cost and quality together?" |

**Final line:** "Tokens are what we build on, but **design determines the bill**. Get the design right and AI costs
become predictable as you scale."
Links: https://ai.azure.com · https://aka.ms/FoundryTokenomics

---

## If something breaks
| Problem | Fix |
|---|---|
| `cached_tokens` stays 0 | Prefix too short (< 1,024 tokens) or not identical, so run again within a few minutes |
| Empty answer in Demo 6 | Reasoning used up the cap, so set `REASONING_EFFORT=low` or raise `OUTPUT_CAP` |
| 429 / quota | Switch `MODEL_SMALL` to another deployment, or use the backup screenshots |
| Cost shows "set price" | Fill in prices.json |
| Router always picks one model | Expected in Cost mode, so show the Quality mode |
