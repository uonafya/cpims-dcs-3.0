class Country(object):
    def __init__(self, **kwargs):
        for field in ('id', 'code', 'name'):
            setattr(self, field, kwargs.get(field, None))
