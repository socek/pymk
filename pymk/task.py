TASKS = {}

class BaseTask(object):
    conditions = []
    name = None
    output_file = None

    def test_conditions(self):
        make_rebuild = True
        for condition in self.conditions:
            make_rebuild = condition(self)
            if make_rebuild:
                break
        return make_rebuild

    def run(self):
        if self.test_conditions():
            print ' * Building "%s"' %(self.name)
            self.build()
            return True
        else:
            print " * '%s' is up to date" %(self.name)
            return False

    def build(self):
        pass

def TaskDecorator(cls):
    if cls.name:
        name = cls.name
    else:
        name = cls.__name__
    if TASKS.has_key(name):
        raise RuntimeError('Task name %s already exists!' %(name))
    TASKS[name] = cls
    return cls
