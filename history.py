# 生成历史数据
import datetime
import os 
import time

def get_valid_date(prompt):
    while True:
        try:
            date_str = input(prompt + " (格式: YYYY-MM-DD): ")
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("日期格式错误，请使用 YYYY-MM-DD 格式重新输入")

# 获取用户输入的起始日期和结束日期
first_day = get_valid_date("请输入起始日期")
last_day = get_valid_date("请输入结束日期")

# 确保起始日期不晚于结束日期
if first_day > last_day:
    print("起始日期不能晚于结束日期，程序将退出")
    exit(1)

current_day = first_day
while current_day <= last_day:
    cmd = f'cd news;scrapy crawl cntv -a date={current_day}'    
    if not os.path.exists(f'artifacts/xwlb-{current_day}.md'):
        print(cmd)
        os.system(cmd) 
    current_day += datetime.timedelta(days=1)
    # time.sleep(1)
 