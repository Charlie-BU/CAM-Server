import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User
from database.enums import UserRole
from services.user import userListUsers


class UserDirectoryTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.factory = sessionmaker(bind=self.engine)
        with self.factory() as db:
            db.add_all([
                User(id=1, username='alice', nickname='Alice', email='private@example.com', password='not-public', role=UserRole.GUEST),
                User(id=2, username='bob', nickname=' ', role=UserRole.GUEST),
                User(id=9007199254740993, username='precise', role=UserRole.GUEST),
            ])
            db.commit()

    def tearDown(self):
        self.engine.dispose()

    def test_all_users_paginate_without_private_fields_or_numeric_id_loss(self):
        with self.factory() as db:
            first = userListUsers(db, limit=2)
            second = userListUsers(db, after_id=int(first['next_after_id']), limit=2)
        self.assertEqual(first['items'], [{'cdi_user_id': '1', 'display_name': 'Alice', 'jelly_config': None}, {'cdi_user_id': '2', 'display_name': 'bob', 'jelly_config': None}])
        self.assertTrue(first['has_more'])
        self.assertEqual(second['items'], [{'cdi_user_id': '9007199254740993', 'display_name': 'precise', 'jelly_config': None}])
        self.assertFalse(second['has_more'])
        self.assertEqual(second['next_after_id'], '')

    def test_exact_user_filter_and_missing_user(self):
        with self.factory() as db:
            self.assertEqual(userListUsers(db, user_id=2)['items'][0]['cdi_user_id'], '2')
            self.assertEqual(userListUsers(db, user_id=999)['items'], [])

    def test_route_rejects_invalid_queries(self):
        from subRouters.v1.user import listUsers
        for params in [{'limit':'101'}, {'after_id':'-1'}, {'user_id':'0'}, {'limit':'oops'}]:
            result = asyncio.run(listUsers(SimpleNamespace(query_params=params)))
            self.assertEqual(result.status_code, 400)

    def test_guest_can_read_directory_but_expired_or_deleted_user_cannot(self):
        from authentication import AuthHandler
        handler = AuthHandler(token_getter=SimpleNamespace(get_token=lambda request: 'synthetic'))
        request = SimpleNamespace(url=SimpleNamespace(path='/v1/user/listUsers'))
        with patch('authentication.session', self.factory), patch('authentication.decodeAccessToken', return_value={'id':1}):
            self.assertIsNotNone(handler.authenticate(request))
        with patch('authentication.session', self.factory), patch('authentication.decodeAccessToken', return_value={'id':999}):
            self.assertIsNone(handler.authenticate(request))
        with patch('authentication.decodeAccessToken', side_effect=ValueError('expired')):
            self.assertIsNone(handler.authenticate(request))

    def test_jelly_config_roundtrips_as_json_and_null(self):
        config = {"type": "airjelly.floating-avatar-presets", "schemaVersion": 1,
                  "presets": [{"id": "sample", "appearance": {"variant": "pixel"}}], "customFaces": []}
        with self.factory() as db:
            user = db.get(User, 1)
            user.jelly_config = config
            db.commit()
            db.expire_all()
            self.assertEqual(userListUsers(db, user_id=1)["items"][0]["jelly_config"], config)
            self.assertEqual(db.get(User, 1).toJson()["jelly_config"], config)
            user.jelly_config = None
            db.commit()
            from sqlalchemy import text
            self.assertEqual(db.execute(text('SELECT jelly_config IS NULL FROM "user" WHERE id=1')).scalar(), 1)
