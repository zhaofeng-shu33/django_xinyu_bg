from setuptools import setup
setup(
    name="lawyer",
    version="0.1",
    author="zhaofeng-shu33",
    description="backend for xinyu",
    url="https://github.com/zhaofeng-shu33/django_xingyu_bg",
    author_email="616545598@qq.com",
    install_requires=['django', 'djangorestframework', 'django-allauth', 'django-rest-auth'],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django"
    ]
)