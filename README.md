# Team improbable: COMPSOC 2023


## Motivation of rule

We modify the Converge voting mechanism proposed by Bana, Gergei, et al. The voting rule uses voter preference orderings to build a Markov Chain between candidates. The score returned by the voting rule is the steady state probabilities for the candidates in the constructed Markov Chain.

## Construction of the Markov chain

Our construction of the Markov chain differs from  Bana, Gergei, et al. We described our construction in this section.

Let $t(i,j)$ denote the transition probability from candidates $i$ to $j$. Let $n$ denote the number of candidates, and $d$ denote a hyper-parameter which is analogous to the damping factor used in PageRank.

We compute $t(i,j)$ where $i \neq j$ as follows: First we compute $p_{ji}$: the proportion of voters who prefer j to i. Then
$$t(i,j) = 
(1-d) \cdot \frac{p_{ji}}{n-1} 
+d \cdot \frac{1}{n}
$$
Given the computations of $t(i,j)$ where $i \neq j$, $t(i,i)$ is determined by the constraints of the stochastic matrix (rows and columns must add to 1).

### Interpretation of the voting rule

Our Markov chain corresponds to the following thought experiment. Suppose we are at candidate $i$. With probability $d$ we move to a random state. With probability $(1-d)$ we follow the following procedure: we randomly pick a state $j \neq i$ to compare to $i$. We then randomly pick a voter $k$. We move to $j$ if voter $k$ prefers $j$ to $i$, and otherwise we remain at $i$.  

## Expected properties of the voting rule

TBD

## Constraints

180 seconds per rule. 

## References

- Bana, Gergei, et al. "Convergence Voting: From Pairwise Comparisons to Consensus." arXiv preprint arXiv:2102.01995 (2021).
- Page, Lawrence, et al. The PageRank citation ranking: Bringing order to the web. Stanford InfoLab, 1999.
