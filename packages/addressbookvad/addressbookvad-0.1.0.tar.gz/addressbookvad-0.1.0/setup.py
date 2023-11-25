from setuptools import setup, find_namespace_packages

setup(
    name='addressbookvad',
    version='0.1.0',
    description='very helpful address book',
    url='https://github.com/VadimTrubay/Vad_address_book',
    author='TrubayVadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama', 'numexpr'],
    entry_points={'console_scripts': ['addressbookvad=addressbookvad.main:main']}
)