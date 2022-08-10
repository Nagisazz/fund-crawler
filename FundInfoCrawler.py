import requests
import time
import execjs
import pandas as pd

folderCode = './data/'

class FundInfoCrawler:
    def __init__(self, plateCode):
        self.fileFundTrain = folderCode + plateCode + "/fundinfo.csv"

        fundTrainTemp = pd.read_csv(folderCode + plateCode + "/code.csv",header=None,dtype=object).values.tolist()[0]
        self.fundTrainCode = fundTrainTemp

    def getUrl(self, fscode):
        head = 'http://fund.eastmoney.com/pingzhongdata/'
        tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())
        return head+fscode+tail

    # 根据基金代码获取净值
    def getWorth(self, fscode):
        content = requests.get(self.getUrl(fscode))
        jsContent = execjs.compile(content.text)
        # 累计净值走势
        ACWorthTrend = jsContent.eval('Data_ACWorthTrend')
        ACWorth = []
        for dayACWorth in ACWorthTrend:
            ACWorth.append(dayACWorth[1])
        return ACWorth

    def getFundTrain(self):
        trainFundFile = open(self.fileFundTrain, 'w')
        for code in self.fundTrainCode:
            try:
                trainFund = self.getWorth(code)
            except:
                continue
            if len(trainFund) > 0:
                trainFundFile.write(code + ",")
                trainFundFile.write(",".join(list(map(str, trainFund))))
                trainFundFile.write("\n")
                print('{} data downloaded'.format(code))
        trainFundFile.close()