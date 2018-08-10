from setuptools import setup, find_packages

VERSION = '1.0'

INSTALL_REQUIRES = [
    'packtools>=2.4.1'
]

DEPENDENCY_LINKS = [
    'git+https://github.com/scieloorg/packtools.git#egg=packtools'
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
    dependency_links=DEPENDENCY_LINKS,
    entry_points="""
    [packtools.catalog]
    packtools_catalog=erudit_catalog:catalog
    packtools_checks=erudit_catalog.checks:StyleCheckingPipeline
    """,
)
