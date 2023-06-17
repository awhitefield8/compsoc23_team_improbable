# Team improbable: COMPSOC 2023


## Motivation of rule

## Constraints

180 seconds per rule. 

## Notes

Kemeny-young as it's pretty elegant. But it's NP-hard, so let's approximate it.

### Approach 1:

#### summary: compute Kemeny-young on subset of voters to save time

#### steps 
- select k voters 
- compute kemeny young ranking
- return result

#### improvements
- first check if pairwise election graph is DAG. If so, return topological order.
- trade off voters and alturnatives (i.e. consider fewer alturnatives)

### Approach 2:

#### summary: work on the full data, approximate winner
- check if pairwise election graph is DAG. If so, return topological order.
- randomly choose k orderings, choose the best

#### improvements
- simulated annealing approach (with greedy search)
- ILP relaxation (e.g. solve with regression)

### Approach 3:
#### summary: We modify convergence voting proposed by Bana, Gergei, et al.



## References

- Bana, Gergei, et al. "Convergence Voting: From Pairwise Comparisons to Consensus." arXiv preprint arXiv:2102.01995 (2021).
