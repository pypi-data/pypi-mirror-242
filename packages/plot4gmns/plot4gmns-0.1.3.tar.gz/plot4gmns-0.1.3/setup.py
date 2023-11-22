# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, December 28th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    # if have requirements.txt file inside the folder
    with open("requirements.txt", "r", encoding="utf-8") as f:
        modules_needed = [i.strip() for i in f.readlines()]
except Exception:
    modules_needed = []

setuptools.setup(
    name="plot4gmns",  # Replace with your own username
    version="0.1.3",
    author="Dr. Junhua Chen, Zanyang Cui, Xiangyong Luo",
    author_email="cjh@bjtu.edu.cn, zanyangcui@outlook.com, luoxiangyong01@gmail.com",
    description="Plot4GMNS: An open-source academic research tool for visualizing multimodal networks for transportation system modeling and optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyluo25/plot4gmns",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=modules_needed,

    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.xls', '*.xlsx', '*.csv'],
                  "test_data": ['*.xls']},
    project_urls={
        'Homepage': 'https://github.com/asu-trans-ai-lab/plot4gmns',
        'Documentation': 'https://github.com/asu-trans-ai-lab/plot4gmns',
        # 'Bug Tracker': '',
        # 'Source Code': '',
        # 'Download': '',
        # 'Publication': '',
        # 'Citation': '',
        # 'License': '',
        # 'Acknowledgement': '',
        # 'FAQs': '',
        # 'Contact': '',
    }
)