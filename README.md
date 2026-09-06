# GenPark AI Agent Skill - LLM Tool Call Fuzzy JSON Repair

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Fault-tolerant JSON repair engine restoring damaged, truncated, or markdown-polluted tool call payloads from LLMs (Instructor / DirtyJSON inspired).

```mermaid
flowchart TD
    A[Damaged LLM Tool Output] --> B{Valid JSON?}
    B -->|Yes| C[Instant Parse]
    B -->|No| D[Strip Markdown Fences]
    D --> E[Balance Quotes and Braces]
    E --> F[Convert Python Constants & Remove Trailing Commas]
    F --> G[Synthesized Clean JSON Object]
```

## Features
- **Recovers Truncated Streams**: Closes uncompleted brackets and quotes.
- **Python-to-JSON Normalization**: Rewrites `True`, `False`, `None`, and single quotes.
- **Zero External Dependencies**: Standard library Python 3.9+.

## Quickstart
```python
from client import ToolCallFuzzyJSONRepairClient

repairer = ToolCallFuzzyJSONRepairClient()
parsed = repairer.parse_tool_call(malformed_string)
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
