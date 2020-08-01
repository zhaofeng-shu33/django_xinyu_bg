from setuptools import setup, find_packages
setup(
    name="lawyer",
    version="0.2",
    packages=find_packages(),
    author="zhaofeng-shu33",
    description="backend for xinyu",
    url="https://github.com/zhaofeng-shu33/django_xingyu_bg",
    author_email="616545598@qq.com",
    install_requires=['django', 'djangorestframework', 'django-allauth', 'django-rest-auth', 'django-import-export'],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3"
    ]
)
