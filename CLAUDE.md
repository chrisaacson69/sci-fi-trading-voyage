# sci-fi-trading-voyage — app-local rules

Follows the user-global kernel (`~/.claude/CLAUDE.md`, grounding first) and the vault project SDK
(`Vault/projects/CLAUDE.md`). Vault pointer: `projects/sci-fi-trading-voyage/`.

- `data/market.csv` is the single source of truth for prices and coordinates. Correct typos there,
  never inside the script.
- Every model assumption in README.md cites what measured it. A new assumption (overhead, price
  changes, ship stats) needs the same before it changes a ranking.
- `py -3 trade_routes.py --selftest` must pass before committing. When the snapshot changes, update the
  hand-checked values in `selftest()` from the new prices; don't loosen the checks.
- Paths stay relative to the repo; no machine-specific paths.
