from setuptools import setup, find_packages


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
            'poogle = poogle.cli:cli'
        ],
    },
    install_requires=['requests>=2.8.1,<2.9', 'click>=6.2,<6.3'],
)
