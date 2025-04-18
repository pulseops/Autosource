from setuptools import setup, find_packages

setup(
    name="autosource",
    version="0.1.0",
    description="Event simulation engine for Pulse's A0-L1 layer",
    author="Pulse Team",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.5.0",
        "PyYAML>=6.0.1",
        "python-dateutil>=2.8.2",
        "faker>=20.0.0",
        "typing-extensions>=4.8.0",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "autosource": ["stories/*.yaml"],
    },
)
