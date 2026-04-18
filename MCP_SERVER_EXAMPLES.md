# MCP server examples (input → typical output)

These examples match the servers in [`browser_mcp.json`](browser_mcp.json). You run them in the **`app.py`** chat (`uv run app.py`), at the `You:` prompt.

**Note:** Exact assistant wording and tool payloads change with the model, API versions, and live data. Tool **names** and shapes below match the MCP tool schemas; bodies are **illustrative**.

---

## 1. `playwright` — `@playwright/mcp`

Browser automation (navigate, click, type, accessibility snapshot, screenshots, etc.).

### Example A — Open a page

**You (input):**

```text
Use the browser to open https://example.com and tell me the page title from the snapshot.
```

**Typical tool sequence (conceptual):**

1. `browser_navigate` — `{ "url": "https://example.com" }`
2. `browser_snapshot` — `{}` (omit optional fields like `filename`; do not send `null`)

**Illustrative tool result (`browser_snapshot`, excerpt):**

```yaml
- generic [ref=e2]:
  - heading "Example Domain" [level=1] [ref=e3]
  - paragraph [ref=e4]: This domain is for use in documentation examples without needing permission.
  - paragraph [ref=e5]:
    - link "Learn more" [ref=e6] [cursor=pointer]:
      - /url: https://iana.org/domains/example
```

**Typical assistant (output):**

```text
The page shows the heading “Example Domain” and explains it is reserved for documentation examples, with a “Learn more” link to iana.org.
```

### Example B — Google search (recommended pattern)

**You (input):**

```text
Search Google for climate summit 2026 and summarize the first few results.
```

**Typical tool call:**

- `browser_navigate` — `{ "url": "https://www.google.com/search?q=climate+summit+2026" }`
- then `browser_snapshot` to read result snippets.

**Typical assistant (output):** A short summary of visible result titles/snippets (exact text depends on Google’s page at that moment).

---

## 2. `airbnb` — `@openbnb/mcp-server-airbnb`

Listing search and listing details (scraped/public data; respect Airbnb terms of use).

### Example A — Search listings

**You (input):**

```text
Search Airbnb for Paris for 2 adults, check-in 2026-06-01, check-out 2026-06-05, max price 200 per night if the tool supports it.
```

**Typical tool call:**

- `airbnb_search` — e.g.

```json
{
  "location": "Paris, France",
  "checkin": "2026-06-01",
  "checkout": "2026-06-05",
  "adults": 2,
  "maxPrice": 200
}
```

**Illustrative tool result (excerpt):**

```text
Found N listings for Paris…
- Title: … | Price: … | Link: https://www.airbnb.com/rooms/…
- Title: … | Price: … | Link: https://www.airbnb.com/rooms/…
…
```

**Typical assistant (output):** A few listings with titles, rough prices, and **direct links** for the user to open.

### Example B — Listing details

**You (input):**

```text
Get Airbnb listing details for id 12345678, 2 adults, check-in 2026-06-01, check-out 2026-06-05.
```

**Typical tool call:**

- `airbnb_listing_details` — e.g.

```json
{
  "id": "12345678",
  "checkin": "2026-06-01",
  "checkout": "2026-06-05",
  "adults": 2
}
```

**Illustrative tool result (excerpt):** Description, amenities, host snippet, price context, and listing URL (exact fields depend on the server response).

**Typical assistant (output):** A concise summary plus the listing URL.

---

## 3. `duckduckgo-search` — `duckduckgo-mcp-server`

Web search via DuckDuckGo (no browser required for this tool).

### Example — Web search

**You (input):**

```text
Use DuckDuckGo to search for LangChain MCP integration and list 3 relevant links with one-line descriptions.
```

**Typical tool call:**

- `duckduckgo_web_search` — e.g.

```json
{
  "query": "LangChain MCP integration",
  "count": 5,
  "safeSearch": "moderate"
}
```

**Illustrative tool result (excerpt):**

```text
1. Example Site — https://example.com/article
   Snippet: …
2. Another Result — https://…
   Snippet: …
…
```

**Typical assistant (output):** Three bullets with title, URL, and one-line description per result.

---

## Mixed prompt (several servers in one project)

**You (input):**

```text
DuckDuckGo: what is MCP? Then open https://modelcontextprotocol.io in the browser and say what the hero headline is.
```

**Typical flow:**

1. `duckduckgo_web_search` with `query` about MCP.
2. `browser_navigate` to the docs URL.
3. `browser_snapshot` to read the hero text.

**Typical assistant (output):** Short MCP definition from search, then the visible headline from the site.

---

## Reference — tool names used above

| Server (`browser_mcp.json`) | Example tool names |
|----------------------------|--------------------|
| `playwright` | `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, … |
| `airbnb` | `airbnb_search`, `airbnb_listing_details` |
| `duckduckgo-search` | `duckduckgo_web_search` |

For full argument schemas, see your Cursor MCP descriptors under `mcps/` or the upstream package docs for each server.
