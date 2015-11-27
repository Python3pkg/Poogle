import os
from setuptools import setup, find_packages


def find_data_files():
    data_files = []

    # for root, dirs, files in os.walk('plugins'):
    #     for name in files:
    #         if name.endswith('.cfg') or name.endswith('.aml'):
    #             data_files.append(os.path.join(root, name))
    #
    # for root, dirs, files in os.walk('config'):
    #     for name in files:
    #         if name.endswith('.cfg'):
    #             data_files.append(os.path.join(root, name))

    return data_files


setup(
    name='Poogle',
    version='0.1.0',
    description='Google search results scraper for Python',
    long_description='Google search results scraper for Python.',
    author='Makoto Fujimoto',
    author_email='makoto@makoto.io',
    url='https://github.com/FujiMakoto/Poogle',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            # 'firefly = firefly.cli:cli',
            # 'firefly-config = firefly.cli.config:cli'
        ],
    },
    install_requires=['', 'requests'],
    package_data={
        'firefly': find_data_files(),
    },
)
