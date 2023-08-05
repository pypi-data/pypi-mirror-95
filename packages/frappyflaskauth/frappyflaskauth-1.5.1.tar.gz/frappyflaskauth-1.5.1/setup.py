from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappyflaskauth",
      version="1.5.1",
      description="Flask endpoints for user management and authentication.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-flask-authentication",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappyflaskauth"
      ],
      install_requires=[
            "flask",
            "pbu>=0.6.11"
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
