import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='passer_web_client',
    version='v0.3.0',
    author='Daryl.Xu',
    author_email='xuziqiang@zyheal.com',
    description='The client of passer-ground!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://xymedimg.coding.net/public/data-manage-platform/passer-web-client/git',
    packages=setuptools.find_packages(),
    package_dir={'': '.'},
    install_requires=['requests', 'dicomweb-client', 'requests-toolbelt'],
    entry_points={},
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ),
)
