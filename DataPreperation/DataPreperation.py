# This script prepares the scrapes data for further usage
import json
import glob


# List of Leaders (id's)
LEADER_IDS = {
    "OP12-061", "OP05-022", "P-076", "ST08-001", "OP08-021", "OP03-076", 
    "OP12-001", "OP01-006", "OP05-002", "OP14-060", "ST10-001", "OP10-022",
    "ST29-001", "ST14-001", "OP06-001", "OP03-021", "OP05-041", "OP12-041", 
    "OP04-058", "OP12-020", "OP14-080", "PRB01-001", "EB02-010", "OP02-071", 
    "EB01-040", "ST05-001", "OP01-060", "ST10-003", "OP04-039", "OP10-099", 
    "OP14-001", "OP13-003", "OP10-001", "OP01-062", "OP02-049", "OP13-100", 
    "OP03-058", "OP04-040", "OP06-080", "OP07-097", "OP04-020", "OP12-081", 
    "EB03-001", "OP10-002", "OP14-079", "OP05-001", "OP06-020", "OP03-099", 
    "OP03-022", "OP09-062", "OP11-022", "ST13-002", "OP07-038", "ST22-001", 
    "OP02-002", "OP07-019", "OP12-040", "ST09-001", "OP03-040", "OP08-057", 
    "OP04-019", "OP03-077", "OP08-001", "OP09-061", "OP01-031", "EB01-001", 
    "OP06-042", "OP02-026", "ST04-001", "OP13-002", "OP13-001", "OP01-002", 
    "OP11-041", "OP01-003", "ST06-001", "ST02-001", "OP05-060", "P-011", "OP11-062", 
    "OP06-021", "OP05-098", "OP01-001", "ST11-001", "OP14-040", "ST03-001",
    "OP14-041", "ST01-001", "OP08-058", "OP01-091", "OP13-004", "OP07-059", 
    "ST21-001", "OP01-061", "OP02-001", "OP10-003", "ST12-001", "ST07-001", 
    "OP07-079", "OP09-001", "ST13-001", "OP04-001", "OP03-001", "OP02-025", 
    "OP11-001", "ST13-003", "OP09-042", "OP09-081", "P-047", "EB01-021", 
    "OP14-020", "OP13-079", "OP08-098", "OP02-072", "OP10-042", "OP08-002", 
    "OP06-022", "ST10-002", "P-117", "OP11-021", "OP07-001", "OP02-093", "OP11-040", "OP09-022"}



def infer_leader(deck):
    for card_id in deck.keys():
        if card_id in LEADER_IDS:
            return card_id
    return None

def normalize_leader_id(leader_id):
    # If the leader has a variant suffix like _p1, _p2, _alt, etc.
    if "_" in leader_id:
        return leader_id.split("_")[0]
    return leader_id

def normalize_deck(deck):
    normalized = {}
    for card_id, count in deck.items():
        base_id = card_id.split("_")[0]
        normalized[base_id] = int(count)
    return normalized


all_entries = []


for file in glob.glob("decks/*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

        for entry in data:

            if "deck" not in entry:
                continue

            deck = entry["deck"]

            leader = entry.get("leader", "") or infer_leader(deck)
            if leader is None:
                continue

            # Normalize leader ID
            leader = normalize_leader_id(leader)
            entry["leader"] = leader

            # Normalize deck card IDs (optional but recommended)
            entry["deck"] = normalize_deck(deck)

            all_entries.append(entry)


print("Loaded:", len(all_entries), "decklists")


missing = [e for e in all_entries if not e.get("leader")]
print("Missing leaders:", len(missing))


leaders = {e["leader"] for e in all_entries}
print("Unique leaders:", len(leaders))
print(leaders)

invalid = [e for e in all_entries if e["leader"] not in LEADER_IDS]
print("Invalid leaders:", len(invalid))

# Filtering out any leaders with too few deack list registred
from collections import Counter

# Count decklists per leader
leader_counts = Counter(e["leader"] for e in all_entries)
