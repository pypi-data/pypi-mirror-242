from setuptools import setup, find_packages

setup(
    name='vectordb-orm-pyler',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 여기에 종속성 목록을 넣으세요. 예: 'requests', 'numpy'
        "numpy",
        "pinecone-client",
        "tqdm",
        "protobuf",
    ],
    # 기타 메타데이터
    author='Hyungook Kang',
    author_email='hgkang1226@gmail.com',
    description='clone of vectordb-orm',
    license='MIT',
    keywords='vector db orm',
    url='https://github.com/hgkang1226/vectordb-orm-pyler'
)
