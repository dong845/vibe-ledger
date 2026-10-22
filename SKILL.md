---
name: vibe-ledger
description: Explain an AI-built ("vibe-coded") app to the person who made it and check it at the same time. Draws the project's files as an interactive flowchart — click a file to read what it does, what calls it, its main functions, its risks and how it came to be — and, from the Claude Code and Codex conversations that built it, keeps a ledger of what was asked for, claimed and put off, each checked against verified code evidence. Renders one offline HTML page (flowchart plus an overview with app map, who-can-see matrix, conversation timeline and call paths). Use when someone wants to understand or sanity-check an app an AI wrote — "explain my app", "how do my files connect", "what did the AI actually build", "is my vibe-coded app safe", "帮我看懂这个 AI 写的项目", "这些文件之间怎么调用的", "检查一下 AI 写的代码有没有问题". Runs locally and sends nothing anywhere.
---

# vibe-ledger

Draws the project's files as a flowchart the user can click through, and turns *what was asked, claimed and put off* into a ledger of promises checked against the code. **Every conclusion carries evidence a script verifies. Anything that fails verification shows as ❓ or "unverified" — it is never shown as fact.**

## Rules

1. **Never invent evidence.** Copy quotes character for character from a reading pack, and code snippets from the file. `check` rejects anything else, and the report shows the rejection.
2. **Only the five questions** (references/five-questions.md): where data lives, what costs money, who can see it, where it is most likely to break, what was put off. Leave cosmetic and feature requests out of the ledger.
3. **A status other than `unknown` needs code or probe evidence.** When unsure, write `unknown`.
4. **Two voices.** Plain text is for someone who cannot read code (an analogy only if it is accurate); dev text names the file and the mechanism. Write both in the run's language (`lang` in `run.json`).
5. **Explanations name only what exists.** Function names are copied from their definitions; a name goes in backticks only if it is in the project. Describe what a file does, not what it should do.
6. **Ask before `retention --set`.** It edits the user's Claude Code settings.
7. **Transcripts are private.** Quote only what a promise or a file's history needs. The digest is already masked; never unmask or repeat a secret.

## Steps

Run everything as `python3 <this skill's folder>/scripts/vl.py …`. Each step prints the exact next command — run it as printed.

1. **Start** — `vl.py start --project <app folder>`. It finds the conversations, writes reading packs, runs the probes, builds the file graph and writes `explain_pack.md`. Read its summary: conversations, candidates, probes, file graph, files to explain, warnings. If it prints a retention line, ask the user (rule 6).
2. **Ledger** — follow references/extraction-guide.md.
   - One reading pack: read it, `probes.json`, `candidates.json` and the code it points at; write `<run>/ledger.json`, including `map`, `access` and `paths`.
   - Several packs: give each pack to its own subagent (or work through them one by one) → `<run>/parts/part_NN.json` with evidence, promises and compromises only.
3. **Explanations** — follow references/explain-guide.md.
   - One group (8 files or fewer): read `explain_pack.md` and every file it lists; write `<run>/explain.json`, including 2–4 `journeys` — what the user does and the files it passes through, in order.
   - Several groups: give each group to its own subagent → `<run>/parts/explain_NN.json`.
4. **Merge** (only if step 2 or 3 wrote parts) — `vl.py merge --project <app folder>`. It merges both kinds of part. Then add `map`, `access` and `paths` to `<run>/ledger.json`, and the `journeys` to `<run>/explain.json`, yourself.
5. **Check** — `vl.py check --project <app folder>`. It verifies `ledger.json` and `explain.json`; it stops if either is missing or malformed. Fix a failed quote, snippet or function line only by copying the real text. Downgrades to ❓, dropped function names and "unverified" purposes are the honest result, not something to work around.
6. **Render** — `vl.py render --project <app folder>`. It compares with the previous finished run of this project by itself and prints what changed (`--compare <run folder>` picks another run, `--no-compare` skips it).
7. **Look** — `vl.py shot --project <app folder>`. It must print `Layout check: … none overlap`. Then open every screenshot: the flowchart reads left to right with no overlapping cards; the selected file's panel explains it; the overview diagrams say what the ledger says; at phone width the panel's text stays inside the screen. (On a phone the flowchart itself is wider than the screen on purpose — it keeps cards readable and pans with a finger — so a graph cut at the right edge is expected.) Fix and re-render if not. If no browser is available, open the HTML and read it.
8. **Tell the user** — the report path; how to read it (start on the flowchart, open a route under “点一下会发生什么” — “What happens when you…” on English pages, click a file, red cards have problems; the 模块 / 数据流 views and a route's 时序图 give the overview, where data goes and the order of calls; “对比上次” shows what changed; “导出” saves a PNG or SVG); if render printed a comparison, say what changed since last time; the counts (✅ ❌ ⚠️ ⏳ ❓); the three most important problems in plain words, each with the fix it suggests; and what the report could not see (the overview's last section).

## When there are no conversations

`start` says so. Leave `promises` empty, still record `map`, `access` and `paths` from the code, write `explain.json` without `history`, and tell the user the report checked the code only.

## Reference

- references/extraction-guide.md — how to write the ledger, with a worked example
- references/explain-guide.md — how to write the file explanations, with a worked example
- references/ledger-schema.md — every ledger field
- references/five-questions.md — what belongs under each question
- references/probes.md — what each probe checks and where it is blind
- references/candidates.md — how candidates are found
