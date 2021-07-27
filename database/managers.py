from .exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from .models import User


def _find_user(discord_id) -> User:
    user = User.objects(discord_id=discord_id)
    if not user:
        raise ObjectNotFoundError(f'User with discord id {discord_id} does not exist')

    return user[0]


# TODO: Test UserManager
class UserManager:
    @staticmethod
    def create(discord_id, **kwargs) -> User:
        try:
            _find_user(discord_id)
            raise ObjectAlreadyExistsError(f'User with id {discord_id} already exists')
        except ObjectNotFoundError:
            user = User(discord_id=discord_id, **kwargs)
            user.validate()
            return user.save()

    @staticmethod
    def find_one(discord_id) -> User:
        return _find_user(discord_id)

    @staticmethod
    def update(discord_id, **kwargs) -> User:
        user = _find_user(discord_id)
        user.update(**kwargs)

        return user

    @staticmethod
    def delete(discord_id):
        user = _find_user(discord_id)
        user.save()
        user.delete()
