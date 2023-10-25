# 生成历史数据
import datetime
import os 
import time
today = datetime.date.today()
first_day = datetime.date(2023, 1, 1)
# last_day = datetime.date(2022, 12, 31)
last_day = datetime.date(2023, 10, 24)

current_day = first_day
while current_day <= last_day:
    cmd = f'cd news;scrapy crawl cntv -a date={current_day}'    
    if not os.path.exists(f'artifacts/xwlb-{current_day}.md'):
        print(cmd)
        os.system(cmd) 
    current_day += datetime.timedelta(days=1)
    # time.sleep(1)
 