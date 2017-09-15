class BaseModel:
    def __init__(self):
        """Model is a set of classes to do computation.

        Each model has 2 kinds of members:
            - the options get from receivers (possibly fake inputted options).
            - the result of higher level class (possibly fake inputted result).
        Each model has at least 1 public method:
            - This is the computation result for lower class or views to use.
        """
        pass
