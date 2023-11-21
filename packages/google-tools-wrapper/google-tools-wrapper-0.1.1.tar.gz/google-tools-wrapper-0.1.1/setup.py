from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='google-tools-wrapper',
    version='0.1.1',
    license='MIT License',
    author='João Zacchello',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='xonguinhos@gmail.com',
    keywords=['google tools', 'google finance', 'google api', 'currency conversion'],
    description=u'An unofficial Google Tools wrapper',
    packages=['google_tools'],
    install_requires=['requests', 'bs4'],
)

#comandos:
# criar empacotamento: python.exe setup.py sdist
# enviar para pypi: twine upload dist/*
#pypi-AgEIcHlwaS5vcmcCJDU2MDM5OGRhLTY2NmItNDVlYS04ZWZjLTFlZDE2ZGNmYWM3NAACKlszLCI3MDc0ZjIwNi0xZThhLTRmMTctYjI0Mi1hOTkxN2JjY2RjNzAiXQAABiCS_I9qkaVCYXgDEbTHyWFoKiI3WnrfXJHw2u7syLi_sw