class BaseModel:
    def __init__(self):
        """Model is a set of classes to do computation.

        Each model has 2 kinds of members:
            - the options get from receivers (possibly fake inputted options).
            - the result of higher level class (possibly fake inputted result).
        Each model has 1 public method with name "generate"
            - This is the computation result for lower class or views to use.
        """
        pass

    def generate(self):
        """The virtual method to generate result of the model"""
        raise NotImplementedError
