from setuptools import setup
from setuptools import find_packages

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='projectawesome',
      version="0.0.0",
      description="Le Wagon final project",
      license="NA",
      author="Le Wagon DS batch 1615: team awesome",
      author_email="na@na.na",
      #url="https://github.com/lewagon/taxi-fare",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
