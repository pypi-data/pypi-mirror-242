# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import patch, MagicMock

import sqlalchemy as sa
from sqlalchemy import orm

from wuttjamaican import app, db


class TestAppHandler(TestCase):

    def setUp(self):
        self.config = MagicMock()
        self.app = app.AppHandler(self.config)

    def test_init(self):
        self.assertIs(self.app.config, self.config)
        self.assertEqual(self.app.handlers, {})

    def test_make_session(self):
        session = self.app.make_session()
        self.assertIsInstance(session, db.Session.class_)

    def test_short_session(self):
        short_session = MagicMock()
        mockdb = MagicMock(short_session=short_session)

        with patch.dict('sys.modules', **{'wuttjamaican.db': mockdb}):

            with self.app.short_session(foo='bar') as s:
                short_session.assert_called_once_with(
                    foo='bar', factory=self.app.make_session)

    def test_get_setting(self):
        Session = orm.sessionmaker()
        engine = sa.create_engine('sqlite://')
        session = Session(bind=engine)
        session.execute(sa.text("""
        create table setting (
                name varchar(255) primary key,
                value text
        );
        """))
        session.commit()

        value = self.app.get_setting(session, 'foo')
        self.assertIsNone(value)

        session.execute(sa.text("insert into setting values ('foo', 'bar');"))
        value = self.app.get_setting(session, 'foo')
        self.assertEqual(value, 'bar')
