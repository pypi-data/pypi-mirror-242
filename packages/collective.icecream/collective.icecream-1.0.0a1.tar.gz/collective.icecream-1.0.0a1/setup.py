"""Installer for the collective.icecream package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CONTRIBUTORS.md").read(),
        open("CHANGES.md").read(),
    ]
)


setup(
    name="collective.icecream",
    version="1.0.0a1",
    description="An addon for Plone that allow you debug your code using the icecream package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="ale-rt",
    author_email="alessandro.pisa@gmail.com",
    url="https://github.com/collective/collective.icecream",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.icecream/",
        "Source": "https://github.com/collective/collective.icecream",
        "Tracker": "https://github.com/collective/collective.icecream/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=["setuptools", "plone.api", "icecream"],
    extras_require={
        "test": [
            "plone.app.testing",
        ],
    },
    # TODO for Plone 6+ we need to use replace z3c.autoinclude with plone.autoinclude
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
