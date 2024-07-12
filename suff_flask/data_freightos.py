from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# ActionChains 모듈 import
from selenium.webdriver.common.action_chains import ActionChains
# driver.implicitly_wait(10)
from datetime import date

# 크롬드라이버 실행


def search(start_country, start_port, finish_country, finish_port):
    driver = webdriver.Chrome()
    driver.get('https://ship.freightos.com/')

    # login
    login_buttion = driver.find_element(By.XPATH, '//*[@id="app-container"]/header/div/div[2]/div/div[1]/button')
    driver.implicitly_wait(10)
    login_buttion.click()
    id_box = driver.find_element(By.CLASS_NAME, 'ant-input.ant-input-lg')
    driver.implicitly_wait(10)
    id_box.send_keys('4840sss@kookmin.ac.kr')
    driver.implicitly_wait(10)
    password_box = driver.find_element(By.XPATH, '//*[@id="authUILogIn_password"]')

    driver.implicitly_wait(10)
    password_box.send_keys('Bok18864jae!')
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, '/html/body/div[12]/div/div[2]/div/div[2]/div/div/div[1]/div/form/button').click()
    time.sleep(3)

    ## 검색요건1(origin)
    origin_button = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[1]/p')
    driver.implicitly_wait(10)
    origin_button.click()
    # type 선택
    origin_type = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/span/div/div/div/div')
    driver.implicitly_wait(10)
    origin_type.click()
    driver.find_element(By.XPATH,'/html/body/div[12]/div/div/div/ul/li[1]').click()
    # country 선택
    origin_country = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/span/div/div/div/div')
    driver.implicitly_wait(10)
    origin_country.click()
    driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/span/div/div/div/div/div[3]/div/input').send_keys(start_country)
    target = driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/span/div/div/div/div/div[3]/div/input')
    action = ActionChains(driver)
    action.move_to_element(target).move_by_offset(90, 45).click().perform()
    
    origin_address = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/span/div/div/div')
    driver.implicitly_wait(10)
    origin_address.click()
    driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/span/div/div/div/div[2]/div/input').send_keys(start_port)
    target = driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/span/div/div/div/div[2]/div/input')
    action = ActionChains(driver)
    action.move_to_element(target).move_by_offset(90, 45).click().perform()
    time.sleep(3)

    ## 검색요건2(destination)
    destination_button = driver.find_element(By.CSS_SELECTOR, '[data-test-id="CategoryWrapper-destination"]')
    driver.implicitly_wait(10)
    destination_button.click()
    # type 선택
    destination_type = driver.find_element(By.CSS_SELECTOR, '[data-test-id="destination-type"]')
    driver.implicitly_wait(10)
    destination_type.click()
    action = ActionChains(driver)
    action.move_to_element(destination_type).move_by_offset(90, 45).click().perform()
    #country 선택
    destination_country = driver.find_element(By.CSS_SELECTOR, '[data-test-id="destination-country-select"]')
    driver.implicitly_wait(10)
    destination_country.click()
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[6]/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/span/div/div/div/div/div[3]/div/input').send_keys(finish_country)
    driver.implicitly_wait(10)
    target = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[6]/div/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/span/div/div/div/div/div[3]/div/input')
    action = ActionChains(driver)
    action.move_to_element(target).move_by_offset(90, 45).click().perform()
    
    destination_address = driver.find_element(By.CSS_SELECTOR, '[data-test-id="destination-address-select"]')
    driver.implicitly_wait(10)
    destination_address.click()
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[6]/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/span/div/div/div/div[2]/div/input').send_keys(finish_port)
    target = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[6]/div/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/span/div/div/div/div[2]/div/input')
    action = ActionChains(driver)
    action.move_to_element(target).move_by_offset(90, 45).click().perform()
    time.sleep(3)
    
    ## 검색요건3(Load)
    load_button = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[3]')
    driver.implicitly_wait(10)
    load_button.click()
    driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[7]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/span').click()
    # add goods 40ft
    add_button = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[7]/div/div/div/div/div/div/div[2]/button[1]')
    driver.implicitly_wait(10)
    #add_button.click()
    # add goods 20ft
    #driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div/div[1]/div[2]/div/div/div[7]/div/div/div/div/div/div/div[1]/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/div/span/div/label[1]/span[1]').click()
    target = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[7]/div/div/div/div/div/div/div[2]/button[2]')
    action = ActionChains(driver)
    action.move_to_element(target).move_by_offset(-252, -115).click().perform()
    add_button.click()

    driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[7]/div/div/div/div/div/div/div[2]/button[2]').click()
    time.sleep(3)

    ## 검색요건4(Goods)
    goods_button = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[4]')
    driver.implicitly_wait(10)
    goods_button.click()
    # goods value 입력
    driver.find_element(By.XPATH, '/html/body/div[2]/section/main/div/div[1]/div[2]/div/div/div[8]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div/span/span/span/input').send_keys("100000")
    # ready
    driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[8]/div/div/div/div/div/div/div[1]/div[3]/div[2]/div/span/div/div/div/div').click()
    
    target = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[8]/div/div/div/div/div/div/div[1]/div[3]/div[2]/div/span/div/div/div/div')
    action = ActionChains(driver)
    action.move_to_element(target).move_by_offset(10, 40).click().perform()
    
    driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/div[8]/div/div/div/div/div/div/div[2]/button').click()
    time.sleep(3)

    ## Done !
    search_button = driver.find_element(By.XPATH, '//*[@id="app-container"]/main/div/div[1]/div[2]/div/div/button')
    driver.implicitly_wait(10)
    search_button.click()
    singleBond_button = driver.find_element(By.XPATH, '/html/body/div[12]/div/div/div/div[2]/div[2]/div/div[3]/div[2]/ul[2]/li/div[4]/label[1]')
    driver.implicitly_wait(10)
    singleBond_button.click()
    result_button = driver.find_element(By.XPATH, '/html/body/div[12]/div/div/div/div[2]/div[3]/div/button[2]')
    driver.implicitly_wait(10)
    result_button.click()
    time.sleep(5)

    ## best offer 선택
    offer_button = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div')
    driver.implicitly_wait(10)
    offer_button.click()

    fee20 = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[2]/div/div[1]/div[3]/div[6]/span/span[2]')
    fee40 = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[2]/div/div[1]/div[4]/div[6]/span/span[2]')
    print("OCEAN 20' :", fee20.text)
    print("OCEAN 40' :", fee40.text)

    ## json 파일로 저장
    data =  {
  "RESPONSE": "SUCCESS",
  "ERRORMSG": "",
  "ETRACE": "",
  "requestNo": "",
  "dataSource": "FREIGHTOS",
  "platDate": "",
  "validToDate": "",
  "polCode": "",
  "podCode": "",
  "freightInfo": [
    {
      "polCode": "",
      "podCode": "",
      "leadTime": 50,
      "billList": [
        {
          "tariffGroupCode": "FRIT",
          "billName": "Basic Ocean Freight",
          "billDivCode": "BOX",
          "billUnit": "20DR",
          "cntrSize": "20",
          "cntrType": "HC",
          "currencyCode": "USD",
          "billRate": ""
        },
        {
          "tariffGroupCode": "FRIT",
          "billName": "Basic Ocean Freight",
          "billDivCode": "BOX",
          "billUnit": "45HC",
          "cntrSize": "40",
          "cntrType": "HC",
          "currencyCode": "USD",
          "billRate": ""
        }
      ]
    }
  ]
}   
    today_date = date.today()
    plateDate =  today_date.strftime("%Y%m%d")
    data["platDate"] = plateDate
    validToDate = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[1]/div[1]/div/div[2]/div/div[2]/span')
    validToDate = validToDate.text
    validToDate = validToDate.split(' ')
    month = validToDate[2]
    monthDic = {'Janu':'01', 'Feb':'02', 'March':'03', 'April':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    month = monthDic[month]
    day = validToDate[3][:2]
    year = validToDate[4]
    validToDate = year + month + day

    polCode = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[1]/div[1]/div/div[1]/div[3]/span[1]')
    podCode = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[1]/div[1]/div/div[1]/div[3]/span[2]')
    fee20 = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[2]/div/div[1]/div[3]/div[6]/span/span[2]')
    fee40 = driver.find_element(By.XPATH, '//*[@id="results-view"]/section/section/main/div[1]/div/div[2]/div/div[1]/div[4]/div[6]/span/span[2]')

    data["validToDate"] = validToDate
    data["polCode"] = polCode.text
    data["podCode"] = podCode.text
    data["freightInfo"][0]["polCode"] = polCode.text
    data["freightInfo"][0]["podCode"] = podCode.text
    data["freightInfo"][0]["billList"][0]["billRate"] = fee20.text
    data["freightInfo"][0]["billList"][1]["billRate"] = fee40.text
    print(data)
    driver.quit()

    return data
    # json 파일로 저장
    #import json
    #with open('data.json', 'w') as f:
    #    json.dump(data, f, indent=4)