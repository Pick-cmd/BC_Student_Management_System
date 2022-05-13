# Management_System
for **python divide into groups**


## 模块化设计介绍如下
![模块图 drawio](https://user-images.githubusercontent.com/88447898/168292833-f2181670-0c4f-433e-aba6-d53867d1e022.svg)


### 1 服务器模块
服务器模块的主要起的作用是数据库同客户端的中介，服务器需要做：
- [ ] 使用多线程的方式，同时对多个客户端服务；
- [ ] 使用多线程的方式，并发式访问数据库，解决的临界区访问问题；
- 或者应该是，使用多线程的方式，同时服务多个客户端并且并发式访问数据库；
- 统计相应客户端的数据包括但不限于：在线时间、特殊指标（设置按钮，统计按键点击次数）

类说明：
- 客户端类，包含数据库登录信息
- 线程——接受client请求类，设计一个线程处理
- 线程——并发访问database类，设计一个线程处理

类图：
- [ ] ![服务器类图 drawio](https://user-images.githubusercontent.com/88447898/168303792-0ca5c5b0-d135-4761-8b32-3b228ccbbc62.svg)

eg:创建游标的实例代码
```
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='stu_info',
    charset='utf8',
)
```
### 2 客户端模块
客户端模块主要是GUI页面设计，以及内部数据逻辑的处理，需要做：
- 登录界面设计；
- 不同权限用户主页面的设计（包含权限信息展示）与底层逻辑；

类说明：
- 登录数据包类，包含登录信息；
- 用户类，包含用户信息；
- 数据展示类，多种数据展示的类；

#### 2.1 登录界面
- 界面设计：包含一个下滑式表，用来选择教师、组长或者一般用户，然后是输入用户名和密码的框，最后是登录按钮，参考QQ登录界面，；
- 数据流：客户端根据用户所选所填，将对应的类序列化后通过tcp协议发送给服务器，服务器进行相应信息匹配后，返回登录信号；
- 其它：根据登录信号设计弹窗，登陆失败（及原因）、登陆超时（及原因）、其它；

#### 2.2 用户主页
如果是第一次登陆，需要填写相应的信息，应有一个界面用来填报信息，对于所有用户，都应该展示**身份信息**，**登陆时间戳等杂项**，其余加上：
- 一般用户：展示所属小组信息，展示需要做的任务列表；
- 组长：展示所有组员信息，展示所属小组信息，展示需要做的任务列表；
- 教师：展示所有小组的可展开列表（展开后显示组长的视图）；
- *数据统计界面：展示统计信息*
- *数据维护界面：展示所需修改部分*

### 3 其他模块
- 暂无设计

## 开发者：
**许振华**
**杨光**
**殷嘉材**
