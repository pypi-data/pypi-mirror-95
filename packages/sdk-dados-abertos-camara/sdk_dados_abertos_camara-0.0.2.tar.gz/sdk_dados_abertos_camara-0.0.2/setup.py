import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='sdk_dados_abertos_camara',
    version='0.0.2',
    author='AcompanhaLegis',
    description='SDK to use Dados Abertos da Camara dos Deputados',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/acompanhalegis/sdk-dados-abertos-camara-py',
    packages=setuptools.find_packages(),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
