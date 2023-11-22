from setuptools import setup, find_packages
from io import open


def read(filename):
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(
   name="crystalpayio",
   version="1.0.5",
   description="Asynchronous wrapper for CrystalPay API",
   long_description=read("README.md"),
   long_description_content_type="text/markdown",
   author="Fsoky",
   author_email="cyberuest0x12@gmail.com",
   url="https://github.com/Fsoky/aiocrystalpay",
   keywords="api crystalpay asyncio crypto",
   packages=find_packages()
)