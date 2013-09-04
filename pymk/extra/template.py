from jinja2 import Environment, PackageLoader


class Template(object):
    cache = {}  # yes, this should be "static"

    def get_env(self):
        if not 'env' in self.cache:
            loader = PackageLoader('pymktemplates', '.')
            self.cache['env'] = Environment(loader=loader)
        return self.cache['env']

    def make(self, template_path, output_file, data={}):
        env = self.get_env()
        template = env.get_template(template_path)
        stream = template.stream(**data)
        stream.dump(output_file)


def mktemplate(template_path, output_file, data={}):
    return Template().make(template_path, output_file, data)
