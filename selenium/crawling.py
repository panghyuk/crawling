from logging import setLoggerClass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import pandas as pd

options=webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["enable-logging"])

driver = webdriver.Chrome(executable_path = r"C:\Users\오광혁\Desktop\crawling\selenium\chromedriver.exe")
driver.get('https://movie.naver.com/')

def changeWindow(number):
    if number==0:
        driver.close()
    driver.switch_to.window(driver.window_handles[number])

xpathPaper = '/html/body/div/div[3]/div/div[1]/div/div/ul/li[3]/a'
driver.find_element_by_xpath(xpathPaper).send_keys(Keys.CONTROL+'\n')

changeWindow(0)

count = 0
result = []
for i in range(1,5):
    info = []
    xpathPaper = '/html/body/div/div[4]/div/div/div/div/div[1]/table/tbody/tr['+str(i+1+count)+']/td[2]/div/a'
    driver.find_element_by_xpath(xpathPaper).send_keys(Keys.CONTROL+'\n')
    changeWindow(1)
    title = driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/h3/a[1]').text
    info.append(title)

    director = driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[2]/p/a').text
    info.append(director)

    src = driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[2]/a/img').get_attribute('src')
    urllib.request.urlretrieve(src, title+".jpg")
    info.append(src)

    xpathPaper = '/html/body/div/div[4]/div[3]/div[1]/div[3]/ul/li[6]/a'
    driver.find_element_by_xpath(xpathPaper).send_keys(Keys.CONTROL+'\n')

    changeWindow(0)
    changeWindow(1)

    for comment_num in range(1,4):
        try:
            review = driver.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[4]/div/div/div/div/ul/li['+str(comment_num)+']/a/strong').text
            info.append(review)
        except:
            continue

    result.append(info)
    changeWindow(0)

    if i % 10 ==0:
        count += 1

list_df = pd.DataFrame(result, columns=['제목','감독','사진','리뷰1','리뷰2','리뷰3'])
list_df.to_csv('크롤링결과.csv',index=False,encoding='euc-kr')
print(result)
