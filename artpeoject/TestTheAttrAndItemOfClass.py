# coding=utf-8
class Foo:
    def __getitem__(self, item):
        print('=====>get')
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        # setattr(self,key,value)

    def __delitem__(self, key):
        self.__dict__.pop(key)


f = Foo()
f.x = 1
print(f.x)
print(f.__dict__)
