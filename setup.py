import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="symbiotic-StefanoFrazzetto",
    version="0.0.1",
    author="Stefano Frazzetto",
    author_email="stefano.frazzetto@hey.com",
    description="Easily create simbiotic relationships with your smart devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StefanoFrazzetto/symbiotic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
    ],
    python_requires='>=3.8',
)
