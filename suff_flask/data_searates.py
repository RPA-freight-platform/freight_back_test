import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import sys
import re
import json
from LocalStorage import LocalStorage
import requests
from datetime import date

# 오늘 날짜 가져오기
today = date.today()

## 검색 정보
# search_port_from_code = "KRPUS"
# search_port_to_code = "ESVLC"
# search_port_from = "Pusan"
# search_port_to = "Barcelona"
search_year = today.year
search_month = today.month
search_day = today.day

## LOG
LOG = True 

## 로그인 ID/PW
EMAIL = "ictrpa240318@gmail.com"
PW = "ictRPA240318!!"

## 스크래핑
url = u'https://www.searates.com/'
driver = webdriver.Chrome()

month_name = ['', 'January', 'February', 'March', 'April', 'May', 'June'
    ,'July', 'August', 'September', 'October', 'November', 'December']


def input_port(port_name, port_type, form):
    port_input = form.find_element(By.ID, port_type)
    port_input.send_keys(port_name)
    port_input2 = form.find_elements(By.CLASS_NAME, '_2jpsCkr-G1PW15JvOiVTeI')

    port_input2[0].click()
    port_input2 = form.find_elements(By.CLASS_NAME, '_2jpsCkr-G1PW15JvOiVTeI')
    port_input2[1].click()

## API
def get_api():

    # API 준비
    storage = LocalStorage(driver)
    token = storage.get("s-token")
    refer_url = driver.current_url

    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer '+token,
    'content-type': 'application/json',
    'origin': 'https://www.searates.com',
    'priority': 'u=1, i',
    'referer': refer_url,
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    json_data = {
        'query': '\n    {\n  rates(\n    \n    includedServices: p2p,\n    portFromFees: false,\n    portToFees: false,\n    \n    shippingType: FCL,\n    pointIdFrom: "P_10375",\n    pointIdTo: "P_3190",\n    date: "2024-07-27",\n    container: ST20,\n    \n    \n    \n    \n  ) {\n      points {\n    id\n    rateId\n        location {\n          id\n          name\n          country\n          lat\n          lng\n          code\n     inaccessible\n\n     pointType\n        }\n        shippingType\n        provider\n    providerLogo\n        loads {\n          id\n          unit\n          amount\n        }\n        pointTariff {\n     name\n     abbr\n          price\n     currency\n     profileId\n        }\n        routeTariff {\n          name\n     abbr\n     price\n     currency\n    }\n\n    lumpsumTariff {\n          price\n          currency\n    }\n\n    co2 {\n     amount\n     price\n     placeAmount\n     placePrice\n    }\n\n    transitTime {\n    rate\n    port\n    route\n   }\n   owner {\n    profileId\n    companyId,\n    fullName,\n    companyName,\n    country,\n    role {\n      id,\n      name,\n      slug\n    },\n    avatar\n   },\n\n    distance\n    totalPrice\n    totalCurrency\n    pointTotal\n    routeTotal\n    terms\n   }\n      general {\n    shipmentId\n        validityFrom\n        validityTo\n\n    individual\n        totalPrice\n        totalCurrency\n        totalTransitTime\n    totalCo2 {\n     amount\n     price\n    }\n    dfaRate\n\n    alternative\n\n    expired\n    spaceGuarantee\n    spot\n    indicative\n\n\n\n    rateOwner\n\n    queryShippingType\n      }\n  }\n}\n  ',
    }

    # API request
    # if LOG:
    #     print("request API")
    response = requests.post('https://rates.searates.com/graphql', headers=headers, json=json_data).text

    return json.loads(response)

def get_freight():
    freight = {}
    response = get_api()

    for i in range(0, len(response["data"]["rates"])):
        element = response["data"]["rates"][i]["points"][0]

        freight[element["provider"]] = {
            'cost': element["totalPrice"],
            'time': element["transitTime"]["route"],
            'valid': response["data"]["rates"][i]["general"]["validityTo"]
        }
    
    return freight

def home_search(port_from,search_port_from_code, port_to, search_port_to_code):

    driver.set_window_size(1200, driver.get_window_size().get('height'))
    driver.get(url)
    driver.implicitly_wait(5)

    login()

    # if LOG:
    #     print("[SEARCH]")
    #     print("FROM: "+port_from+" / TO: "+port_to+" / DATE: "+str(search_year)+"-"+str(search_month)+"-"+str(search_day))
    
    # 검색 입력
    form_div1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[1]/div/div[2]')
    form_div2 = driver.execute_script('return arguments[0].shadowRoot',form_div1)

    input_port(port_from, 'from', form_div2)
    input_port(port_to, 'to', form_div2)

    date_input = form_div2.find_element(By.CLASS_NAME, 'Fxh_p7ksiflCkUswgS3zb')
    date_input.click()
    month_input = form_div2.find_element(By.CLASS_NAME, 'Calendar__monthText')
    month_input.click()
    time.sleep(1)
    month_input = form_div2.find_elements(By.CLASS_NAME, 'Calendar__monthSelectorItem')
    for i in month_input:
        if i.text == month_name[search_month]:
            i.click()
            break
    
    day_input = form_div2.find_elements(By.CLASS_NAME, 'Calendar__day')
    for i in day_input:
        s = i.text
        if len(s) == 0:
            continue
        if int(s) == search_day:
            i.click()
            break

    ## 검색
    btn = form_div2.find_element(By.CLASS_NAME, 'RL3JD-TXrjsmpZuZzofVR')
    btn.click()
    driver.implicitly_wait(15)

    cur_url = driver.current_url[0:-4]

    # 20 DR 검색
    # if LOG:
    #     print('search 20 ctnr')
    driver.get(cur_url+"ST20")
    driver.implicitly_wait(5)
    freight_20 = get_freight()

    # 40 DR 검색
    # if LOG:
    #     print('search 40 ctnr')
    driver.get(cur_url+"ST40")
    driver.implicitly_wait(5)
    freight_40 = get_freight()

    # 최솟값 찾기
    # if LOG:
    #     print('find min freight')
    total_freight = {}
    companys = [*freight_20.keys()]
    for i in range(0, len(freight_20)):
        total_cost = freight_20[companys[i]]['cost'] + freight_40[companys[i]]['cost']
        total_freight[total_cost] = companys[i]

    min_freight = min(total_freight)
    min_company = total_freight[min_freight]

    # if LOG:
    #     print("min company: " + min_company)
    #     print("min freight: " + str(min_freight))
    #     print('')

    # JSON으로 출력
    # if LOG:
    #     print('[LOG]')
    #     print("write JSON file")
    #     print(freight_20[min_company])

    res = {
        "RESPONSE": "SUCCESS",
        "ERRORMSG": "",
        "ETRACE": "",
        "requestNo": "",
        "dataSource": "SEARATES",
        "platDate": datetime.today().strftime("%Y%m%d"),
        "validToDate": (freight_20[min_company]['valid']).replace("-", ""),
        "polCode": search_port_from_code,
        "podCode": search_port_to_code,
        "freightInfo": [
            {
                "polCode": search_port_from_code,
                "podCode": search_port_to_code,
                "leadtime": freight_20[min_company]['time'],
                "billList": [
                    {
                    "tariffGroupCode": "FRIT",
                    "billName": "Basic Ocean Freight",
                    "billDivCode": "BOX",
                    "billUnit": "20DR",
                    "cntrSize": "20",
                    "cntrType": "DR",
                    "currencyCode": "USD",
                    "billRate": freight_20[min_company]['cost']
                    },
                    {
                    "tariffGroupCode": "FRIT",
                    "billName": "Basic Ocean Freight",
                    "billDivCode": "BOX",
                    "billUnit": "40DR",
                    "cntrSize": "40",
                    "cntrType": "DR",
                    "currencyCode": "USD",
                    "billRate": freight_40[min_company]['cost']
                    }
                ]
            }
        ]
    }

    # if LOG:
    #     print(res)

    # with open("./response.json", 'w', encoding='utf-8') as file:
    #     json.dump(res, file)
    return res


## 로그인
def login():
    # if LOG:
    #     print('[LOGIN]')

    driver.get(u'https://www.searates.com/auth/sign-in')
    email_input = driver.find_element(By.ID, 'login')
    email_input.send_keys(EMAIL)
    pw_input = driver.find_element(By.ID, 'password')
    pw_input.send_keys(PW)
    btn = driver.find_element(By.XPATH, '//*[@id="authForm"]/button')
    btn.click()

    home_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]/div[2]/a')))
    home_btn.click()

    # if LOG:
    #     print('success')
    #     print('')

## Main
# if __name__ == '__main__':
#     driver.set_window_size(1200, driver.get_window_size().get('height'))
#     driver.get(url)
#     driver.implicitly_wait(5)

    # if LOG:
    #     print('')
    #     print('title: ' + driver.title)
    #     print('url: ' + driver.current_url)
    #     print('')

    # home_search(search_port_from, search_port_to)