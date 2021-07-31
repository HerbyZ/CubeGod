from database.exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from database.managers import UserManager
from dataclasses import dataclass

import database
import datetime
import pytest


@dataclass
class TestUserModel:
    discord_id: int
    level: int
    experience: int


database.init()


@pytest.fixture
def test_user_model():
    return TestUserModel(
        discord_id=1234567891234567,
        level=24,
        experience=79
    )


# User model tests

def test_create_user(test_user_model):
    user = UserManager.create(test_user_model.discord_id,
                              level=test_user_model.level,
                              experience=test_user_model.experience)

    assert user.discord_id == test_user_model.discord_id
    assert user.level == test_user_model.level
    assert user.experience == test_user_model.experience
    assert user.on_server

    try:
        UserManager.create(test_user_model.discord_id)
        assert False
    except ObjectAlreadyExistsError:
        assert True


def test_find_user(test_user_model):
    user = UserManager.find_one(test_user_model.discord_id)

    assert user.discord_id == test_user_model.discord_id
    assert user.level == test_user_model.level
    assert user.experience == test_user_model.experience
    assert user.on_server

    try:
        # Try to find user that does not exist
        UserManager.find_one(921939219392193219)
        assert False
    except ObjectNotFoundError:
        assert True


def test_update_user(test_user_model):
    new_level = 5
    new_exp = 20

    user = UserManager.find_one(test_user_model.discord_id)
    user.update(level=new_level, experience=new_exp, on_server=False)

    assert user.level == new_level
    assert user.experience == new_exp
    assert not user.on_server

    new_level = 8
    new_exp = 74

    UserManager.update(user.discord_id, level=8, experience=new_exp, on_server=True)
    user = UserManager.find_one(user.discord_id)

    assert user.level == new_level
    assert user.experience == new_exp
    assert user.on_server


def test_delete_user(test_user_model):
    UserManager.delete(test_user_model.discord_id)

    try:
        UserManager.find_one(test_user_model.discord_id)
        assert False
    except ObjectNotFoundError:
        assert True


def test_bans(test_user_model):
    user = UserManager.create(test_user_model.discord_id)

    test_reason = 'secret reason'*100

    user.ban(test_reason)
    user.unban()
    user.ban()

    user = UserManager.find_one(user.discord_id)
    bans = user.bans

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


def test_imprisonments(test_user_model):
    user = UserManager.create(test_user_model.discord_id)

    test_reason = 'test reason'

    user.imprison(test_reason)
    user.end_imprisonment()
    user.imprison(test_reason*100)

    imprisonments = user.imprisonments

    assert imprisonments[0].is_active
    assert imprisonments[0].reason == test_reason*100

    assert not imprisonments[1].is_active
    assert imprisonments[1].reason == test_reason

    UserManager.delete(user.discord_id)
