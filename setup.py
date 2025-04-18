from setuptools import setup, find_packages

setup(
    name="autosource",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple event stream simulator for testing and development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autosourcesim",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
