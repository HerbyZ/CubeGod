class DatabaseException(Exception):
    """Base database module exception."""
    pass


class ObjectNotFoundError(DatabaseException):
    """Database model object is not found."""
    pass


class ObjectAlreadyExistsError(DatabaseException):
    """
    Object with specified parameters that are marked
    unique already exists.
    """
    pass
