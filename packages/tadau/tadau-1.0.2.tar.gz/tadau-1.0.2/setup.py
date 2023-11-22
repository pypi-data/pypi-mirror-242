# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
import io

install_requires = []

with io.open("README.rst", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="tadau",
    packages= ["tadau"],
    version="1.0.2",
    author="Google LLC",
    author_email="gps-latam-solutions@googlegroups.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    description="Tadau offers a sample on how to TrAck Downloads, Adaption and Usage of Solutions",
    include_package_data=True,
    python_requires=">=3.7",
    long_description=long_description,
    install_requires=install_requires,
    extras_require={
    },
    license="Apache 2.0",
    url="https://github.com/google/tadau",
)
