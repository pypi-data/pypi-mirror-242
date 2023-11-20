# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
WuttJamaican - app handler
"""

from wuttjamaican.util import load_entry_points


class AppHandler:
    """
    Base class and default implementation for top-level app handler.

    aka. "the handler to handle all handlers"

    aka. "one handler to bind them all"

    There is normally no need to create one of these yourself; rather
    you should call :meth:`~wuttjamaican.conf.WuttaConfig.get_app()`
    on the config object if you need the app handler.

    :param config: Config object for the app.  This should be an
       instance of :class:`~wuttjamaican.conf.WuttaConfig`.
    """

    def __init__(self, config):
        self.config = config
        self.handlers = {}

    def make_session(self, **kwargs):
        """
        Creates a new SQLAlchemy session for the app DB.  By default
        this will create a new :class:`~wuttjamaican.db.sess.Session`
        instance.

        :returns: SQLAlchemy session for the app DB.
        """
        from .db import Session

        return Session(**kwargs)

    def short_session(self, **kwargs):
        """
        Returns a context manager for a short-lived database session.

        This is a convenience wrapper around
        :class:`~wuttjamaican.db.sess.short_session`.

        If caller does not specify ``factory`` nor ``config`` params,
        this method will provide a default factory in the form of
        :meth:`make_session`.
        """
        from .db import short_session

        if 'factory' not in kwargs and 'config' not in kwargs:
            kwargs['factory'] = self.make_session

        return short_session(**kwargs)

    def get_setting(self, session, name, **kwargs):
        """
        Get a setting value from the DB.

        This does *not* consult the config object directly to
        determine the setting value; it always queries the DB.

        Default implementation is just a convenience wrapper around
        :func:`~wuttjamaican.db.conf.get_setting()`.

        :param session: App DB session.

        :param name: Name of the setting to get.

        :returns: Setting value as string, or ``None``.
        """
        from .db import get_setting

        return get_setting(session, name)
