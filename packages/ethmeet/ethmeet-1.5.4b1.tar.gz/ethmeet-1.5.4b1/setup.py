import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ethmeet",
    version="1.5.4-b.1",
    author="Lo Han",
    author_email="lohan.uchsa@protonmail.com",
    description="'ethmeet' stands for 'Ethical Meeting'. A video-communication webdriver library. API compatible with most famous platforms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sourcerer0/ethmeet",
    packages=setuptools.find_packages(),
    keywords="bot firefox automation browser selenium meeting zoom google",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
    scripts=[
        'scripts/gecko_install',
        'scripts/QT_DEVICE',
    ],
    install_requires=[
        'selenium>=3.141.0',
        'urllib3>=1.26.3',
        'cryptography>=3.2'
    ]
)