def get_closest_subclass(typ, types):
    for cls in typ.mro():
        if cls in types:
            return cls
    return None