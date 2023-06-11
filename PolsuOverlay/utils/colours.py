class Colours:
    """
    A class representing the colour configuration of the overlay.
    """
    def __init__(self, data) -> None:
        self.data = data

    
    def __getitem__(self, nb: int) -> None:
        """
        Get a colour from the configuration set in: C:\\Users\\USER\\Polsu\\settings\\data.json

        :param nb: Player reqeueue level index
        :return: A string representing a colour code (hex, e.g. #FFFFFF)
        """
        return self.data[str(nb)]
