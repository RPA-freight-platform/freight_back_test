from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from datetime import date
import requests
import time
import json

# 브라우저 꺼짐 방지 옵션

def login_and_initial_search(driver):
    driver.get('https://www.icontainers.com/')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Login/Register')))
    login_link = driver.find_element(By.LINK_TEXT, 'Login/Register')
    login_link.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'email')))
    email_field = driver.find_element(By.NAME, 'email')
    email_field.send_keys('jiyeyu1220@gmail.com')
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('Novelove18!')
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()

def select_container_and_search(start_port, end_port, option_index):
    try:
        # chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)

        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver = webdriver.Chrome()
        login_and_initial_search(driver)
        
        WebDriverWait(driver, 20).until(EC.url_contains('https://my.icontainers.com/'))

        origin_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'originLocation'))
        )
        # 출발지 입력
        origin_input.send_keys(start_port)
        time.sleep(3)
        action = ActionChains(driver)
        action.move_to_element(origin_input).move_by_offset(10, 120).click().perform()
        time.sleep(1)

        # 도착지 입력
        destination_input = driver.find_element(By.NAME, 'destinationLocation')
        destination_input.send_keys(end_port)
        time.sleep(3)
        action = ActionChains(driver)
        action.move_to_element(destination_input).move_by_offset(10, 120).click().perform()
        time.sleep(1)

        # 컨테이너 타입 드롭다운을 클릭
        #container_dropdown = WebDriverWait(driver, 5).until(
        #    EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[2]/main/div/div[1]/div/div/div[2]/form/div[5]/div[1]/div/div/input'))
        #)
        #container_dropdown.click()
        container_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-1g6gooi'))
        )
        container_dropdown.click()

        # 옵션 선택 - 드롭다운 방식 사이트 (첫 번째 옵션: 0 - 20, 두 번째 옵션: 1 - 40)
        container_option = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, f'react-select-3-option-{option_index}'))
        )
        container_option.click()
        

        #if option_index == 1:
        #    target = driver.find_element(By.XPATH, '//*[@id="root"]/div[3]/div[2]/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div/div[2]/div/div/button')
        #    action = ActionChains(driver)
        #    action.move_to_element(target).move_by_offset(10, -36).click().perform()
        #    time.sleep(1)
        #    #action.move_to_element().move_by_offset(10, 188).click().perform()
        #    #time.sleep(1)

        search_rates_button = driver.find_element(By.XPATH, '//span[text()="Search Rates"]')
        search_rates_button.click()
        time.sleep(5)
        # WebDriverWait(driver, 20).until(EC.url_contains('https://my.icontainers.com/quotes'))

        show_details_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="ShowRateDetailsButton"]'))
        )
        show_details_button.click()

        # 동적 url
        def get_dynamic_url():
            for request in driver.requests:
                if request.response and 'delivery=false' in request.url:
                    return request.url
            return None

        time.sleep(7)
        print('---')
        # 동적 url로 요청하기
        dynamic_url = get_dynamic_url()
        if dynamic_url:
            response = requests.get(dynamic_url)
            original_data = response.json()
            driver.quit()
            today_date = date.today()
            plateDate =  today_date.strftime("%Y%m%d")
            if option_index == 0:
                return {
                    "RESPONSE": "SUCCESS",
                    "ERRORMSG": "",
                    "ETRACE": "",
                    "requestNo": original_data.get("data", {}).get("uuid", ""),
                    "dataSource": "iContainers",
                    "platDate": plateDate,
                    "validToDate": original_data.get("data", {}).get("expirationDate", "").replace("-", ""),
                    "polCode": original_data.get("data", {}).get("maritimeSchedule", {}).get("originPort", {}).get("isoCode", ""),
                    "podCode": original_data.get("data", {}).get("maritimeSchedule", {}).get("destinationPort", {}).get("isoCode", ""),
                    "freightInfo": [
                        {
                            "polCode": original_data.get("data", {}).get("maritimeSchedule", {}).get("originPort", {}).get("isoCode", ""),
                            "podCode": original_data.get("data", {}).get("maritimeSchedule", {}).get("destinationPort", {}).get("isoCode", ""),
                            "leadtime": "",
                            # original_data.get("data", {}).get("maritimeSchedule", {}).get("transitDays", 0)
                            "billList": [
                                {   
                                    #"tariffGroupCode": original_data.get("data", {}).get("suppliersInformation", {}).get("freight", {}).get("tariffGroupCode", ""),
                                    "tariffGroupCode": "FRIT",
                                    "billName": original_data.get("data", {}).get("suppliersInformation", {}).get("freight", {}).get("name", ""),
                                    "billDivCode": "BOX",
                                    "billUnit": "20DR",
                                    #"currency": original_data.get("data", {}).get("total", {}).get("currency", ""),
                                    #"amount": original_data.get("data", {}).get("total", {}).get("amount", 0),
                                    #"taxes": original_data.get("data", {}).get("total", {}).get("taxes", 0),
                                    #"discounts": original_data.get("data", {}).get("total", {}).get("discounts", 0),
                                    "cntrSize": "20",
                                    "cntrType": "HC",
                                    "currencyCode": "USD",
                                    "billRate": original_data.get("data", {}).get("total", {}).get("total", 0)
                            }
                        ]
                    }

                    ]
                }
            
            else:
                return  {       
                            "tariffGroupCode": original_data.get("data", {}).get("suppliersInformation", {}).get("freight", {}).get("tariffGroupCode", ""),
                            "billName": original_data.get("data", {}).get("suppliersInformation", {}).get("freight", {}).get("name", ""),
                            "billDivCode": "BOX",
                            "billUnit": "40DR",
                            #"currency": original_data.get("data", {}).get("total", {}).get("currency", ""),
                            #"amount": original_data.get("data", {}).get("total", {}).get("amount", 0),
                            #"taxes": original_data.get("data", {}).get("total", {}).get("taxes", 0),
                            #"discounts": original_data.get("data", {}).get("total", {}).get("discounts", 0),
                            "cntrSize": "20",
                            "cntrType": "HC",
                            "currencyCode": "USD",
                            "billRate": original_data.get("data", {}).get("total", {}).get("total", 0)

                    }
        else:
            print("동적 URL을 찾을 수 없습니다.")
            return None
            
    except TimeoutException:
        driver.quit()
        return None


# 로그인

# 40 ft. Container 검색
#bill_list_40ft = select_container_and_search(1)
#print(bill_list_40ft)

#if data_20ft and bill_list_40ft:
#    data_20ft['freightInfo']['billList'].extend(bill_list_40ft)
#    print(json.dumps(data_20ft, indent=4))


#driver.quit()
#return data_20ft