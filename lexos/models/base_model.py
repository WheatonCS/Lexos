"""This is the base model and other models inherit from this base model."""


class BaseModel:
    """Model is a set of classes to do computation.

    Each model has 2 properties:
        - the options get from receivers (possibly fake inputted options).
        - the result of higher level class (possibly fake inputted result).
    Each model has at least 1 public method:
        - This is the computation result for lower class or views to use.
    """

    def __init__(self):
        """Initialize the class."""
        pass
