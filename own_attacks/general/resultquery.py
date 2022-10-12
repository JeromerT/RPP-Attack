
class ResultQuery:
    """Class that holds the code for the resultquery created in our attacks.
    """

    def __init__(self, min_start, max_start, min_end, max_end) -> None:
        """Init to set the initial parameters.

        :param min_start: The minimum start.
        :param max_start: The maximum start.
        :param min_end: The minimum end.
        :param max_end: The maximum end.
        """
        self.min_start = min_start
        self.max_start = max_start
        self.min_end = min_end
        self.max_end = max_end
