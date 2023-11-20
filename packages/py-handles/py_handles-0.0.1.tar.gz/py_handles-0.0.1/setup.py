from setuptools import setup, find_packages

setup_args = dict(
    name='py_handles',
    version='0.0.1',
    description='Simple manipulative python package.',
    license='MIT',
    packages=find_packages(),
    author='MITdude',
    keywords=['mainpulative', 'python handles']
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
