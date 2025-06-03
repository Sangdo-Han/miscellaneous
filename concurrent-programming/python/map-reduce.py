import multiprocessing
import random
from collections import Counter


# --- Map Phase: Process a chunk of votes into a Counter ---
def map_votes(pile_chunk):
    return Counter(pile_chunk)


# --- Reduce Phase: Merge multiple Counters into one ---
def reduce_counters(counter_list):
    result = Counter()
    for counter in counter_list:
        result.update(counter)
    return result


# --- Full map-reduce pipeline ---
def vote_up(pile, num_workers=4):
    vote_count = len(pile)
    chunk_size = vote_count // num_workers
    chunks = [
        pile[i * chunk_size: (i + 1) * chunk_size] if i != num_workers - 1
        else pile[i * chunk_size:]
        for i in range(num_workers)
    ]

    with multiprocessing.Pool(num_workers) as pool:
        mapped = pool.map(map_votes, chunks)

    # Show intermediate map results
    for i, partial in enumerate(mapped):
        print(f"Votes from worker {i}: {{", end="")
        print(", ".join(f"{k}: {v}" for k, v in sorted(partial.items())), end="}\n")

    reduced = reduce_counters(mapped)

    print("Total number of votes: {", end="")
    print(", ".join(f"{k}:{v}" for k, v in sorted(reduced.items())), end="}\n")

    return reduced


if __name__ == "__main__":
    num_candidates = 3
    num_voters = 1_000_000
    random.seed(42)
    pile = [random.randint(1, num_candidates) for _ in range(num_voters)]

    vote_up(pile)
