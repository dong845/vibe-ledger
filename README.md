# vibe-ledger

You built an app by talking to an AI. vibe-ledger reads those conversations (Claude Code and Codex) and the code they produced, and answers five plain questions — **where your data lives, what costs money, who can see it, where it is most likely to break, and what was put off "for later"** — with a clickable flowchart of your files, diagrams and evidence.

It does this as a ledger: everything you asked for, everything the AI said it did and everything it postponed becomes a promise, and each promise is checked against the code. A promise that cannot be backed by code shows as ❓ — never as a fact.

**中文简介**：用 AI 写出了应用、自己却看不懂代码？vibe-ledger 读取你和 AI 的对话记录（Claude Code、Codex）以及当前代码，把“你要的、AI 说做了的、说以后再做的”整理成承诺账本，逐条用代码核对，生成一份带图表的本地报告：数据存在哪、谁能看到、什么会花钱、哪里最容易出事、还欠着什么。

## What you get

- **File flowchart** — every file as a card, laid out left to right from entry points through logic to data and outside services; arrows mean "calls". Click a file to read what it does, what calls it, its main functions, its risks and how it came to be. Red cards have problems; ✦ marks services that charge per use.
- **Three more views** — modules (folders as boxes, for the big picture), data flow (only the paths from an entry to a data store or paid service, each link saying what it sends) and, for any route, a sequence diagram of who calls whom.
- **Compare with the last run** — after the AI changes your app again, new and changed files, new and gone links, new and resolved risks and changed promises are marked.
- **Export** — the map in its current state as a PNG or SVG.
- **App map** — browser, your server, storage and outside services; 💰 marks what charges per use; red marks risk.
- **Who-can-see matrix** — each kind of data against strangers, other users and you; cells that contradict what you asked for are framed in red.
- **Conversation timeline** — what you said, what broke, what the AI changed and what it put off, each linked to where it stands today. Workarounds made just to get past an error are called out.
- **Call paths** (developer view) — what runs, step by step, after one action.
- **The ledger** — every promise with its evidence, and a fix instruction you can paste back to your AI.
- **What it could not see** — conversations it read, files with no conversation behind them, stacks it does not cover.

## Use

In Claude Code (or Codex), with this skill installed, ask: *"explain my app and check it"* / *"帮我看懂这个项目"*. The skill runs:

```
python3 scripts/vl.py start  --project <your app folder>
# the agent writes ledger.json (from the reading packs) and explain.json (from explain_pack.md)
python3 scripts/vl.py check  --project <your app folder>
python3 scripts/vl.py render --project <your app folder>
python3 scripts/vl.py shot   --project <your app folder>
```

The report lands on your Desktop (or Downloads).

## Privacy

Everything runs on your machine; nothing is sent anywhere. Secrets found in conversations or code are masked (`sk-proj-…wXyZ`) everywhere the tool writes, and the report refuses to be written if one slipped through. Working files live in `~/.vibe-ledger`, never inside your project.

Claude Code deletes conversations older than 30 days by default. vibe-ledger keeps a masked copy of each project's conversations and will offer — only with your agreement — to raise that limit.

## Limits

- Conversations: Claude Code and Codex only.
- Deterministic checks cover Next.js, Vite + React, Express, Supabase and Firebase. Other stacks are named in the report as not covered.
- It reads code; it does not run your app.
- The flowchart covers JS/TS and Python files and static imports; it does not trace what runs at runtime.

## Development

```
python3 -m pytest
python3 tests/e2e/prepare.py --out /tmp/vl-e2e   # fixture apps with planted problems
```

License: MIT.
