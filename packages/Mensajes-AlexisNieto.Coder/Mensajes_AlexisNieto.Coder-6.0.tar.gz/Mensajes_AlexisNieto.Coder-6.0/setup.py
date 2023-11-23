from setuptools import setup, find_packages

setup(
    name="Mensajes_AlexisNieto.Coder",
    version="6.0",
    description="un paquete para saludar y despedir".title(),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Alexis nieto".title(),
    author_email="alexisnieto.coder@gmail.com",
    url="https://github.com/Aleont18/.git",
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ]
)
