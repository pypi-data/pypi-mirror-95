"""High level API for internationalizing Python libraries and applications."""


from setup_helpers import get_version, require_python
from setuptools import setup, find_namespace_packages


require_python(0x30600f0)
__version__ = get_version('flufl/i18n/__init__.py')


with open('README.rst') as fp:
    readme = fp.read()


setup(
    name='flufl.i18n',
    version=__version__,
    author='Barry Warsaw',
    author_email='barry@python.org',
    description=__doc__,
    long_description=readme,
    long_description_content_type='text/x-rst',
    license='Apache 2.0',
    keywords='internationalization i18n',
    url='https://flufli18n.readthedocs.io',
    download_url='https://pypi.python.org/pypi/flufl.i18n',
    packages=find_namespace_packages(where='.', exclude=['test*', 'docs']),
    namespace_packages=['flufl'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'atpublic',
        'typing_extensions;python_version<"3.8"',
        ],
    project_urls={
        'Documentation': 'https://flufli18n.readthedocs.io',
        'Source': 'https://gitlab.com/warsaw/flufl.i18n.git',
        'Tracker': 'https://gitlab.com/warsaw/flufl.i18n/issues',
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        ],
    )
