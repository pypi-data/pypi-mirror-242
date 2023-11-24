import setuptools

setuptools.setup(
    name="jjstock",
    version="0.0.2",
    license='MIT',
    author="joe",
    author_email="kim_junhan@naver.com",
    description="money tree",
    long_description=open('README.md').read(),
    url="https://blog.naver.com/joendjoy",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)