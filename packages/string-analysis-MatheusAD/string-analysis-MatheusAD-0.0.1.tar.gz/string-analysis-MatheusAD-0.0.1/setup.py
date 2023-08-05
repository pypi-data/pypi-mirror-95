import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="string-analysis-MatheusAD", # Replace with your own username
    version="0.0.1",
    author="Matheus Alves Diniz",
    author_email="matheusad95@gmail.com",
    description="String Stream Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatheusAD95/str_analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'edlib'
    ],
    python_requires='>=3.6',
)
