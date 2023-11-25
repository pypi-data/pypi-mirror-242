from setuptools import setup,find_packages

setup(
    name='tb_wrapper',
    version='0.0.1',    
    description='tb wrapper of the thingsboard library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GolDandy7/tb_wrapper',
    author='GolDandy7 and ManuelDeho',
    packages=find_packages(),
    install_requires=['tb_rest_client',
                      'requests',                     
                      ]
)