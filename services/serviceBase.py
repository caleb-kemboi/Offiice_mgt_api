class ServiceBase(object):
    manager = None

    def all(self, *args, **kwargs):
        return self.manager.all(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.manager.get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self.manager.filter(*args, **kwargs)

    def create(self, *args, **kwargs):
        return self.manager.create(**kwargs)

    def update(self, uuid, *args, **kwargs):
        data_to_update = self.filter(uuid=uuid)
        return data_to_update.update(**kwargs)