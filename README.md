# AI Assistant with MCP, LangChain, and Groq

A small terminal chat app that connects a **Groq** LLM to multiple **MCP (Model Context Protocol)** servers through **[mcp-use](https://github.com/mcp-use/mcp-use)** and **LangChain**. You type natural language; the agent picks tools (browser automation, search, etc.) and runs them for you.

## Features

- **Multi-server MCP** — Configured via `browser_mcp.json` (Playwright browser, Airbnb, DuckDuckGo search).
- **Groq** — Fast inference via `langchain-groq` (`ChatGroq`).
- **Conversation memory** — `MCPAgent` keeps context across turns until you clear it.
- **Robust tool calls** — Custom middleware strips `null` optional arguments so strict MCP servers (e.g. Playwright) do not reject JSON `null` for optional string fields.
- **Browser search hints** — System instructions steer the model toward reliable patterns (e.g. Google: navigate to `https://www.google.com/search?q=...` instead of typing into ambiguous homepage refs).

## Requirements

| Requirement | Notes |
|-------------|--------|
| **Python** | 3.13+ (see `pyproject.toml`) |
| **[uv](https://docs.astral.sh/uv/)** | Used to create the venv and run the app |
| **Node.js** | `npx` must work; MCP servers in this project start via `npx` |
| **Groq API key** | [Groq Console](https://console.groq.com/) |

## Quick start

1. **Clone the repository** (use the exact URL from your GitHub repo page).

2. **Install dependencies**

   ```bash
   cd mcpdemos
   uv sync
   ```

3. **Create a `.env` file** in the project root (this file is gitignored):

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the chat loop**

   ```bash
   uv run app.py
   ```

   First run may download MCP packages through `npx`; allow network access.

## Usage

- Type your request at the `You:` prompt (e.g. open a site, search, or combine steps).
- **`exit`**, **`quit`**, or **`bye`** — Leave the app.
- **`clear`**, **`clear history`**, or **`reset`** — Clear the agent’s conversation memory.

## Configuration

### `browser_mcp.json`

Defines MCP servers in the standard `mcpServers` shape. This project includes:

| Server | Purpose |
|--------|--------|
| **playwright** | `@playwright/mcp` — browser navigate, click, type, snapshot, etc. |
| **airbnb** | `@openbnb/mcp-server-airbnb` |
| **duckduckgo-search** | `duckduckgo-mcp-server` |

You can add/remove servers or change `args`; restart the app after edits.

### `app.py` (knobs you might change)

- **`config_file`** — Path to the MCP JSON config (default: `browser_mcp.json`).
- **`ChatGroq`** — `model`, `max_tokens`, `temperature`.
- **`MCPAgent`** — `max_steps`, `memory_enabled`, `additional_instructions` (browser/search behavior).

## Project layout

| Path | Role |
|------|------|
| `app.py` | Async chat loop, MCP client, middleware, agent setup |
| `browser_mcp.json` | MCP server definitions |
| `main.py` | Minimal entry stub (primary demo is `app.py`) |
| `pyproject.toml` / `uv.lock` | Dependencies and lockfile |

## Troubleshooting

- **`Repository not found` (git)** — Confirm the remote URL matches your GitHub repo slug exactly (including any trailing `.` in the repo name if you created it that way).
- **`429` from Groq** — Rate limit; wait and retry or check [Groq rate limits](https://console.groq.com/docs/rate-limits).
- **Playwright / browser errors** — Ensure Node and `npx` work; first run may install `@playwright/mcp`. For Google searches, the app is tuned to prefer direct `search?q=` URLs to avoid filling non-input elements.
- **Telemetry** — mcp-use may log anonymized telemetry; set `MCP_USE_ANONYMIZED_TELEMETRY=false` in the environment if you want it off.

## License

Specify your license here (e.g. MIT) or add a `LICENSE` file.
