
  


# spider_news
抓取重要新闻，可配置推送


 [![Spider](https://github.com/hjue/spider_news/actions/workflows/python-app.yml/badge.svg)](https://github.com/hjue/spider_news/actions/workflows/python-app.yml)


## 功能


抓取自己挑选的新闻源，新闻可按照关键词过滤后，推送符合要求的新闻到手机上。

第一个新闻源：《新闻联播》，每晚9点抓取当天新闻联播的主要内容，推送到手机上



## 关于推送

目前仅支持推送到iOS手机上，手机端需要安装Bark并获取到DeviceKey。

获取到DeviceKey后，在Github项目中设置环境变量DEVICEKEY。

以下是在 GitHub Workflow 中使用 Secrets 的示例：

打开你的代码仓库。导航到 "Settings" 选项卡。在左侧的侧边栏中，选择 "Secrets"，增加Environment secrets，Name为DEVICEKEY，Value是你手机端Bark中获取到的APIKEY

