"""
Fault-Tolerant LLM Tool Call JSON Repair and Extraction Engine.
Zero external dependencies, standard library only.
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple

class ToolCallFuzzyJSONRepairClient:
    """
    Recovers valid JSON data structures from damaged LLM tool call outputs:
    - Strips markdown ```json fences
    - Balances unclosed brackets { [ and quotes
    - Fixes trailing commas
    - Replaces Python constants (True/False/None) with JSON standard (true/false/null)
    """

    def __init__(self):
        pass

    def strip_markdown_fences(self, text: str) -> str:
        """Extracts JSON chunk from markdown code blocks or raw prose."""
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if fence_match:
            return fence_match.group(1).strip()
        
        # Look for outer-most braces
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1].strip()

        return text.strip()

    def repair_json_string(self, damaged_str: str) -> str:
        """Applies heuristic transformations to fix common LLM formatting flaws."""
        s = self.strip_markdown_fences(damaged_str)

        # 1. Replace single quotes with double quotes around keys
        s = re.sub(r"(?<=[{\s,])'([a-zA-Z0-9_]+)'\s*:", r'"\1":', s)

        # 2. Replace Python literals
        s = re.sub(r"\bTrue\b", "true", s)
        s = re.sub(r"\bFalse\b", "false", s)
        s = re.sub(r"\bNone\b", "null", s)

        # 3. Strip trailing commas before closing braces/brackets
        s = re.sub(r",\s*([\]}])", r"\1", s)

        # 4. Balance quotes and brackets if truncated
        quote_count = s.count('"') - s.count('\"')
        if quote_count % 2 != 0:
            s += '"'

        open_braces = s.count('{') - s.count('}')
        if open_braces > 0:
            s += '}' * open_braces

        open_brackets = s.count('[') - s.count(']')
        if open_brackets > 0:
            s += ']' * open_brackets

        return s

    def parse_tool_call(self, raw_output: str) -> Dict[str, Any]:
        """
        Attempts direct parse, followed by incremental repair stages.
        Returns parsed dict and repair diagnostics.
        """
        # Stage 1: Fast path
        try:
            parsed = json.loads(raw_output)
            return {"status": "clean", "data": parsed, "repaired": False}
        except Exception:
            pass

        # Stage 2: Heuristic Repair
        repaired_str = self.repair_json_string(raw_output)
        try:
            parsed = json.loads(repaired_str)
            return {"status": "repaired", "data": parsed, "repaired": True, "repaired_string": repaired_str}
        except Exception as e:
            return {"status": "failed", "error": str(e), "repaired_string": repaired_str}
