import setuptools

setuptools.setup(
    name="hellofresh_oa_data",
    version="0.3.28",
    author="US OA Team",
    author_email="sca-automation@hellofresh.com",
    long_description="Package with helper function to support functions of OA team in regarding to data",
    url="https://github.com/hellofresh/us-ops-tech-scripts/hellofresh-oa-data",
    packages=setuptools.find_packages(),
    zip_safe=False,
    package_data={'': ['config.yml']},
    include_package_data=True
)
