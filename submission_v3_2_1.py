import numpy as np
from compsoc.profile import Profile

def mod_convergence_rule_v3_2_1(profile: Profile, candidate: int) -> int:
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
    #hyperperams
    iterations = 100
    anneal = 0.1

    #check if we have already computed steady state
    if 'steady_state' not in list(profile.__dict__.keys()):
        #setup
        v = np.array([1] + [0]*(len(profile.candidates) - 1))
        S = np.eye(len(profile.candidates)) #initialise S
        #input edges of stochastic matrix
        for i in range(len(profile.candidates)):
            for j in range(len(profile.candidates)):
                if i == j:
                    S[i,j] = 0
                else:
                    implied_pref_j = sum([ ((i not in v) and (j in v))*k for k,v in profile.pairs ])  #count profiles where only j
                    implied_pref_i = sum([ ((i in v) and (j not in v))*k for k,v in profile.pairs ])  #count profiles where only i
                    #compute implied net preference
                    implied_net_preference = profile.get_net_preference(j,i)  + implied_pref_j  - implied_pref_i
                    pref_j_to_i = (implied_net_preference + profile.total_votes) / 2
                    prob_pref_j_to_i = pref_j_to_i / profile.total_votes
                    S[i,j] = (1-anneal)*(prob_pref_j_to_i/(len(profile.candidates) - 1)) + (anneal*(1/len(profile.candidates))) #law of total probability
        #add self edges in stochastic matrix
        for i in range(len(profile.candidates)):
            S[i,i] = 1 - sum(S[i])
        #compute steady state 
        v1 = np.matmul(v,np.linalg.matrix_power(S, iterations))
        setattr(profile, 'steady_state', v1)
    else:
        v1 = profile.steady_state
    # Return the total score
    return v1[candidate]
