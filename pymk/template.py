from jinja2 import Environment, PackageLoader
_cache = {}


def mktemplate(template_path, output_file, data={}):
    global _cache
    if not 'env' in _cache:
        _cache['env'] = Environment(loader=PackageLoader('pymktemplates', '.'))
    template = _cache['env'].get_template(template_path)
    template.stream(**data).dump(output_file)
