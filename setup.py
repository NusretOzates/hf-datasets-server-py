from setuptools import find_packages, setup

setup(
    name='datasets_server_py',
    packages=find_packages(include=['datasets_server_py']),
    version='0.1.0',
    description='Python SDK to access the Datasets Server',
    author='Nusret Ozates',
    license='MIT',
    install_requires=["requests", "pydantic"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.3'],
    test_suite='tests',
)