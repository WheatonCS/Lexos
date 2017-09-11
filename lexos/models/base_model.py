from flask import request


class BaseModel:
    def __init__(self):
        """This is the base model for all the models

        used to handle requests and other common stuff
        """
        if request.json:  # check request.json (ajax request) first
            self._option = request.json
        elif request.form:  # fall back to request.form (form request)
            self._option = request.form
        else:  # no data send to the back end
            self._option = None

    @property
    def front_end_data(self) -> dict:
        return self._option

    def check_data_exists(self, data_key: str) -> bool:
        """check whether the data key exists in the data sent from front end

        :param data_key: the key of the data
        :return: whether that data key is in the request parameter.
        """
        if not self._option:
            raise KeyError(NO_DATA_SENT_ERROR_MESSAGE)

        return data_key in self._option
