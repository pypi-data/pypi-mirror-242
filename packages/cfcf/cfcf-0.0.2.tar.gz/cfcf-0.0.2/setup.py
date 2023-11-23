from setuptools import find_packages
from setuptools import setup
import cfcf


def load_description():
    with open('README.md', 'r') as file:
        line = file.readline()
        prev = ''
        while line:
            if prev == '# cfcf\n':
                return line.rstrip()
            prev = line
            line = file.readline()
    return ''


setup(
    name='cfcf',
    version=cfcf.__version__,
    description=load_description(),
    author='tkms',
    author_email='tkmnet.dev@gmail.com',
    url='https://github.com/tkmnet/cfcf',
    packages=find_packages(),
    install_requires=['ulid-py'],
)
