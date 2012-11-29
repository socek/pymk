import os

TASKS = {}

class BaseTask(object):
    conditions = []
    name = None
    output_file = None

    @classmethod
    def test_conditions(cls):
        make_rebuild = True
        for condition in cls.conditions:
            make_rebuild = condition(cls)
            if make_rebuild:
                break
        return make_rebuild

    @classmethod
    def run(cls):
        if cls.test_conditions():
            print ' * Building "%s"' %(cls.name)
            cls.build()
            return True
        else:
            print " * '%s' is up to date" %(cls.name)
            return False

    @classmethod
    def build(cls):
        pass

    @classmethod
    def condition_FileExists(cls, task):
        if os.path.exists(cls.output_file):
            return False
        else:
            cls.run()
            return True

    @classmethod
    def condition_FileChanged(cls, task):
        from pymk.condition import FileChanged
        return FileChanged(cls.output_file, cls)(task)

def TaskDecorator(cls):
    if cls.name:
        name = cls.name
    else:
        name = cls.__name__
    if TASKS.has_key(name):
        raise RuntimeError('Task name %s already exists!' %(name))
    TASKS[name] = cls
    return cls
