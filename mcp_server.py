"""MCP Server for Gossip Protocol Skill."""
import json
import sys
from client import GossipCluster

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "simulate_gossip_dissemination",
                            "description": "Simulate epidemic gossip information spread over node swarm",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "num_nodes": {"type": "integer"},
                                    "rounds": {"type": "integer"},
                                    "fanout": {"type": "integer"}
                                },
                                "required": ["num_nodes"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                num = args["num_nodes"]
                nodes = [f"node_{i}" for i in range(num)]
                gossip = GossipCluster(nodes)
                gossip.inject_rumor(nodes[0], "PAYLOAD")
                rounds = args.get("rounds", 5)
                fanout = args.get("fanout", 2)
                for _ in range(rounds):
                    gossip.step_round(fanout=fanout)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps({"dissemination_ratio": gossip.dissemination_ratio("PAYLOAD")})}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
