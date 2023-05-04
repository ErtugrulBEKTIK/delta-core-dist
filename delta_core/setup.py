import setuptools

setuptools.setup(
    name='delta_core',
    version='1.0.0',
    author='Ertuğrul BEKTİK',
    author_email='ertugrulbektik99@gmail.com',
    packages=setuptools.find_packages(),
    url="https://github.com/ErtugrulBEKTIK",
    zip_safe=False,
    package_data={'': ['*.pyi', '*.so']},
    include_package_data=True
)
