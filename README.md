# 项目目标

- 熟练掌握 Web 应用程序开发流程
- 熟悉 Web 应用常见功能实现步骤
- 熟练掌握 Git 的使用
- 提升源代码阅读能力，BUG调试能力，工具使用能力
- 为后续 Django 项目打好代码基础

## 项目分析

### 新经资讯网

- 一款新闻展示的Web项目，主要为用户提供最新的金融资讯、数据
- 以抓取其他网站数据和用户发布作为新闻的主要来源
- 基于 Flask 框架，以 前后端不分离 的形式实现具体业务逻辑

## 技术实现

- 基于 Python 3.0 + Flask 框架实现
- 数据存储使用 Redis + MySQL 实现
- 第三方扩展：
  - 七牛云：文件存储平台
  - 云通信：短信验证码平台
- 布署：基于ubuntu 16.04系统，使用 Gunicorn + Nginx 进行布署

## 功能模块

- 新闻模块
  - 首页新闻列表
  - 新闻详情
- 用户模块
  - 登录注册/个人信息修改
  - 新闻收藏/发布
- 后台管理

## 具体需求

- 首页

  - 根据分类进行新闻列表展示
  - 上拉加载更多数据
  - 点击新窗口跳转到新闻详情页
  - 顶部显示用户登录信息，未登录显示登录/注册按钮
  - 右侧显示新闻点击排行

- 注册

  - 用户账号为手机号
  - 图片验证码正确后才能发送短信验证码
  - 短信验证码每60秒发送一次
  - 条件出错时有相应的错误提示

- 登录

  - 用手机号与密码登录

  - 错误时有相应的提示

  - 新闻详情

  - 新闻内容 html 数据展示

  - 用户点击收藏可以收藏当前新闻

  - 根据当前登录用户显示收藏状态

  - 用户可以评论该新闻

  - 其他用户可以回复某一条评论

  - 右侧显示新闻点击排行

  - 如果当前新闻由具体作者发布，右侧显示作者信息，并且可以关注作者

- 个人中心

    - 显示个人头像、昵称(未设置时显示为用户手机号)

    - 提供我的关注、我的粉丝入口

    - 提供修改基本资料入口

    - 提供头像设置入口

    - 提供密码修改入口

    - 提供我的收藏入口

    - 提供新闻发布入口

    - 提供我发布的新闻的入口

      

- 个人信息修改

    - 可以修改用户名
    - 可以修改个人头像
    - 登陆手机号不能修改
    - 上传新头像后页面立即显示新头像



- 我的关注
  - 以分页的形式展示数据

  - 每页展示4个我关注的用户

  - 可以在当前页面进行取消关注

  - 点击关注用户的昵称跳转到用户信息页面

    

- 我的收藏
  - 以分页的形式展示数据
  - 按收藏时间倒序排序

- 发布新闻

  - 可以发布新闻
  - 可以将新闻页的图片上传到七牛云
  - 发布完新闻跳转到我的新闻列表页面

- 我发布的新闻

  - 按照发布的时候先后顺序排序，最近新闻排在前面
  - 显示当前我发布新闻的新闻状态
  - 点击审核通过的新闻直接跳转到新闻详情页
  - 审核中的无法点击
  - 未审核通过的新闻可以重新发布
  - 点击审核失败的新闻跳转到新闻发布页面，并填充具体新闻内容

- 查看其他人用户页面

  - 显示他人的头像、昵称、粉丝数
  - 可以点击关注和取消关注按钮进行关注操作
  - 展示他发布的新闻
  - 点击新闻在新窗口中打开展示新闻详情

- 退出

  - 提供退出功能

- 后台-登录

  - 提供后台登录页面
  - 如果当前用户已登录，进入到登录页面之后直接跳转到后台主页

- 后台-用户统计

  - 登录到后台界面之后展示用户统计界面
  - 显示用户总人数
  - 展示当前月用户新增人数
  - 展示当前日新增数

- 后台-新闻审核

  - 展示待审核新闻内容
  - 点击进入新闻审核界面
  - 可以对新闻进行审核
  - 如果审核不通过，需要有拒绝原因

- 新闻版式编辑

  - 进入默认展示所有新闻数据
  - 可以根据新闻标题搜索新闻

- 新闻分类管理

  - 展示所有分类列表
  - 可以添加/修改分类