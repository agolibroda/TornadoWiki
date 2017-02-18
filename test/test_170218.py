

class SingletonDecorator:
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance

class foo: pass
foo = SingletonDecorator(foo)

class Top: pass
_Top = SingletonDecorator(Top)


x=foo()
y=foo()
z=foo()
q=_Top()
x.val = 'sausage'
y.val = 'eggs'
z.val = 'spam'
q.val = 'qqqqqqqq'
print(x.val)
print(y.val)
print(z.val)
print(q.val)
print(x is y is z)
print(x is q)