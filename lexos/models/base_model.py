from flask import request

from lexos.helpers.error_messages import NO_DATA_SENT_ERROR_MESSAGE, \
    INVALID_DATA_KEY_MESSAGE_FORMAT


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

    def get_front_end_data(self, data_key: str):
        """get a data from request

        wrapped in a data to prevent bad request error
        :param data_key: the name (key) of the data you want to get
        :return: the value of the data
        """
        if not self._option:
            raise KeyError(NO_DATA_SENT_ERROR_MESSAGE)

        try:
            return self._option[data_key]
        except KeyError:
            raise KeyError(
                INVALID_DATA_KEY_MESSAGE_FORMAT.format(data_key=data_key))

    def data_exists_in_requests(self, data_key: str) -> bool:
        """check whether the data key exists in the data sent from front end

        :param data_key: the key of the data
        :return: whether that data key is in the request parameter.
        """
        if not self._option:
            raise KeyError(NO_DATA_SENT_ERROR_MESSAGE)

        return data_key in self._option
