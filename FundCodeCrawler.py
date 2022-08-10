from calendar import c
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

folderCode = './data/'

class FundCodeCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(
            executable_path='./driver/chromedriver.exe', options=options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://fund.eastmoney.com/ztjj"

    def craw_page(self, plate, num):
        driver = self.driver
        url = self.base_url
        driver.get(url)
        fundCode = []

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[7]/div[1]/ul/li[1]")))
            
            # 点击板块
            parent = driver.find_element(By.XPATH,"//*[@id=\"ulContent\"]")
            plateEle = parent.find_element(By.XPATH,"//*[@data-name=\""+plate+"\"]")
            plateCode = plateEle.get_attribute("data-id")
            plateEle.click()

            # 获取板块基金code
            i = 1
            while i <= num:
                table = driver.find_element(By.XPATH,"//*[@id=\"fundtopicdetail\"]/div[3]/div[2]/div[1]/table")
                codesElement = table.find_elements(By.CLASS_NAME,"jjmc")
                for codeEle in codesElement:
                    code = codeEle.find_element(By.CLASS_NAME,"fcode").text
                    fundCode.append(str(code))
                i += 1
                driver.find_element(By.XPATH,"//*[@id=\"fundtopicdetail\"]/div[3]/div[2]/div[1]/div/div/div[1]/ul/li[last()]/a").click()
        finally:
            driver.quit()
        
        # 保存code
        fileCode = folderCode + plateCode + "/code.csv"
        if not os.path.exists(folderCode + plateCode):
            os.mkdir(folderCode + plateCode)
        fundCodeFile = open(fileCode, 'w')
        if len(fundCode) > 0:
            fundCodeFile.write(",".join(list(map(str, fundCode))))
            fundCodeFile.write("\n")
            print('{} data downloaded'.format(plateCode+plate))
        fundCodeFile.close()
        return plateCode