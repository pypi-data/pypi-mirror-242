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
WuttJamaican -  database configuration
"""

from collections import OrderedDict

import sqlalchemy as sa

from wuttjamaican.util import load_object, parse_bool, parse_list


def engine_from_config(configuration, prefix='sqlalchemy.', **kwargs):
    """
    Construct a new DB engine from configuration.

    This is a wrapper around upstream
    :func:`sqlalchemy:sqlalchemy.engine_from_config()`.

    The purpose of the customization is to allow certain attributes of
    the engine to be driven by config, whereas the upstream function
    is more limited in that regard.  The following in particular:

    * ``poolclass``
    * ``pool_pre_ping``

    If these options are present in the configuration dictionary, they
    will be coerced to appropriate Python equivalents and then passed
    as kwargs to the upstream function.

    An example config file leveraging this feature:

    .. code-block:: ini

       [wutta.db]
       sqlalchemy.url = sqlite:///tmp/default.sqlite
       sqlalchemy.poolclass = sqlalchemy.pool:NullPool
       sqlalchemy.pool_pre_ping = true

    Note that if present, the ``poolclass`` value must be a "spec"
    string, as required by :func:`~wuttjamaican.util.load_object()`.
    """
    config_dict = dict(configuration)

    # convert 'poolclass' arg to actual class
    key = f'{prefix}poolclass'
    if key in config_dict:
        kwargs.setdefault('poolclass', load_object(config_dict[key]))
        del config_dict[key]

    # convert 'pool_pre_ping' arg to boolean
    key = f'{prefix}pool_pre_ping'
    if key in config_dict:
        kwargs.setdefault('pool_pre_ping', parse_bool(config_dict[key]))
        del config_dict[key]

    engine = sa.engine_from_config(config_dict, prefix, **kwargs)

    return engine


def get_engines(config, prefix):
    """
    Construct and return all database engines defined for a given
    config prefix.

    For instance if you have a config file with:

    .. code-block:: ini

       [wutta.db]
       keys = default, host
       default.url = sqlite:///tmp/default.sqlite
       host.url = sqlite:///tmp/host.sqlite

    And then you call this function to get those DB engines::

       get_engines(config, 'wutta.db')

    The result of that will be like::

       {'default': Engine(bind='sqlite:///tmp/default.sqlite'),
        'host': Engine(bind='sqlite:///tmp/host.sqlite')}

    :param config: App config object.

    :param prefix: Prefix for the config "section" which contains DB
       connection info.

    :returns: A dictionary of SQLAlchemy engines, with keys matching
       those found in config.
    """
    keys = config.get(f'{prefix}.keys', usedb=False)
    if keys:
        keys = parse_list(keys)
    else:
        keys = ['default']

    engines = OrderedDict()
    cfg = config.get_dict(prefix)
    for key in keys:
        key = key.strip()
        try:
            engines[key] = engine_from_config(cfg, prefix=f'{key}.')
        except KeyError:
            if key == 'default':
                try:
                    engines[key] = engine_from_config(cfg, prefix='sqlalchemy.')
                except KeyError:
                    pass
    return engines


def get_setting(session, name):
    """
    Get a setting value from the DB.

    Note that this assumes (for now?) the DB contains a table named
    ``setting`` with ``(name, value)`` columns.

    :param session: App DB session.

    :param name: Name of the setting to get.

    :returns: Setting value as string, or ``None``.
    """
    sql = sa.text("select value from setting where name = :name")
    return session.execute(sql, params={'name': name}).scalar()
