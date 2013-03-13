===============
4.4.1 Templates
===============
.. module:: extra.template

This module can generate file from jinja2 templates. Templates needs to me in
``pymktemplates`` folder with empty ``pymktemplates/__init__.py`` file.

.. function:: mktemplate(template_path, output_file[, data={}])

    Function generates files from jinja2 templates.

    :param template_path: path to a template in the ``pymktemplates`` directory
    :param output_file: path to a output file
    :param data: dict with data inputed to a template
