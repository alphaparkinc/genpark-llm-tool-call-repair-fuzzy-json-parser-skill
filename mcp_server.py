"""
MCP Server for genpark-llm-tool-call-repair-fuzzy-json-parser-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import ToolCallFuzzyJSONRepairClient

client = ToolCallFuzzyJSONRepairClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "repair_and_parse_json",
                        "description": "Repair malformed or truncated LLM tool call JSON string.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "raw_text": {"type": "string"}
                            },
                            "required": ["raw_text"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "repair_and_parse_json":
            res = client.parse_tool_call(args.get("raw_text", ""))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
