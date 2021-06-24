from database.models import User

import datetime
import unittest


class ModelsTest(unittest.TestCase):
    def setUp(self):
        # Test user model
        self.test_user = User()
        self.test_user.discord_id = 123456781234567123
        self.test_user.join_date = datetime.datetime.now()
        self.test_user.level = 12
        self.test_user.experience = 33

    def test_user_model(self):
        try:
            user = User.create(
                self.test_user.discord_id,
                self.test_user.join_date,
                self.test_user.level,
                self.test_user.experience
            )
        except ValueError:
            User.delete(self.test_user.discord_id)
        
        user = User.create(
            self.test_user.discord_id,
            self.test_user.join_date,
            self.test_user.level,
            self.test_user.experience
        )

        self.assertEqual(user.discord_id, self.test_user.discord_id)
        self.assertEqual(user.join_date, self.test_user.join_date)
        self.assertEqual(user.level, self.test_user.level)
        self.assertEqual(user.experience, self.test_user.experience)

        new_join_date = datetime.datetime.now()
        new_level = 5
        new_exp = 2

        User.update(
            self.test_user.discord_id,
            join_date=new_join_date,
            level=new_level,
            experience=new_exp
        )

        user = User.find_one(self.test_user.discord_id)
        self.assertEqual(user.level, new_level)
        self.assertEqual(user.experience, new_exp)
        self.assertEqual(user.join_date, new_join_date)

        User.delete(user.discord_id)
