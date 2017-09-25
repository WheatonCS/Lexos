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
