class PostyError(RuntimeError):
    pass


class InvalidConfig(PostyError):
    def __init__(self, config_obj, reason):
        msg = 'Invalid config at {}. Reason: {}'.format(
            config_obj.path,
            reason
        )
        super(__class__, self).__init__(msg)


class UnableToImport(PostyError):
    pass


class MalformedInput(PostyError):
    pass
