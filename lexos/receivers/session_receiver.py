import os
from typing import Optional

from flask import session

import lexos.helpers.constants as const


class SessionReceiver:

    def __init__(self):
        """This is the receiver to pack the information in session."""
        pass

    @property
    def _session_nullable(self) -> Optional[dict]:
        """A non-null safe version of session.

        - if you are not in an request environments this function will return
            a None
        :return: an unsafe nullable session.
        """
        try:
            return dict(session)
        except RuntimeError:
            return None

    @property
    def _session(self) -> dict:
        """A helper property to cast the session into dict.

        :return: a session casted into dict
        """
        return dict(session)

    def _get_id_nullable(self) -> Optional[str]:
        """Return the id possibly None.

        :return: the id of current session, possiblly None
        """
        if self._session_nullable:
            return self._session_nullable['id']
        else:
            return None

    def _get_id(self) -> str:
        """Get the non-nullable id

        :return: This will get the id, cannot be None
        """
        return self._session['id']

    def get_session_folder_nullable(self) -> Optional[str]:
        """Get an nullable version of session folder.

        :return: the path of the session folder, possibly None
        """
        if self._session_nullable:
            return os.path.join(const.UPLOAD_FOLDER, self._get_id_nullable())
        else:
            return None

    def get_session_folder(self) -> str:
        """A none nullable version of session folder.

        :return: The path to the session folder
        """
        return os.path.join(const.UPLOAD_FOLDER, self._get_id_nullable())
