from bs4 import BeautifulSoup
import requests

def get_keyword_number(keyword):
    
    url = "https://www.google.com/search?q={}".format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    # 웹 요청
    res = requests.get(url, headers=headers)
    #print(type(res.text))

    # 구문 분석
    soup = BeautifulSoup(res.text, 'lxml')
    #print(type(soup))

    # 원하는 데이터 추출
    number = soup.select_one('#result-stats').text
    #print(number)

    # 데이터 다듬기
    number = int(number[number.find('약')+2: number.rfind('개')].replace(',',''))
    #print(number)

    return number

if __name__ == "__main__":
    print(get_keyword_number("미국"))