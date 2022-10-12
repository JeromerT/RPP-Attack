from attacks.score_attack_pq_rank import ScoreAttackPQRank
from attacks.score_attack_pq_volume import ScoreAttackPQVolume
from attacks.score_attack_pq import ScoreAttackPQ
from attacks.refined_score_attack_pq import RefinedScoreAttackPQ,RefinedScoreAttackPQRank, RefinedScoreAttackPQVolume


class CombinedAttack(ScoreAttackPQVolume, ScoreAttackPQRank):
    """
    Class that uses both the rank information and the volume information.
    """

    def get_pq_tree_plus_estimates(self, tokens):
        """
        Method that gets the estimated values for the buckets given the observed tokens and leakage.
        :param tokens: The tokens we have observed.
        :return: The created pq tree, the correctly ordered buckets from the pq tree and the range guesses per bucket.
        """

        pqtree, correctly_ordered_buckets, checked_ranges = ScoreAttackPQ.get_pq_tree_plus_estimates(self, tokens)

        if len(self.known_documents) > 0:
            # Refine the ranges based on the volume leakage. This first as it is a more strong refinement step.
            checked_ranges = self.check_known_documents_one_step(correctly_ordered_buckets, checked_ranges)

        if len(self.d_similar) > 0:
            # Refine the ranges based on the rank leakage.
            checked_ranges = self.handle_rank_information(correctly_ordered_buckets, checked_ranges, self.d_similar, self.N)

        return pqtree, correctly_ordered_buckets, checked_ranges


class RefinedCombinedAttack(RefinedScoreAttackPQ, CombinedAttack):
    """
    Class that does the refined variant of the combined attack. It goes in an iterative process then.
    """
    pass
