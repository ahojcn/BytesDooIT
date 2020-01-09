### 评论相关


#### 新增评论

1. 路径

    ```djangourlpath
    api/comment/
    ```

2. 方法

    ```djangourlpath
    POST
    ```

3. 参数

    | 参数名 | 类型 | 必须 | 描述 |
    |---|---|---|---|
    | post_id | int | 否 | 文章id |
    | video_id | int | 否 | 视频id |
    | ref_id | int | 否 | 引用评论id |
    | content | string | 是 | 评论内容 |
 
4. 响应

    ```json
    {}
    ```

5. 说明

    需登录后才能新增评论，post_id、video_id二选一。


#### 获取评论

1. 路径

    ```djangourlpath
    api/comment/
    ```

2. 方法

    ```djangourlpath
    GET
    ```

3. 参数

    | 参数名 | 类型 | 必须 | 描述 |
    |---|---|---|---|
    | to | string | 是 | VIDEO/POST |
    | post_id | int | 否 | 文章id |
    | video_id | int | 否 | 视频id |
    | page_index | int | 是 | 分页参数，当前第几页 |
    | page_size | int | 是 | 分页参数，每页多少条 | 

4. 响应

    ```json
    {}
    ```

5. 说明

    无


#### 删除评论

1. 路径

    ```djangourlpath
    api/comment/
    ```

2. 方法

    ```djangourlpath
    DELETE
    ```

3. 参数

    | 参数名 | 类型 | 必须 | 描述 |
    |---|---|---|---|
    | id | int | 是 | 评论id |
 
4. 响应

    ```json
    {}
    ```

5. 说明

    无


#### 喜欢/不喜欢评论

1. 路径

    ```djangourlpath
    api/comment/like/
    ```

2. 方法

    ```djangourlpath
    POST
    ```

3. 参数

    | 参数名 | 类型 | 必须 | 描述 |
    |---|---|---|---|
    | id | int | 是 | 评论id |
    | like | bool | 是 | true 喜欢；false 不喜欢|
 
4. 响应

    ```json
    {}
    ```

5. 说明

    无

