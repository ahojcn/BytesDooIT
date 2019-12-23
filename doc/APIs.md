<div align=center>
    <img src="../logo.png" width="50%"/>
  <br>
  <h2>
    接口文档
  </h2>
</div>

### util

#### 获取 CSRF Token

**基本格式**

```json
POST
/api/util/csrf_token/
Content-Type: application/json
```

**参数说明**

无

**返回值示例**

```json
{
  status_code: 0,
  msg: 'success',
  data: {
    token: 'xxxx'
  }
}
```

**返回值说明**

无

**备注**

请求后的 request 会向 Cookies 中添加一个 csrftoken 字段，值即为 token，不用单独保存。

在使用其他接口请求时需在 headers 里带上这个 csrftoken。



#### 获取图片验证码

**基本格式**

```json
GET
/api/util/verify_code_img/
```

**参数说明**

| 参数   | 必须 | 类型   | 说明     |
| ------ | ---- | ------ | -------- |
| width  | 否   | string | 图片宽度 |
| height | 否   | string | 图片高度 |

**返回值示例**

![](https://i.loli.net/2019/11/16/gTMXtSLiWy4U7Kc.png)

**返回值说明**

无

**备注**

无

### user

#### 注册

**基本格式**

```json
POST
/api/user/
Content-Type: application/x-www-form-urlencoded
```

**参数说明**

| 参数        | 必须 | 类型   | 说明             |
| ----------- | ---- | ------ | ---------------- |
| username    | 是   | string | 用户名           |
| email       | 是   | string | 邮箱             |
| pwd         | 是   | string | 密码             |
| c_pwd       | 是   | string | 确认密码         |
| verify_code | 是   | string | 验证码           |
| is_agree    | 是   | bool   | 是否同意用户协议 |

**返回值示例**

```json
{
  status_code: 0,
  msg: 'success',
  data: {
    // 用户信息
  }
}
```

**返回值说明**

| 参数            | 类型   | 说明          |
| --------------- | ------ | ------------- |
| user_id         | int    | 用户id        |
| email           | string | 邮箱          |
| gender          | string | 性别          |
| desc            | string | 用户简介/签名 |
| avatar          | string | 头像地址      |
| last_login_time | string | 上次登录时间  |
| level           | int    | 等级          |
| exp_val         | int    | 当前经验值    |
| food_num        | int    | 当前辣条数    |
| is_mute         | bool   | 是否禁言      |
| is_active       | bool   | 是否激活      |

**备注**

用户需查看邮箱激活邮件并点击链接进行激活。

#### 登录

**基本格式**

```json
POST
/api/user/login/
```

**参数说明**

| 参数        | 必须 | 类型   | 说明         |
| ----------- | ---- | ------ | ------------ |
| username    | 否   | string | 用户名       |
| email       | 否   | string | 邮箱         |
| is_email    | 是   | bool   | 是否邮箱登录 |
| pwd         | 是   | string | 密码         |
| verify_code | 是   | string | 验证码       |

**返回值示例**

Xxx

**返回值说明**

xxx

**备注**

无

### post

