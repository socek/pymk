from mock import patch

from pymk.tests.base import PymkTestCase
from pymk.extra.template import mktemplate, Template


class TemplateTest(PymkTestCase):

    def _init_patchers(self):
        super(TemplateTest, self)._init_patchers()
        self.patchers['cache'] = patch.dict(Template.cache, {})
        self.patchers['PackageLoader'] = patch(
            'pymk.extra.template.PackageLoader')
        self.patchers['Environment'] = patch('pymk.extra.template.Environment')

    def test_get_env(self):
        env = Template().get_env()

        self.assertEqual(env, Template().cache['env'])
        self.mocks['PackageLoader'].assert_called_once_with(
            'pymktemplates', '.')
        loader = self.mocks['PackageLoader'].return_value
        self.mocks['Environment'].assert_called_once_with(loader=loader)
        self.assertEqual(env, self.mocks['Environment'].return_value)

    def test_get_env_with_env(self):
        Template.cache['env'] = 'something'
        env = Template().get_env()

        self.assertEqual('something', env)
        self.assertEqual(0, self.mocks['PackageLoader'].call_count)
        self.assertEqual(0, self.mocks['Environment'].call_count)

    def test_make(self):
        with patch.object(Template, 'get_env') as get_env:
            env = get_env.return_value

            Template().make('template_path', 'output_file', {'data': 1})

            env.get_template.assert_called_once_with('template_path')
            template = env.get_template.return_value
            template.stream.assert_called_once_with(**{'data': 1})
            stream = template.stream.return_value
            stream.dump.assert_called_once_with('output_file')

    def test_mktemplate(self):
        with patch('pymk.extra.template.Template') as Template:
            mktemplate('template_path', 'output_file', 'data')

            Template.assert_called_once_with()
            template = Template.return_value
            template.make.assert_called_once_with(
                'template_path', 'output_file', 'data')
