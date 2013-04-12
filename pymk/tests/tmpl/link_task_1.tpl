from pymk.tests.base import BaseTestTask
from pymk.dependency import FileChanged

class task_linka(BaseTestTask):

    output_file = 'a.out'

    dependencys = [
        FileChanged('a.dep.txt'),
    ]


class task_linkb(BaseTestTask):

    output_file = 'a.out'

    dependencys = [
        FileChanged('b.dep.txt'),
        task_linka.dependency_Link(),
    ]

