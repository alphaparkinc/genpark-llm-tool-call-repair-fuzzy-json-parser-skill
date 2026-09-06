"""
Demonstration of genpark-llm-tool-call-repair-fuzzy-json-parser-skill
"""

from client import ToolCallFuzzyJSONRepairClient

def main():
    repairer = ToolCallFuzzyJSONRepairClient()

    malformed_llm_output = """
Here is the tool call parameter you requested:
```json
{
    'name': 'search_database',
    'parameters': {
        'query': 'machine learning',
        'limit': 10,
        'filters': ['active', 'verified',],
        'is_admin': True,
        'extra_data': None,
```
"""

    res = repairer.parse_tool_call(malformed_llm_output)
    print("=== REPAIRED LLM TOOL CALL PAYLOAD ===")
    print("Status:", res["status"])
    print("Repaired:", res.get("repaired"))
    print("Clean Data:", res.get("data"))

if __name__ == "__main__":
    main()
