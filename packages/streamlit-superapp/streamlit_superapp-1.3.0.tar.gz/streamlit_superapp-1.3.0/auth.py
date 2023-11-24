def is_authenticated(user):
    return user is not None


def not_authenticated(user):
    return user is None
