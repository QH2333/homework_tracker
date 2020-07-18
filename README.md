# 作业跟踪器

## 这个工具可以干什么

可以按照课程对作业进行分类，按提交时间对作业进行排序。每项作业都有明确的提交方式和提交时间，不同阶段的作业（普通作业、即将提交的作业、提交截止的作业）按照颜色进行区分。

## 为什么要写这个小工具

出于种种原因，某些老师/助教布置作业时的要求总是让人费解，同学们经常为作业的提交时间而争吵，甚至产生恐慌。

我认为，所有让同学理解作业时产生overhead的老师/助教，都该骂。

可惜能力有限，无法改变现状（如果怼的话，相信老师会让我考虑自己的前途的），只能做一个整合平台，尽力用最直观的方式让人了解作业的布置情况。

## 依赖

本工具使用`Flask`框架编写，并采用`MySQL`作为数据库。在使用前，你可能需要安装`MySQL`数据库以及下面两个Python模块：

```sh
pip install flask
pip install mysql-connector-python
```

## 如何使用

本工具有两种运行模式：作为其他Web服务器的一个后端（WSGI），或独立运行。

不管是哪种方式，你都需要将`config.json.template`更名为`config.json`，并修改里面的配置项，关于每个配置项具体含义的解释如下：

- "db_host": string类型，数据库服务器的IP或域名
- "db_user": string类型，登录数据库时使用的用户名
- "db_passwd": string类型，登录数据库时使用的密码
- "db_name": string类型，存放表的数据库名
- "server_port": number类型，作为独立Flask App运行时的端口号（使用WSGI时将会被忽略）

### 建议使用WSGI，将本工具作为Apache2或Nginx的后端

1. 在MySQL中使用`database.sql`内的DDL语句定义一张表；
2. 把`server.py`配置成WSGI脚本。

### 你也可以将本工具作为一个独立的Flask App运行

1. 在MySQL中使用`database.sql`中的DDL语句定义一张表；
2. 在服务器上直接运行`server.py`。
