# WeChat Group Message Push

一个基于 Python + 企业微信机器人的自动化群消息推送工具。

支持：

* ☀️ 每日天气播报
* 📅 工作日自动判断
* 💬 每日一句
* 🤖 企业微信群机器人推送
* ⏰ 定时任务自动发送
* 🐳 Docker 部署（可扩展）

适用于：

* 运维通知
* 团队早报
* 自动问候
* 企业内部消息推送
* 自动化办公场景

---

# 项目预览

```text
各位同学早上好!
    今日气温 低温 19℃ - 高温 30℃，天气情况：晴
    温馨提示：愿你拥有比阳光明媚的心情
    每一次挑战都是自我超越的契机，把握它，让自己在成长的道路上不断飞跃。新的一天，早安!
```

---

# 项目特点

* 基于企业微信机器人 Webhook
* 自动获取天气信息
* 自动判断节假日 / 工作日
* 支持每日一句轮播
* 无数据库依赖
* 轻量级部署
* 适合 Linux 定时任务（crontab）
* 代码结构简单，易于二次开发

---

# 技术栈

* Python 3
* requests
* parsel
* 企业微信机器人 Webhook
* 第三方天气 API
* 万年历节假日接口

---

# 项目结构

```bash
.
├── start.py               # 主程序
├── sentence.txt           # 每日一句文本
├── current_index.txt      # 当前句子索引
└── README.md
```

---

# 功能说明

## 1. 工作日自动发送

程序会自动判断：

* 是否为工作日
* 是否为节假日
* 是否为周末

仅在工作日发送消息。

节假日数据来源：

* [https://wannianrili.bmcx.com/](https://wannianrili.bmcx.com/)

---

## 2. 天气获取

当前默认获取：

* 北京天气

天气接口：

```python
http://t.weather.itboy.net/api/weather/city/101010100
```

你可以修改城市 ID 实现其他地区天气推送。

---

## 3. 每日一句

程序会从：

```bash
sentence.txt
```

按顺序读取一句话，并自动循环。

示例：

```text
努力不一定成功，但放弃一定失败。
坚持热爱，奔赴山海。
愿你眼里有光，心中有梦。
```

---

## 4. 企业微信机器人推送

使用企业微信群机器人 Webhook 发送消息。

配置位置：

```python
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"
```

---

# 快速开始

## 1. 克隆项目

```bash
git clone https://github.com/wangzq96/WeChat-group-message-push.git

cd WeChat-group-message-push
```

---

## 2. 安装依赖

```bash
pip install requests parsel
```

或者：

```bash
pip install -r requirements.txt
```


```txt
requests
parsel
```

---

## 3. 配置企业微信机器人

进入企业微信群：

```text
群设置 -> 群机器人 -> 添加机器人
```

获取 Webhook 地址。

修改：

```python
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"
```

---

## 4. 配置每日一句

编辑：

```bash
sentence.txt
```

每行一条内容。

---

## 5. 运行项目

```bash
python start.py
```

---

# Linux 定时任务

使用 crontab 实现每天自动推送。

编辑定时任务：

```bash
crontab -e
```

每天早上 8 点发送：

```bash
0 8 * * * /usr/bin/python3 /opt/WeChat-group-message-push/start.py
```

查看日志：

```bash
tail -f /var/log/cron
```

---

# Docker 部署（推荐）

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install requests parsel

CMD ["python", "start.py"]
```

---

## 构建镜像

```bash
docker build -t wechat-push .
```

---

## 启动容器

```bash
docker run -d --name wechat-push wechat-push
```

---

# 消息流程

```text
获取日期
   ↓
判断是否工作日
   ↓
获取天气
   ↓
读取每日一句
   ↓
拼接消息
   ↓
企业微信机器人推送
```

---

# 常见问题

## 1. 为什么没有收到消息？

检查：

* Webhook 是否正确
* 机器人是否开启
* 网络是否正常
* 是否触发工作日判断

---

## 2. 如何修改城市？

修改：

```python
url = "http://t.weather.itboy.net/api/weather/city/101010100"
```

替换为对应城市 ID。

---

## 3. 如何改成每天都发送？

修改：

```python
if is_workday(today) and not is_holiday(today):
```

改为：

```python
if True:
```

---



---

# License

MIT License

---

# Star History

如果这个项目对你有帮助，欢迎 Star ⭐

GitHub：

[WeChat-group-message-push](https://github.com/wangzq96/WeChat-group-message-push?utm_source=chatgpt.com)
