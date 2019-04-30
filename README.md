# 新雨网站后端

## 依赖

采用 django 模块化开发的方法，如需使用本模块，需启用

```python
['django.contrib.auth', 
 'django.contrib.admin', #后台管理 
 'django.contrib.sessions',
 'rest_framework',
 'rest_framework.authtoken',
 'rest_auth',
 'allauth',
 'allauth.account',
 'rest_auth.registration',
 'corsheaders',# 开发时需要设置跨域请求允许
 'lawyer',
 'import_export' # 后台导出Excel
]
```

在`settings.py`文件，需启用基于token 的验证来支持前后端分离时的调试，

```python
REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES':(
          'rest_framework.authentication.SessionAuthentication',
          'rest_framework.authentication.TokenAuthentication',
      )
 }

```

设置`SITE_ID = 1`支持用户注册相关的后台处理；

设置CORS相关的调试：

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
```

设置中文时区和中文语言
```python
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'
```

在主目录的 ·urlpatterns· 里包含
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('xinyu/', include('lawyer.urls')),
    ...
]
```
## 数据库设计

分律所、律师、学校、课程、班级、课时六张表，其中律师表与`django`自带的user表相关联，便于处理验证相关的请求，班级表目前采用如下的结构：

- 所在的学校
- 班级的序号（如5班）
- 讲课的律师（可为空）

由于普法课程在设计之初与1~2个年级相对应，因此在课程的表里添加了 `grade` 和 `grade_2` 两个字段，从5-8年级中选择。

专门用一个中间表处理班级与课程的多对多的关系，并补充其他信息（课时表）

- 班级ID
- 课程ID
- 开始日期和时间
- 持续时间

## 对外的接口

目前对外的接口主要有：

- 律师注册、登录、修改密码（使用`rest_auth`的库）
- 律师完善个人信息(PUT)和查看个人信息(GET)
- 律师认领和取消认领某门课程（需登录）

### 律所列表
用于律师修改个人信息从指定的列表中选择。

### 课程列表
 查看本学期所有课程（没有访问控制）
GET [root]/class/?page=[page_number]
没有 page 参数默认 page = 1，返回 JSON 格式的数据，其中 results 键对应着实际请求的数据：

```JSON
{
    "count": 100,
    "next": "next url",
    "previous": "previous url",
    "results": []
}
``` 
关于具体的接口路径可查看 `lawyer/urls.py` 文件

## 后端管理文档
[wiki](https://github.com/zhaofeng-shu33/django_xinyu_bg/wiki/backend-admin.py)