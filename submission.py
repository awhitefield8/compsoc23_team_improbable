import numpy as np
import random
from compsoc.profile import Profile

#copy my submission below
def mod_convergence_rule(profile: Profile, candidate: int) -> int:
    """
    Calculates the score for a candidate based on a profile.

    :param profile: The voting profile.
    :type profile: VotingProfile
    :param candidate: The base candidate for scoring.
    :type candidate: int
    :return: The my_rule score for the candidate.
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
            #prob_pref_a_to_b = profile.get_net_preference(candidate_b,candidate_a) / profile.total_votes
            #compute number who prefer b to a (solution to system of 2 linear equations)
            pref_b_to_a = (profile.get_net_preference(candidate_b,candidate_a) + profile.total_votes) / 2
            prob_pref_b_to_a = pref_b_to_a / profile.total_votes
            draw = random.random()
            if draw < prob_pref_b_to_a:
                candidate_a = candidate_b
            tally[candidate_a] += 1
    # Return the total score
    return tally[candidate]



