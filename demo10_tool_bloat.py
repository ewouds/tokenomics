"""Demo 10 - Tool definitions are input tokens on EVERY call.

Part A runs the same prompt with 30 tool definitions vs only the relevant ones (a simple local
router that mimics what Foundry Toolbox does for you). Part B = Foundry Toolbox in the portal.
"""
from common import *

banner("DEMO 10 - Tool bloat", "You pay for every tool description, even the ones you don't use")

def tool(name, desc, props):
    return {"type": "function", "function": {"name": name, "description": desc, "parameters": {
        "type": "object", "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
        "required": list(props)[:1]}}}

DOMAINS = {
    "catalog":  ["list_products", "get_product_details", "search_products", "get_product_reviews", "get_product_price"],
    "orders":   ["create_order", "get_order_status", "cancel_order", "list_orders", "update_shipping_address"],
    "returns":  ["start_return", "get_return_status", "get_return_policy", "issue_refund", "print_return_label"],
    "customer": ["get_customer_profile", "update_customer_email", "list_loyalty_points", "redeem_points", "get_invoices"],
    "inventory":["check_stock", "reserve_stock", "list_warehouses", "transfer_stock", "forecast_demand"],
    "support":  ["open_ticket", "get_ticket", "escalate_ticket", "list_faq", "schedule_callback"],
}
TOOLS, TOOL_DOMAIN = [], {}
for domain, names in DOMAINS.items():
    for n in names:
        TOOLS.append(tool(n, f"{n.replace('_', ' ').capitalize()} in the Contoso {domain} system. "
                          f"Use this when the user asks about {domain} related to {n.split('_')[-1]}.",
                          {"id": f"Identifier for the {domain} item", "filter": "Optional filter expression",
                           "locale": "Language code, e.g. en-US"}))
        TOOL_DOMAIN[n] = domain

all_defs = json.dumps(TOOLS)
print(f"{len(TOOLS)} tools -> ~{Y}{count_tokens(all_defs)}{X} tokens of definitions sent with every request\n")

def route(prompt):
    """Toy router: pick the domain(s) whose keywords appear in the prompt. Toolbox does this properly."""
    keywords = {"catalog": ["product", "catalog"], "orders": ["order"], "returns": ["return", "refund"],
                "customer": ["profile", "loyalty", "invoice"], "inventory": ["stock", "warehouse"],
                "support": ["ticket", "help", "callback"]}
    hit = {d for d, kws in keywords.items() if any(k in prompt.lower() for k in kws)} or {"support"}
    return [t for t in TOOLS if TOOL_DOMAIN[t["function"]["name"]] in hit]

prompt = "Show me our product catalog."
msgs = [{"role": "system", "content": "You are Contoso's agent. Use tools when needed."},
        {"role": "user", "content": prompt}]
selected = route(prompt)
for label, tools in [("Agent A: all 30 tools", TOOLS), (f"Agent B: {len(selected)} routed tools", selected)]:
    r, s = chat(msgs, tools=tools)
    calls = [c.function.name for c in (r.choices[0].message.tool_calls or [])]
    u = log_usage(label, r, s)
    print(f"   tool chosen: {G}{calls}{X}\n")
    pause()
print(f"{Y}Same tool chosen, a fraction of the input tokens.{X} "
      "Now switch to the Foundry portal and show Toolbox (agent run details: tokens per run).")
