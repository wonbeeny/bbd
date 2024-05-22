# encoding: utf-8
# author : WONBEEN

from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='bbd',
        version='0.0.1',
        description='Budget Buddy you and i Do for GDR network.',
        url='https://github.com/wonbeeny/bbd',
        install_requires=[
            "gspread>=6.1.1",
            "oauth2client>=4.1.3"
        ],
        author='BBD team',
        author_email='wonbeeny@gmail.com',
        license='Apache-2.0 license',
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        zip_safe=False,
        include_package_data=True,
        package_data={'': ['*.pickle']}
    )
