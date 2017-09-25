from typing import Optional, Dict, Any

from flask import request

RequestData = Dict[str, Any]


class BaseReceiver:
    def __init__(self):
        """This is the base model for all the models.

        used to handle requests and other common stuff
        """
        pass

    @property
    def _front_end_data_nullable(self) -> Optional[dict]:
        """An nullable front-end data

        the front end data, possibly None:
        - if not in an request context, you will get None
        - if no request data is sent in current request, you will get None
        :return: the front end data, possibly None.
        """
        try:
            return self._get_all_options_from_front_end()
        except RuntimeError:  # working out of request context
            return None

    @property
    def _front_end_data(self) -> RequestData:
        """The null-safe version of front end data.

        :return: all the front end data pack in a dict
        """
        assert self._front_end_data_nullable is not None
        return self._front_end_data_nullable

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
        """A virtual method to pack the specific option needed.

        find all the option needed and pack them into a struct.
        Needs to be implemented in other receivers
        """
        raise NotImplementedError
