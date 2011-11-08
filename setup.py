from setuptools import setup, find_packages

setup(
    name = 'OSP',
    version = '1.0.1',
    url = 'http://code.google.com/p/osp/',
    author = 'Central Piedmont Community College',
    description = ('Early warning system to improve retention rates '
                   'among high-risk students in higher education '
                   'institutions'),
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Education',
        ('License :: OSI Approved :: GNU Library or Lesser General '
         'Public License (LGPL)'),
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript'
    ]
)
