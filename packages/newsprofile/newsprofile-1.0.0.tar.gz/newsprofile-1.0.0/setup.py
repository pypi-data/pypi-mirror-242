from setuptools import setup, find_packages

setup(
  name="newsprofile",
  description="Grpc client for newsprofile",
  version="1.0.0",
  packages=find_packages(
      include=[
          "newsprofile",
      ]
  ),
  install_requires=[
      'grpcio-tools == 1.42.0',
  ],
)
