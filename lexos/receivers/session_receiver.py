import os
from typing import Optional

from flask import session

import lexos.helpers.constants as const


class SessionReceiver:

    def __init__(self):
        pass

    @property
    def _session_nullable(self) -> Optional[dict]:
        try:
            return dict(session)
        except RuntimeError:
            return None

    @property
    def _session(self) -> dict:
        return dict(session)

    def _get_id_nullable(self) -> Optional[str]:
        if self._session_nullable:
            return self._session_nullable['id']
        else:
            return None

    def _get_id(self) -> str:
        return self._session['id']

    def get_session_folder_nullable(self) -> Optional[str]:
        if self._session_nullable:
            return os.path.join(const.UPLOAD_FOLDER, self._get_id_nullable())
        else:
            return None

    def get_session_folder(self):
        return os.path.join(const.UPLOAD_FOLDER, self._get_id_nullable())
