"""Shared helpers for the Tokenomics demo kit.

Configure with environment variables (or a .env file you `source`):
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", )
    AZURE_OPENAI_API_KEY  = os.getenv("AZURE_OPENAI_API_KEY", "<key>")   # or use Entra ID (see below)
    MODEL_LARGE     = os.getenv("MODEL_LARGE", "gpt-5.4")
    MODEL_SMALL     = os.getenv("MODEL_SMALL", "gpt-5.4-mini")
    MODEL_ROUTER    = os.getenv("MODEL_ROUTER", "model-router")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    REASONING_EFFORT = os.getenv("REASONING_EFFORT", "low")   # keeps hidden reasoning tokens small on GPT-5 models; "" to disable
    FOUNDRY_URL     = "https://ai.azure.com"
Prices live in prices.json (fill in current list prices before the session).
"""
import json, os, time
from pathlib import Path
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

HERE = Path(__file__).parent
load_dotenv(HERE / ".env")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://ews-foundry-play.openai.azure.com")
MODEL_LARGE = os.getenv("MODEL_LARGE", "gpt-5.4")
MODEL_SMALL = os.getenv("MODEL_SMALL", "gpt-5.4-mini")
MODEL_ROUTER = os.getenv("MODEL_ROUTER", "model-router")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "low")   # keeps hidden reasoning tokens small on GPT-5 models; "" to disable

# ---------- pretty printing ----------
B, DIM, G, Y, R, C, X = "\033[1m", "\033[2m", "\033[92m", "\033[93m", "\033[91m", "\033[96m", "\033[0m"

def banner(title, subtitle=""):
    print(f"\n{C}{'=' * 72}\n{B}{title}{X}")
    if subtitle:
        print(f"{DIM}{subtitle}{X}")
    print(f"{C}{'=' * 72}{X}")

def pause(msg="Press Enter to continue..."):
    if os.getenv("DEMO_NO_PAUSE") != "1":
        input(f"{DIM}{msg}{X}")

# ---------- client ----------
_client = None
def client():
    global _client
    if _client is None:
        from openai import OpenAI
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
        _client = OpenAI(base_url=f"{endpoint}/openai/v1/",
                         api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"))
    return _client

def chat(messages, model=None, **kwargs):
    """Chat Completions call that returns (response, seconds)."""
    t0 = time.time()
    r = client().chat.completions.create(model=model or MODEL_SMALL, messages=messages, **kwargs)
    return r, time.time() - t0

# ---------- tokens ----------
def count_tokens(text):
    """Local token count with tiktoken (o200k_base = GPT-4o / GPT-5 family)."""
    try:
        import tiktoken
        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except ImportError:  # rough fallback: ~4 characters per token
        return max(1, len(text) // 4)

def show_tokens(text):
    """Print how a string is split into tokens."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        ids = enc.encode(text)
        pieces = [enc.decode([i]) for i in ids]
        print(" | ".join(f"[{p}]" for p in pieces))
        return len(ids)
    except ImportError:
        print("(install tiktoken to see the split)")
        return count_tokens(text)

# ---------- usage & cost ----------
def prices():
    return json.loads((HERE / "prices.json").read_text())

def usage_dict(r):
    u = r.usage
    cached = getattr(getattr(u, "prompt_tokens_details", None), "cached_tokens", 0) or 0
    reasoning = getattr(getattr(u, "completion_tokens_details", None), "reasoning_tokens", 0) or 0
    return {"prompt": u.prompt_tokens, "completion": u.completion_tokens,
            "cached": cached, "reasoning": reasoning, "total": u.total_tokens}

def cost(model, prompt_tokens, completion_tokens, cached_tokens=0):
    """Cost in USD using prices.json. Returns None when no price is configured."""
    p = prices().get(model) or prices().get(model.split("-20")[0])
    if not p or p.get("input") is None:
        return None
    uncached = prompt_tokens - cached_tokens
    cached_price = p.get("cached_input") if p.get("cached_input") is not None else p["input"]
    return (uncached * p["input"] + cached_tokens * cached_price + completion_tokens * p["output"]) / 1_000_000

def fmt_cost(c):
    return f"${c:.6f}" if c is not None else "(set price in prices.json)"

def log_usage(label, r, seconds=None):
    u = usage_dict(r)
    c = cost(r.model, u["prompt"], u["completion"], u["cached"])
    extra = f" cached={G}{u['cached']}{X}" if u["cached"] else ""
    extra += f" reasoning={u['reasoning']}" if u["reasoning"] else ""
    t = f" {seconds:.1f}s" if seconds is not None else ""
    print(f"{B}{label:<28}{X} model={r.model:<22} in={Y}{u['prompt']:>5}{X} out={Y}{u['completion']:>5}{X}{extra} "
          f"cost={fmt_cost(c)}{t}")
    return u
