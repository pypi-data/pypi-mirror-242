import setuptools

setuptools.setup(
    name="PyBulma",
    version='0.1.0',
    url="https://gitlab.com/mnealer-public/pybulma",
    author="Marc Nealer",
    author_email="marcnealer@gmail.com",
    license="GNU3",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "jinja2"
    ],
    python_requires=">=3.6"
)
