import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="touch-callable",
    version="0.1.0",
    author="Peng Weikang",
    author_email="pengwk@pengwk.com",
    description="Automatically generate a Web UI for Python function using type annotations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pengwk/touch-callable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['Flask', 'pytz'],
    setup_requires=['wheel'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['touch-callable=touch_callable.touch_callable:main'],
    }
)
