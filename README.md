# Team improbable: COMPSOC 2023


## Voting rule summary

We use ideas from Rank Centrality and Convergence voting to contruct a voting rule. The voting rule uses voter preference orderings to build a Markov Chain between candidates. The score returned by the voting rule is the steady state probabilities for the candidates in the constructed Markov Chain. We refer to our voting rule as Modified Convergence voting.

## Description of Modified Convergence voting

### Construction of the Markov chain

Let $t(i,j)$ denote the transition probability from candidates $i$ to $j$. Let $n$ denote the number of candidates, and $d$ denote a hyper-parameter which is analogous to the damping factor used in PageRank.

We compute $t(i,j)$ where $i \neq j$ as follows: First we compute $p_{ji}$: the proportion of voters who prefer j to i. Then
$$
t(i,j) = 
(1-d) \cdot \frac{p_{ji}}{n-1} 
+d \cdot \frac{1}{n}
$$
Given the computations of $t(i,j)$ where $i \neq j$, $t(i,i)$ is determined by the constraints of the stochastic matrix (rows and columns must add to 1).

### Scores assigned to candidates

Note that this Markov Chain is aperiod and irreducible. Therefore, the exist steady state probabilities corresponding to each candidate. Moreover, we can quickly estimate the steady state probabilities using matrix multiplication. 

The score for candidate $i$ is the steady state probability of candidate $i$.

### Interpretation of Modified Convergence voting

Our Markov chain corresponds to the following thought experiment. Suppose we are at candidate $i$. With probability $d$ we move to a random state. With probability $(1-d)$ we follow the following procedure: we randomly pick a state $j \neq i$ to compare to $i$. We then randomly pick a voter $k$. We move to $j$ if voter $k$ prefers $j$ to $i$, and otherwise we remain at $i$.  

Suppose we repeat this procedure, and record the amount of periods we spend on each candidate. As we increase the periods this procedure runs, the proportion of time we spend on each candidate will stabilise. These proportions correspond to the score given by the voting rule.

## Expected properties of Modified Convergence voting

TBD

## References

- Bana, Gergei, et al. "Convergence Voting: From Pairwise Comparisons to Consensus." arXiv preprint arXiv:2102.01995 (2021).
- Page, Lawrence, et al. The PageRank citation ranking: Bringing order to the web. Stanford InfoLab, 1999.
- Negahban, S., S. Oh, and D. Shah. "Rank centrality: Ranking from pairwise com-parisons." Operations research 65.1 (2016): 266-287.