# 作业跟踪器

## 这个工具可以干什么

可以按照课程对作业进行分类，按提交时间对作业进行排序。每项作业都有明确的提交方式和提交时间，不同阶段的作业（普通作业、即将提交的作业、提交截止的作业）按照颜色进行区分。

## 为什么要写这个小工具

出于种种原因，某些学校的老师布置下来的作业总是让人费解，甚至让同学们为作业的提交时间而争吵，甚至产生恐慌。

作者认为，所有让同学理解作业时产生overhead的，都该骂。

可惜能力有限，无法改变现状（如果怼的话，相信老师会让我考虑自己的前途的），只能做一个整合平台，尽力用最直观的方式让人了解作业的布置情况。

## 如何使用

本工具使用`Flask`框架编写，并采用`MySQL`作为数据库。在开始前，你可能需要安装`MySQL`数据库以及下面两个Python模块：

```sh
flask
mysql-connector-python
```

### 建议使用WSGI，将本工具作为Apache2或Nginx的后端

1. 在MySQL中使用`database.sql`内的DDL语句定义一张表；
2. 把`server.py`配置成WSGI脚本。

### 你也可以将本工具作为一个独立的Flask App运行

1. 在MySQL中使用`database.sql`中的DDL语句定义一张表；
2. 在服务器上直接运行`server.py`，使用方法为：

   ``` sh
   server.py --host=<db_host> --user=<db_user> --passwd=<db_password> --dbname=<db_name> --port=<server_port>
   ```

[实例](http://homework.qh2333.com/)