"""Example usage for Gossip Protocol Skill."""
from client import GossipCluster

def main():
    print("Executing Gossip Protocol...")
    nodes = [f"peer_{i}" for i in range(8)]
    cluster = GossipCluster(nodes, seed=42)
    cluster.inject_rumor("peer_0", "BLOCK_SYNC_HASH_991")

    for round_num in range(1, 6):
        cluster.step_round(fanout=2)
        ratio = cluster.dissemination_ratio("BLOCK_SYNC_HASH_991")
        print(f" Round {round_num}: dissemination ratio = {ratio}")

    assert ratio == 1.0, f"Expected 1.0 dissemination, got {ratio}"
    print("Gossip Protocol verified successfully!")

if __name__ == "__main__":
    main()
