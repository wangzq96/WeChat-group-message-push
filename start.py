# -*- coding: utf-8 -*-
"""
@File    : main_script.py
@Date    : 2024-07-30
"""

import json
import re
import requests
from datetime import datetime
from parsel import Selector


def get_calendar(year_and_month):
    """
    数据来源：https://wannianrili.bmcx.com/

    @return:
    {
      "2024-04-01": {
        "class_name": "",
        "comment": "愚人节"
        }
    }
    """
    url = "https://wannianrili.bmcx.com/ajax/"
    params = {"q": year_and_month, "v": "22121303"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }
    res = requests.get(url, params=params, headers=headers)
    sel = Selector(text=res.text)
    rows = sel.css(".wnrl_riqi")

    data = {}
    for row in rows:
        class_name = row.css("a::attr(class)").extract_first("").strip()
        day = row.css("a::attr(onclick)").extract_first("").strip()
        comment = row.css(".wnrl_td_bzl::text").extract_first("").strip()
        ret = re.search("\d{4}-\d{2}-\d{2}", day)
        day = ret.group(0)
        data[day] = {"class_name": class_name, "comment": comment}

    return data


def get_day_item(day):
    """
    获取指定日期的节假日信息
    @param day: 日期，格式为 'YYYY-MM-DD'
    @return: {"class_name": "", "comment": "愚人节"}
    """
    calendar = get_calendar("-".join(day.split("-")[:2]))
    return calendar.get(day)


def is_workday(day):
    """
    判断指定日期是否为工作日
    @param day: 日期，格式为 'YYYY-MM-DD'
    @return: True if workday, False otherwise
    """
    workday_class_list = ["", "wnrl_riqi_ban"]
    day_item = get_day_item(day)
    if day_item:
        return day_item.get("class_name") in workday_class_list
    return False


def is_holiday(day):
    """
    判断指定日期是否为节假日
    @param day: 日期，格式为 'YYYY-MM-DD'
    @return: True if holiday, False otherwise
    """
    holiday_class_list = ["wnrl_riqi_xiu", "wnrl_riqi_mo"]
    day_item = get_day_item(day)
    if day_item:
        return day_item.get("class_name") in holiday_class_list
    return False


def get_weather():
    # 北京天气
    url = "http://t.weather.itboy.net/api/weather/city/101010100"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast = data.get("data", {}).get("forecast", [])
        today = datetime.now().strftime("%Y-%m-%d")

        for item in forecast:
            if item.get("ymd") == today:
                high = item.get("high", "未知")
                low = item.get("low", "未知")
                weather_type = item.get("type", "未知")
                notice = item.get("notice", "未知")

                weather_report = (
                    f"今日气温 {low} - {high}，天气情况：{weather_type}\n"
                    f"温馨提示：{notice}"
                )
                return weather_report
        return "无法获取今天的天气信息"
    else:
        return f"请求失败，状态码：{response.status_code}"

def update_and_reset_index(index_file, max_value=59):
    """
    更新索引值并在达到最大值时重置为1
    @param index_file: 存储索引值的文件路径
    @param max_value: 索引最大值，默认为59，因为sentence.txt存了60条
    @return: 当前索引值
    """
    try:
        with open(index_file, "r") as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        index = 0  # 如果文件不存在或值无效，初始化为0

    index += 1
    if index > max_value:
        index = 1  # 超过最大值时重置为1

    with open(index_file, "w") as f:
        f.write(str(index))

    return index

def get_daily_sentence():
    index_file = "./current_index.txt"
    text_file = "./sentence.txt"

    index = update_and_reset_index(index_file)

    try:
        with open(text_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if index - 1 < len(lines):  # 注意索引从0开始
            sentence = lines[index - 1].strip()
        else:
            sentence = "没有更多的句子"
    except FileNotFoundError:
        sentence = "句子文件不存在"

    return sentence
   # try:
   #     with open(index_file, "r") as f:
   #         index = int(f.read().strip())
   # except (FileNotFoundError, ValueError):
   #     index = 0

   # try:
   #     with open(text_file, "r", encoding="utf-8") as f:
   #         lines = f.readlines()
   #     if index < len(lines):
   #         sentence = lines[index].strip()
   #     else:
   #         sentence = "没有更多的句子"
   # except FileNotFoundError:
   #     sentence = "句子文件不存在"

   # index += 1
   # with open(index_file, "w") as f:
   #     f.write(str(index))

   # return sentence


def send_to_wechat(content):
    # 企微微信机器人的ID
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx-xxxx-xxxx-xxxx-xxxxxx"
    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "text", "text": {"content": content}}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    # today = "2024-10-01"
    # print(today)
    if is_workday(today) and not is_holiday(today):
        weather_report = get_weather()
        daily_sentence = get_daily_sentence()

        message_content = (
            "各位同学早上好!\n"
            + "    "
            + weather_report.replace("\n", "\n    ")
            + "\n"
            + "    "
            + daily_sentence.replace("\n", "\n    ")
            + "新的一天，早安!"
        )
        # print(message_content)

        status_code = send_to_wechat(message_content)