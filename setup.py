# -*- coding: utf-8 -*-

from distutils.core import setup
    
'''
IMPORTANTE: los campos que se describen a continuación deben ser rellenados en su totalidad.
Aquellos campos que NO SE VAYAN A UTILIZAR, se deben BORRAR.
'''


setup(name='fvisbuildinginspections',
      version='0.1',
      author=u'Jesú Gómez',
      author_email='jgomo3@gmail.com',
#      url='',
#      download_url='',
      description='An application for store and process building inspections',
      long_description='',
      package_dir={'':'src'},
      packages=['funvisis', 'funvisis.buildinginspections'],
#      py_modules=[''],
#      provides=[''],
#      keywords='',
#      license='',
      classifiers=['Development Status :: Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6+',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Topic :: Internet',
                   'Topic :: Scientific/Engineering :: GIS',
                  ],
       requires=['Django (>=1.3)'],
     )
