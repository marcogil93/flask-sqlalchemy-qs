from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="flask_sqlalchemy_qs",
    version="1.0.8",
    description="Generate and manipulate SQLAlchemy filters and sorts from query strings in the URL",
    packages=["flask_sqlalchemy_qs", "flask_sqlalchemy_qs.qs_parser", "flask_sqlalchemy_qs.query"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcogil93/flask-sqlalchemy-qs",
    author="Marco Gil",
    author_email="marcogil93@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Framework :: Flask"
    ],
    install_requires=["sqlalchemy >= 2.0", "flask >= 2.2", "flask-sqlalchemy >= 3.0"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0"],
    },
    python_requires=">=3.7",
)