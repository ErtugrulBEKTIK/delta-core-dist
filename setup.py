import setuptools

setuptools.setup(
    name='delta_core',
    version='0.0.1',
    author='Ertuğrul BEKTİK',
    author_email='ertugrulbektik99@gmail.com',
    description='A minimal self-contained pybind11 project',
    packages=setuptools.find_packages(),
    url="https://github.com/ErtugrulBEKTIK",
    zip_safe=False,
    package_data={'': ['*.pyi', '*.so']},
    include_package_data=True,
    install_requires=[
        "numpy"
    ]
)
