import random
import typing as T
from multiprocessing.pool import ThreadPool

Summary = T.Mapping[int, int]

def process_votes(
    pile: T.List[int],
    num_workers: int = 4
) -> Summary:
    vote_count = len(pile)
    unit_worklaod = vote_count // num_workers

    vote_piles = [
        pile[i * unit_worklaod : \
             (i+1) * unit_worklaod]
        for i in range(num_workers)
    ]

    with ThreadPool(num_workers) as pool:
        worker_summaries = pool.map(
            process_pile, vote_piles
        )

    total_summary = {}
    for worker_summary in worker_summaries:
        print(f"Votes from staff member: {worker_summary}")
        for candidate, count in worker_summary.items():
            if candidate in total_summary:
                total_summary[candidate] += count
            else:
                total_summary[candidate] = count
    
    return total_summary

def process_pile(pile: T.List[int]) -> Summary:
    summary = {}
    for vote in pile:
        if vote in summary:
            summary[vote] += 1
        else:
            summary[vote] = 1
    return summary

if "__main__" == __name__:
    num_candidates: int = 3
    num_voters:     int = 1000000
    pile = [
        random.randint(1, num_candidates)
        for _ in range(num_voters)
    ]
    counts = process_votes(pile)
    print(f"Total number of votes: {counts}")
