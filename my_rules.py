import numpy as np
import random
from scipy.stats import kendalltau
from compsoc.profile import Profile

from compsoc.voting_rules.borda import borda_rule
from compsoc.voting_rules.copeland import copeland_rule
from compsoc.voting_rules.dowdall import dowdall_rule
from compsoc.voting_rules.simpson import simpson_rule 


### Rule 3
def mod_convergence_rule(profile: Profile, candidate: int) -> int:
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


def mod_convergence_rule2(profile: Profile, candidate: int) -> int:
    """
    Calculates the score for a candidate based on a profile.
    Score is actually the reverse ranking (scores are from 1 to len(profile.candidates) with 1 being the worst)
    The function first runs mod_convergence_rule_v3

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The score for the candidate.
    :rtype: int
    """
    ##set parametrs
    search_steps = 20

    ## run
    v = list(mod_convergence_rule_full_ordering(profile))
    #find implied ordering from v
    current_tuple = [(i,v[i]) for i in profile.candidates]
    current_tuple = sorted(current_tuple, key=lambda x: x[1],reverse=True)
    current_ranking = [i[0] for i in current_tuple]
    current_kt_score = kt_score(current_ranking,profile)
    for s in range(search_steps):
        new_ranking = one_swap(current_ranking,s) #define function and ensure deterministic
        new_kt_score = kt_score(new_ranking,profile)
        if new_kt_score < current_kt_score:
            current_ranking = new_ranking
            current_kt_score = new_kt_score
    return len(profile.candidates) - current_ranking.index(candidate)  #return reverse ranking for candidate



def gen_local_kt_search(profile: Profile, candidate: int) -> int:
    """
    Calculates the score for a candidate based on a profile.
    Score is actually the reverse ranking (scores are from 1 to len(profile.candidates) with 1 being the worst)
    The function first runs some other voting rule - working with Dowdall for now
    Start with Plurality winner, then makes switches that take into account lower order preferences

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The score for the candidate.
    :rtype: int
    """
    ##set parametrs
    search_steps = 20
    ## run
    current_ranking = [i[0] for i in profile.ranking(dowdall_rule)]
    current_kt_score = kt_score(current_ranking,profile)
    for s in range(search_steps):
        new_ranking = one_swap(current_ranking,s) #define function and ensure deterministic
        new_kt_score = kt_score(new_ranking,profile)
        if new_kt_score < current_kt_score:
            current_ranking = new_ranking
            current_kt_score = new_kt_score
    return len(profile.candidates) - current_ranking.index(candidate)  #return reverse ranking for candidate


    












# helper functions for local search on kt distance

def mod_convergence_rule_full_ordering(profile: Profile):
    """
    Calculates a vector of scores for a candidate based on a profile.

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
    return v1


def kt_dist(p1,p2):
    n=len(p1)
    KC,_ = kendalltau(p1,p2)
    KD = ((1 - KC)*(n*(n-1)))/4
    return KD

def kt_score(ordering: list,profile: Profile):
    """
    Compute sum of Kendall tau distance from a ordering to all voters preference orderings
    """
    score = 0
    for pair in profile.pairs:
        score += pair[0]*kt_dist(pair[1],ordering)
    return score

def one_swap(ordering,step=1):
    """
    randomly swap two elements in a list
    """
    new_order = [i for i in ordering]
    #random.seed(step)
    #l = random.randint(0, len(ordering)-2) #pick first elements to swap to right
    l = step % (len(ordering)-1)
    new_order[l], new_order[l + 1] = new_order[l + 1], new_order[l]
    return new_order