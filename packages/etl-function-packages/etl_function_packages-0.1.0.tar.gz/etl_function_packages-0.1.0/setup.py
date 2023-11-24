from setuptools import setup, find_packages

setup(
    name='etl_function_packages',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'great_expectations==0.18.3','numpy==1.26.2','pandas==2.1.3','pytz==2023.3.post1','Unidecode==1.3.7'
    ],
    author='Anurag Mishra',
    author_email='anurag.mishra@codvo.ai',
    description='ETL Functions Packages from mage.ai',
    )
