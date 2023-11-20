from setuptools import setup, find_packages

setup(
    name='mappybyL',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'requests',
    ],
    author='L',
    author_email='pers.gun17@gmail.com',
    description='Mappy는 위치 기반 기능을 제공하는 파이썬 라이브러리로, 주소를 좌표로 변환하는 지오코딩(geocoding), 좌표에서 주소 정보를 얻는 지오로케이션(geolocation), 두 지점 간의 경로를 계산하는 방향(directions) 정보 제공 기능을 포함하고 있습니다.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gunhe17/l-mappy',
)