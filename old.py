
import numpy as np
import random
from compsoc.profile import Profile


def mod_convergence_rule_v1(profile: Profile, candidate: int) -> int:
    """
    Calculates the score for a candidate based on a profile.
    # epoch implementation

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The score for the candidate.
    :rtype: int
    """
    #useful objects
    tally = [0]*len(profile.candidates)
    epochs = 200 # << hardcoded entry
    iterations = 1000 # << hardcoded entry

    for _ in range(epochs):
        candidate_a = random.choice(list(profile.candidates))
        for __ in range(iterations): 
            ## pick next candidate
            candidate_b = random.choice(list(profile.candidates))
            #compute number who prefer b to a (solution to system of 2 linear equations)
            pref_b_to_a = (profile.get_net_preference(candidate_b,candidate_a) + profile.total_votes) / 2
            prob_pref_b_to_a = pref_b_to_a / profile.total_votes
            draw = random.random()
            if draw < prob_pref_b_to_a:
                candidate_a = candidate_b
            tally[candidate_a] += 1
    # Return the total score
    return tally[candidate]

### Rule 2
def mod_convergence_rule_v2(profile: Profile, candidate: int) -> int:
    """
    Calculates the score for a candidate based on a profile.
    # simulating annealing implementation

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The score for the candidate.
    :rtype: int
    """
    #useful objects
    #useful objects
    tally = [0]*len(profile.candidates)
    #epochs = 200 # << hardcoded entry
    iterations = 200000 # << hardcoded entry
    anneal = 0.1

    #iterate
    candidate_a = random.choice(list(profile.candidates))
    for __ in range(iterations): 
        draw2 = random.random()
        if draw2 < anneal:
            candidate_a = random.choice(list(profile.candidates))
        else: 
            ## pick next candidate
            candidate_b = random.choice(list(profile.candidates))
            #compute number who prefer b to a (solution to system of 2 linear equations)
            pref_b_to_a = (profile.get_net_preference(candidate_b,candidate_a) + profile.total_votes) / 2
            prob_pref_b_to_a = pref_b_to_a / profile.total_votes
            draw = random.random()
            if draw < prob_pref_b_to_a:
                candidate_a = candidate_b
            tally[candidate_a] += 1
    # Return the total score
    return tally[candidate]

