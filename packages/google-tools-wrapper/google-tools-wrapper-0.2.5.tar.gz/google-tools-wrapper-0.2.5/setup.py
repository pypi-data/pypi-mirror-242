from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='google-tools-wrapper',
    version='0.2.5',
    license='MIT License',
    author='João Zacchello',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='xongsdartx@gmail.com',
    keywords=['google tools', 'google finance', 'google api', 'currency conversion', 'google translator', 'google tradutor'],
    description=u'An unofficial Google Tools wrapper',
    packages=['google_tools'],
    install_requires=['selenium', 'requests', 'bs4'],
)

#comandos:
# criar empacotamento: python.exe setup.py sdist
# enviar para pypi: twine upload dist/*
#pypi-AgEIcHlwaS5vcmcCJDdkZDgwOTA0LWUzODItNGUwNi04ZDY1LTc4NjBjMDQ1ZGFkMQACHFsxLFsiZ29vZ2xlLXRvb2xzLXdyYXBwZXIiXV0AAixbMixbImZlMzVhODZjLTMyNzQtNDAzMS1hYzBmLTEzODJmYWE5YTM0MSJdXQAABiB4PLaxal4j1dPTG8hOMm3scOeAJ55joHz3_aFl9VF1Ew
