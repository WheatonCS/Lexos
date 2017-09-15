class BaseModel:
    def __init__(self):
        """Model is a set of classes to do computation.

        Each model has 2 kinds of members:
            - the options get from receivers (possibly fake inputted options).
            - the result of higher level class (possibly fake inputted result).
        Each model has 1 public method with name "generate"
            - This is the computation result for lower class or view to use.
        """
        pass

    def generate(self):
        """The virtual method to generate result of the model"""
        raise NotImplementedError

    def data_exists_in_requests(self, data_key: str) -> bool:
        """check whether the data key exists in the data sent from front end

        :param data_key: the key of the data
        :return: whether that data key is in the request parameter.
        """
        if not self._option:
            raise KeyError(NO_DATA_SENT_ERROR_MESSAGE)

        return data_key in self._option
