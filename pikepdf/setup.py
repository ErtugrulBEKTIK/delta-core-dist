import setuptools

setuptools.setup(
    name='pikepdf',
    version='7.2.0',
    packages=setuptools.find_packages(),
    zip_safe=False,
    package_data={'': ['*.pyi', '*.so']},
    include_package_data=True
)