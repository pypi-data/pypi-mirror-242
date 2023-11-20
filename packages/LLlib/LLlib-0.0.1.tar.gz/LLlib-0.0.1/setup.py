from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LLlib",
    version="0.0.1",
    packages=find_packages(),
    description="A simple Python library for creating linked lists and performing operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hnshlr",
    author_email="hanshaller@outlook.fr",
    keywords="linkedlist, listnode, linked list, list node, singly linked list",
    url="https://github.com/Hnshlr/LinkedListLibrary",
    license="MIT",
    include_package_data=True
)
