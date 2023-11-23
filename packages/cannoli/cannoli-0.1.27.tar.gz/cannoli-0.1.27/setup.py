from setuptools import setup, find_packages

setup(
    name="cannoli",
    version="0.1.27",
    packages=find_packages(),
    include_package_data=True,  # Corrigido aqui
    install_requires=[
        'openai==0.28.1',
        'pandas',
        'openpyxl'
    ],
    package_data={
        'cannoli': [
            'default_settings.json', 
            'utils/*.py', 
            'datasets/*'
        ],
    },
    author="Narumi Abe, Bruna Luzzi",
    author_email="mail.narumi@gmail.com",
    description="Lib for prompt engineering using OpenAI",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/naruminho/cannoli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
