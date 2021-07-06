from database.managers import UserManager
from database.models import User

import datetime
import pytest


@pytest.fixture
def test_user_model():
    user = User()
    user.discord_id = 1234567891234567
    user.level = 24
    user.experience = 79

    return user


# User model tests

def test_create_user(test_user_model):
    user = UserManager.create(test_user_model.discord_id,
                              level=test_user_model.level,
                              experience=test_user_model.experience)

    assert user.discord_id == test_user_model.discord_id
    assert user.level == test_user_model.level
    assert user.experience == test_user_model.experience


def test_find_user(test_user_model):
    user = UserManager.find_one(test_user_model.discord_id)

    assert user.discord_id == test_user_model.discord_id
    assert user.level == test_user_model.level
    assert user.experience == test_user_model.experience

    try:
        # Try to find user that does not exist
        UserManager.find_one(921939219392193219)
        assert False
    except ValueError:
        assert True


def test_update_user(test_user_model):
    new_level = 5
    new_exp = 20
    new_join_date = datetime.datetime.now() + datetime.timedelta(days=-1.5)

    user = UserManager.find_one({'discord_id': test_user_model.discord_id})
    user.update(level=new_level, experience=new_exp, join_date=new_join_date)

    assert user.level == new_level
    assert user.experience == new_exp
    assert user.join_date == new_join_date


def test_delete_user(test_user_model):
    UserManager.delete(test_user_model.discord_id)

    try:
        UserManager.find_one(test_user_model.discord_id)
        assert False
    except ValueError:
        assert True


def test_bans(test_user_model):
    user = UserManager.create(test_user_model.discord_id)

    test_reason = 'secret reason'*100

    user.ban(test_reason)
    user.unban()
    user.ban()

    user = UserManager.find_one(user.discord_id)
    bans = user.get_bans()

    test_date1 = datetime.datetime.now() - datetime.timedelta(minutes=-10)
    test_date2 = datetime.datetime.now() - datetime.timedelta(minutes=10)

    assert bans[0].is_active
    assert bans[0].reason is None
    assert bans[0].date < test_date1
    assert bans[0].date > test_date2

    assert not bans[1].is_active
    assert bans[1].reason == test_reason
    assert bans[1].date < test_date1
    assert bans[1].date > test_date2

    UserManager.delete(test_user_model.discord_id)
