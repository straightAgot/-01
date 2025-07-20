from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 初始化浏览器
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

# 打开主网站
driver.get("http://jy.ggzy.foshan.gov.cn:3680/TPBank/newweb/framehtml/onlineTradex/index.html")
time.sleep(3)

# 点击“历史交易”
driver.find_element(By.XPATH, "//a[contains(text(),'历史交易')]").click()
time.sleep(5)

# 勾选状态筛选：“已成交”、“竞价结束”
driver.find_element(By.XPATH, "//label[contains(text(),'已成交')]").click()
driver.find_element(By.XPATH, "//label[contains(text(),'竞价结束')]").click()
time.sleep(2)

# 点击“查询”按钮
driver.find_element(By.XPATH, "//button[contains(text(),'查询')]").click()
time.sleep(5)

# 初始化结果列表
results = []

# 爬取前 10 页
for page in range(1, 11):
    print(f" 第 {page} 页")

    # 获取所有详情按钮
    detail_links = driver.find_elements(By.XPATH, "//a[contains(text(),'详情')]")
    
    for i in range(len(detail_links)):
        # 每次重新找元素（因为刷新页面后会失效）
        detail_links = driver.find_elements(By.XPATH, "//a[contains(text(),'详情')]")
        link = detail_links[i]
        
        # 新标签打开详情页
        driver.execute_script("window.open(arguments[0].href);", link)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        
        # 提取字段
        text = driver.page_source
        info = {
            "成交时间": "",
            "竞得人": "",
            "交易土地面积": "",
            "成交地价": "",
            "地块位置": "",
            "土地用途": "",
            "状态": ""
        }

        for key in info.keys():
            try:
                element = driver.find_element(By.XPATH, f"//*[contains(text(),'{key}')]")
                value = element.find_element(By.XPATH, "following-sibling::*[1]").text.strip()
                info[key] = value
            except:
                pass

        results.append(info)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    # 点击下一页
    try:
        next_btn = driver.find_element(By.LINK_TEXT, "下一页")
        next_btn.click()
        time.sleep(5)
    except:
        print("没有更多页面")
        break

# 导出为 Excel
df = pd.DataFrame(results)
df.to_excel("佛山历史拍地数据（Selenium版）.xlsx", index=False)
print(" 数据保存完成。")

# 关闭浏览器
driver.quit()
