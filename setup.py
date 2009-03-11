#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2009 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from setuptools import setup
import ispman

setup(name=ispman.__package__,
      version=ispman.__version__,
      author=ispman.__author__,
      author_email=ispman.__email__,
      url=ispman.__url__,
      download_url='http://python.org/pypi/%s' % ispman.__package__,
      description=ispman.__summary__,
      long_description=ispman.__description__,
      license=ispman.__license__,
      platforms="OS Independent - Anywhere Python and ISPMan is known to run.",
      install_requires = ['Babel'],
      keywords = "ISPMan Control Panel",
      packages=['ispman'],
#      package_data={
#        'tracext.dm': [
#            'templates/*.html',
#            'htdocs/css/*.css',
#            'htdocs/img/*.png',
#            'htdocs/img/*.gif',
#            'htdocs/js/*.js',
#        ]
#      },
      message_extractors = {
        'ispman': [
            ('**.py', 'python', None)
        ],
        'flex': [
            ('**.as', 'javascript', None),
            ('**.mxml', 'javascript', None),
        ]
      },
      entry_points = {
        'distutils.commands': [
            'extract = babel.messages.frontend:extract_messages',
            'init = babel.messages.frontend:init_catalog',
            'compile = babel.messages.frontend:compile_catalog',
            'update = babel.messages.frontend:update_catalog'
        ]
      },
      classifiers=[
          'Development Status :: 5 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ]
)
