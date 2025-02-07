# 生成历史数据
import datetime
import os 
import time
import re

def get_valid_date(prompt):
    while True:
        try:
            date_str = input(prompt + " (格式: YYYY-MM-DD): ")
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("日期格式错误，请使用 YYYY-MM-DD 格式重新输入")

def toggle_mobile_pipeline(enable=True):
    """切换 PushToMobile pipeline 的启用状态"""
    settings_path = 'news/news/settings.py'
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if '"news.pipelines.PushToMobile"' in line or "'news.pipelines.PushToMobile'" in line:
            if enable and line.strip().startswith('#'):
                # 取消注释
                lines[i] = line.lstrip('#')
            elif not enable and not line.strip().startswith('#'):
                # 添加注释
                lines[i] = '#' + line
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# 获取用户输入的起始日期和结束日期
first_day = get_valid_date("请输入起始日期")
last_day = get_valid_date("请输入结束日期")

# 确保起始日期不晚于结束日期
if first_day > last_day:
    print("起始日期不能晚于结束日期，程序将退出")
    exit(1)

# 注释掉 PushToMobile pipeline
toggle_mobile_pipeline(False)

try:
    current_day = first_day
    while current_day <= last_day:
        cmd = f'cd news;scrapy crawl cntv -a date={current_day}'    
        if not os.path.exists(f'artifacts/xwlb-{current_day}.md'):
            print(cmd)
            os.system(cmd) 
        current_day += datetime.timedelta(days=1)
        # time.sleep(1)
finally:
    # 恢复 PushToMobile pipeline
    toggle_mobile_pipeline(True)
 