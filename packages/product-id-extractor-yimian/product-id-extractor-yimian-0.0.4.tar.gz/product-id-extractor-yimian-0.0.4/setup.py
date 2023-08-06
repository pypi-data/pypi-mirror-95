import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

# build dist: python setup.py sdist bdist_wheel
# dist upload: twine upload dist/*

setuptools.setup(
  name="product-id-extractor-yimian",
  version="0.0.4",
  author="citrusy",
  author_email="luojunshan@yimian.com.cn",
  description="A tiny package to extract product id",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitlab.yimian.com.cn/dev/product_id_extractor",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)