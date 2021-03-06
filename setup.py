from setuptools import setup, find_packages
import os

version = '1.2.1.dev0'

tests_require = ['ftw.testing',
                 'plone.app.testing', ]

setup(name='simplelayout.types.flowplayerblock',
      version=version,
      description="Flow-player support for simplelayout file blocks.",
      long_description=open("README.rst").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/simplelayout.types.flowplayerblock',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplelayout', 'simplelayout.types'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      install_requires=[
        'Plone',
        'setuptools',
        'simplelayout.base',
        'collective.flowplayer',
        'ftw.upgrade',
        ],

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
