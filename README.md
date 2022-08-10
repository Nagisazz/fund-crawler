# fund-crawler
基金爬虫，爬取基金基本信息、所属板块及净值信息

## 使用
修改`FundMain.py`对应参数，运行`FundMain.py`即可
例如：爬取军工板块相关度前20基金信息，即修改参数为
```
fundCodeCraw.craw_page('军工',2)
```
## 查看
输出在`data`目录下，`fundinfo.csv`为爬取的基金净值信息，csv第一列为基金代码