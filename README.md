# Web-Project

* 计科导第十组网页项目

## 项目动机

* 给电影爱好者提供一个可以查看电影信息的平台

## 功能

* 登录

* 注册

* 搜索

* 收藏

## 技术

### MySql

* 后端采用 `pymysql` + `SQLAlchemy` 实现对数据库的操作

* 数据库中含有两类表，一类是用户信息表，存储用户`id`、`用户名`、`密码`，为一张表

* 另一类是收藏夹表，存储用户收藏的电影界面的编号（电影内容存放在 `static` 文件夹下），为注册用户数量的表，其名称为用户 `id`

### 其它

* `Flask` `jinja2` `html` `css` `javascript`

## 完成过程

* 第一周：查阅资料，熟悉任务，进行分工

* 第二、三周：成员各自完成相应的分工任务

* 第四周：合并

## 分工

* 宋子涵：大部分后端+素材搜集
* 韩昊轩：登录、注册页面
* 冯煊、丁奕中：主页
* 王恺欣：电影信息页面
* 魏博文：结果页面+部分后端
* 杨福祥：个人收藏页面

## 如何使用

> 由于我们小组的网站未使用服务器，故需要在本地运行代码和访问数据库。

* 运行mysql指令，建立数据库：

```sql
CREATE DATABASE user;
use user;
CREATE TABLE `user`.`userinfo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NULL,
  `password` VARCHAR(50) NULL,
  PRIMARY KEY (`id`));
```

* 将app.py中第9行和第14行的123456改成你的mysql数据库的密码，然后运行该py文件，即可生成网站。
