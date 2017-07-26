#!/usr/bin/python
# -*- coding: utf-8 -*-

import lexos.helpers.constants as constants
from lexos.application import app
# force matplotlib to use antigrain (Agg) rendering
if constants.IS_SERVER:
    import matplotlib

    matplotlib.use('Agg')


if __name__ == "__main__":
    app.run()
