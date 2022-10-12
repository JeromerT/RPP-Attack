class Attack:

    def __init__(self) -> None:
        pass

    def get_possible_queries(self, size):
        """
        Function that gets all the possible queries for the given size.
        :param size: The domain size.
        :return: List of the possible queries for the size.
        """
        queries = []
        # Loop over the options and add them to the list.
        for x in range(1, size+1):
            for y in range(x, size+1):
                queries.append((x, y))

        return queries

    def execute_attack(self, ):
        pass