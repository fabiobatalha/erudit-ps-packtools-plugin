from setuptools import setup, find_packages

VERSION = '1.0'

INSTALL_REQUIRES = [
   'packtools>=2.4.0'
]

setup(
    name='EruditCatalog',
    version=VERSION,
    description="Érudit Schema Catalog for Packtools",
    author="Érudit",
    maintainer="Fabio Batalha",
    maintainer_email="fabio.batalha@erudit.org",
    license="BSD License",
    url="http://erudit.org",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite='tests',
    install_requires=INSTALL_REQUIRES,
    entry_points="""
    [packtools.catalog]
    packtools_catalog=erudit_catalog:catalog
    """,
)
