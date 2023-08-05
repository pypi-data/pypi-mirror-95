# -*- coding: UTF-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, _
from .choicelists import UploadAreas

class UploadController(dd.Model):

    class Meta(object):
        abstract = True

    def get_upload_area(self):
        return UploadAreas.general

    def get_uploads_volume(self):
        return None

    if dd.is_installed("uploads"):

        show_uploads = dd.ShowSlaveTable(
            'uploads.UploadsByController',
            react_icon_name= "pi-upload",
            button_text=u"🖿")  # u"\u1F5BF"
