from typing import Optional, Dict, Any

from flask import request

RequestData = Dict[str, Any]


class BaseReceiver:
    def __init__(self):
        """This is the base model for all the models.

        used to handle requests and other common stuff
        """
        self._front_end_data_unsafe = self._get_all_options_from_front_end()

    @property
    def _front_end_data(self) -> RequestData:
        """The null-safe version of front end data.

        :return: all the front end data pack in a dict
        """
        assert self._front_end_data_unsafe is not None
        return self._front_end_data_unsafe

    @staticmethod
    def _get_all_options_from_front_end() -> Optional[RequestData]:
        """Get all the options from front end.

        This function is not null-safe:
        (which means this function is possible to return a none).
        :return: a optional dict with data from front end
        """
        if request.json:
            return dict(request.json)
        elif request.form:
            return dict(request.form)
        else:
            return None

    def options_from_front_end(self):
        """A virtual method to get the options"""
        raise NotImplementedError

