# Demo 11 - Agent Optimizer (terminal in VS Code)

Prerequisites: an agent in Microsoft Foundry with **evaluations configured** (the optimizer
optimizes against the evaluators you defined: quality, task adherence, token efficiency, ...).
Start the run BEFORE the session - it takes a while - and show the results live.

```bash
# 1. Sign in and select the project
azd auth login
azd env select <your-env>          # or: azd init in the agent project folder

# 2. (optional) check the AI agent extension is installed / up to date
azd extension list
azd extension upgrade --all

# 3. Run the optimizer (iterates over prompt, model and tool configurations)
azd ai agent optimize
```

What to show:
1. The baseline score of the current agent version.
2. The candidates the optimizer created (prompt / model / tool changes).
3. The best candidate's score versus baseline, and the new agent version it built for testing.
4. The cost angle: a better prompt can let a **smaller model** reach the same pass rate.

Check the exact flags on Friday with `azd ai agent optimize --help` - the extension may be in preview.
