from setuptools import setup

setup(
    name="comp0034-week8",
    packages=["paralympic_app", "iris_app"],
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        # "pandas",
        # "openpyxl",
        "flask-wtf",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        # "scikit-learn",
    ],
)
