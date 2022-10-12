import sys
from pathlib import Path

# Code used and modifiedfrom the LEAKER framework for our research. Link: https://github.com/encryptogroup/LEAKER
# Thus same license can be found in the LICENSE file.


# here path.parents[1]` is the same as `path.parent.parent
path = Path(__file__).resolve().parent.parent
sys.path.insert(1, str(path) + '/pq-trees/build')
print(str(path) + '/pq-trees/build')

# pq-trees lib after being added as a submodule in leaker dir
__import__("pq-trees")  # automatic compilation

from pqtree_cpp import PQTree  # pylint: disable=import-error


class PQTreeMaker:
    """
    Class that handles with the functions for the pq tree.
    """

    def __init__(self):
        """
        Init that sets an empty ree.
        """
        self.pq_tree = None

    def setup_pq_tree(self, values):
        """Function that sets up the PQ tree with the information in values.

        :param values: The values that are put into the PQ Tree.
        :return: void.
        """
        self.pq_tree = PQTree(values)

    def reduce_pq_tree(self, values):
        """Method that reduces the tree in a "secure manner". Meaning that if it fails it returns the orignal tree.

        :param values: The values to reduce the tree with.
        :return: Void
        """
        self.pq_tree.SafeReduce(values)

    def get_pq_tree(self):
        """Method that returns the PQ Tree in its current form.

        :return: PQ Tree
        """
        return self.pq_tree
