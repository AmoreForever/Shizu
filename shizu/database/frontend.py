from lightdb import LightDB

from typing import  KT, VT

def dbload(func): 
    def f(self, *args, **kwargs):
        self.update(**self._load())
        response = func(self, *args, **kwargs)
        self.update(**self._load())
        return response
    return f

class Database(LightDB):
    """Local database in the file"""
    
    def __repr__(self):
        return object.__repr__(self)
    
    @dbload
    def set(self, name: str, key: KT, value: VT):
        self.setdefault(name, {})[key] = value
        return self.save()

    @dbload
    def get(self, name: str, key: KT, default: VT = None):
        try:
            return self[name][key]
        except KeyError:
            return default
        
    @dbload
    def pop(self, name: str, key: KT = None, default: VT = None):
        if not key:
            value = self[name].pop(name, default)  # Изменил имя переменной
        else:
            try:
                value = self[name].pop(key, default)
            except KeyError:
                value = default

        self.save()
        return value if value is not None else default  # Вернуть value или default

