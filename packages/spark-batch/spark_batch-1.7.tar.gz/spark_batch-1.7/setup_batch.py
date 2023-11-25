from setuptools import setup, find_packages

setup(
    name="spark_batch",
    version="1.7",
    description="spark_delta_batch for bronze > silve > gold > mart auto",
    author="GunSik Choi",
    author_email="cgshome@gmail.com", 
    packages=find_packages(where="src", exclude=["spark_extension", "spark_extension.*"]),
    package_dir={"":"src"}, 
    package_data={'spark_batch': ['data/shp/*']},
    install_requires=[
        "pyyaml",
        "psycopg2-binary",
        "delta-spark",
        "boto3",
        "pycryptodome",
        "geopandas",        
    ],
)

