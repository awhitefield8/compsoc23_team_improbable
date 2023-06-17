import numpy as np
import random
from compsoc.profile import Profile

#copy my submission below
def mod_convergence_rule_v3(profile: Profile, candidate: int) -> int:
    """
    Calculates the score for a candidate based on a profile.
    explicit steady state computation

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The score for the candidate.
    :rtype: int
    """
    #useful objects
    iterations = 100
    anneal = 0.1
    #v = np.zeros(len(profile.candidates)) + (1/len(profile.candidates))
    v = np.array([1] + [0]*(len(profile.candidates) - 1))
    S = np.eye(len(profile.candidates)) #initialise S
    #input edges of stochastic matrix
    for i in range(len(profile.candidates)):
        for j in range(len(profile.candidates)):
            if i == j:
                S[i,j] = 0
            else:
                pref_j_to_i = (profile.get_net_preference(j,i) + profile.total_votes) / 2
                prob_pref_j_to_i = pref_j_to_i / profile.total_votes
                S[i,j] = (1-anneal)*(prob_pref_j_to_i/(len(profile.candidates) - 1)) + (anneal*(1/len(profile.candidates))) #law of total probability
    #add self edges in stochastic matrix
    for i in range(len(profile.candidates)):
        S[i,i] = 1 - sum(S[i])
    #compute steady state 
    v1 = np.matmul(v,np.linalg.matrix_power(S, iterations))
    # Return the total score
    return v1[candidate]