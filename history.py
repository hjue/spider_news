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

def check_missing_files(year):
    """检查指定年份缺失的文件并输出报告"""
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    start_date = datetime.date(year, 1, 1)
    end_date = min(datetime.date(year, 12, 31), yesterday)  # 使用昨天作为最大日期
    
    # 如果年份大于当前年份，直接返回
    if start_date > yesterday:
        print(f"\n{year}年还未开始或超出可爬取范围")
        return []
    
    missing_files = []
    current_date = start_date
    while current_date <= end_date:
        file_path = f'artifacts/{year}/xwlb-{current_date}.md'
        if not os.path.exists(file_path):
            missing_files.append(current_date)
        current_date += datetime.timedelta(days=1)
    
    if missing_files:
        print(f"\n=== {year}年缺失文件报告（截至 {yesterday}）===")
        print("\n缺失的文件日期:")
        for date in missing_files:
            print(f"- {date} (artifacts/{year}/xwlb-{date}.md)")
        
        # 计算应有的文件数（从1月1日到昨天）
        total_days = (end_date - start_date).days + 1
        print(f"\n应有文件数: {total_days}")
        print(f"共缺失 {len(missing_files)} 个文件")
        print(f"缺失比例: {len(missing_files)/total_days*100:.1f}%")
    else:
        print(f"\n{year}年的文件完整（截至 {yesterday}），没有缺失")
    
    return missing_files

def get_valid_year(prompt):
    """获取有效的年份输入"""
    current_year = datetime.date.today().year
    while True:
        try:
            year = int(input(prompt))
            if 2000 <= year <= current_year:  # 限制年份不能超过当前年
                return year
            else:
                print(f"请输入2000-{current_year}之间的年份")
        except ValueError:
            print("请输入有效的年份数字")

def crawl_by_date_range():
    """按日期范围爬取"""
    first_day = get_valid_date("请输入起始日期")
    last_day = get_valid_date("请输入结束日期")

    if first_day > last_day:
        print("起始日期不能晚于结束日期，程序将退出")
        return

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
    finally:
        # 恢复 PushToMobile pipeline
        toggle_mobile_pipeline(True)

def crawl_missing_files():
    """检查并爬取指定年份缺失的文件"""
    year = get_valid_year("请输入要检查的年份: ")
    missing_files = check_missing_files(year)
    
    if missing_files and input("\n是否要爬取这些缺失的文件？(y/n): ").lower() == 'y':
        # 注释掉 PushToMobile pipeline
        toggle_mobile_pipeline(False)
        
        try:
            for date in missing_files:
                cmd = f'cd news;scrapy crawl cntv -a date={date}'
                print(f"\n爬取 {date} 的数据...")
                os.system(cmd)
        finally:
            # 恢复 PushToMobile pipeline
            toggle_mobile_pipeline(True)

if __name__ == "__main__":
    while True:
        print("\n=== 新闻联播爬虫工具 ===")
        print("1. 检查并爬取指定年份缺失文件")
        print("2. 按日期范围爬取")
        print("3. 退出")
        
        choice = input("\n请选择功能 (1-3): ").strip()
        
        if choice == '1':
            crawl_missing_files()
        elif choice == '2':
            crawl_by_date_range()
        elif choice == '3':
            print("程序已退出")
            break
        else:
            print("无效的选择，请重新输入")
 