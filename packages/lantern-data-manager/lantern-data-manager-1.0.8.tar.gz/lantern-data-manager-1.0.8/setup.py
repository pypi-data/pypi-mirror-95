"""
Lantern Data Manager
"""
from setuptools import find_packages, setup

PACKAGE_VERSION = "1.0.8"

DEPENDENCIES = [
    "elasticsearch==7.9.1",
    "PyJWT==1.7.1",
    "influxdb-client==1.14.0",
]

setup(
    name='lantern-data-manager',
    version=PACKAGE_VERSION,
    url='https://gitlab.com/lantern-tech/lantern-data-manager.git',
    license='BSD',
    author='Lantern Technologies',
    author_email='support@lantern.tech',
    description='Lantern Data Manager Library',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=DEPENDENCIES,
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
