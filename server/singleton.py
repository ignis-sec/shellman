instances = {}


def singleton(_class):
    def get_instance(*args, **kwargs):
        if _class not in instances:
            instances[_class] = _class(*args, **kwargs)
        return instances[_class]

    return get_instance


def destroy_all(ignore=None):
    if ignore is None:
        ignore = []
    elif callable(ignore):
        ignore = [ignore]

    remove = []
    for key, value in instances.items():
        if value not in ignore:
            remove.append(key)
    for i in remove:
        del instances[i]
