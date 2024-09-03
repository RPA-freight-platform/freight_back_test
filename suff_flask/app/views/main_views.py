from flask import Blueprint, render_template, request, jsonify, render_template_string
import data_freightos, data_icontainers, data_searates
import json
import os
from app import db
from app.models import FreightInfo, Bill, PortCodeItem

# db 저장을 위한 작업
# import pandas as pd

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def homePage():
    table = PortCodeItem.query.all()
    # print(table)
    return render_template('index.html', table=table)

# 셀렉 박스 생성을 위한 저장 과정 
# @bp.route('/db')
# def insert_data_from_excel():
    # 엑셀 파일 읽기
    # df = pd.read_excel('port_code_item.xlsx')

    # # 각 행을 데이터베이스에 삽입
    # for _, row in df.iterrows():
    #     port_code_item = PortCodeItem(
    #         portCode=row['portCode'],
    #         portName=row['portName'],
    #         portNameKor=row['portNameKor'],
    #         nationCode=row['nationCode'],
    #         continent=row['continent'],
    #         region=row['region'],
    #         latitude=row['latitude'],
    #         longitude=row['longitude'],
    #         cargoTypes=row['cargoTypes'],
    #         nearByPort_1=row['nearByPort_1'],
    #         nearByPort_2=row['nearByPort_2'],
    #         nearByPort_3=row['nearByPort_3'],
    #         nearByPort_4=row['nearByPort_4'],
    #         nearByAirport_1=row['nearByAirport_1'],
    #         nearByAirportKm_1=row['nearByAirportKm_1'],
    #         nearByAirport_2=row['nearByAirport_2'],
    #         nearByAirportKm_2=row['nearByAirportKm_2'],
    #         nearByAirport_3=row['nearByAirport_3'],
    #         nearByAirportKm_3=row['nearByAirportKm_3'],
    #         nearByAirport_4=row['nearByAirport_4'],
    #         nearByAirportKm_4=row['nearByAirportKm_4'],
    #         itemOrder=row['itemOrder'],
    #         majorYN=row['majorYN'],
    #         delYN=row['delYN'],
    #         regKey=row['regKey'],
    #         modKey=row['modKey'],
    #     )
    #     db.session.add(port_code_item)

    # db.session.commit()
    # return render_template('index.html')


# 자동완성 셀렉박스 생성
@bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    data = PortCodeItem.query.all()
    # PortCodeItem 객체의 속성을 JSON으로 직렬화 가능한 형태로 변환하는 함수
    def port_code_item_to_dict(item):
        return {
            'portCode': item.portCode,
            'portName': item.portName,
            # 여기에 필요한 모든 속성 추가
        }

    # autocomplete 뷰 함수 내에서 PortCodeItem 객체 리스트를 처리하는 부분
    search = request.args.get('q', '')
    print(search)
    results = [port_code_item_to_dict(item) for item in data if search.upper() in item.portCode.upper()]

    port_codes = [port['portCode'] for port in results]
    # print(port_codes)
    return jsonify(port_codes)


# 엔드포인트: 서비스 시작_사용자 입력에 따라 데이터베이스 검사
@bp.route('/search_data', methods=['GET'])
def search_data():
    key1 = request.args.get('autocomplete-input1')
    key2 = request.args.get('autocomplete-input2')
    key3 = request.args.get('search3')
    print(key1)
    print(key2)

    if key1 == None or key2 == None or key3 == None:
        print(key1, key2, key3)
        return render_template('index.html')
    else:
        if key1 == "" or key2 == "" or key3 == "":
            print(key1, key2, key3)
            return render_template('index.html')
    
    # 사용자 입력에 따라 DB 탐색
    data = FreightInfo.query.filter_by(pol_code=key1, pod_code=key2, plat_date=key3).all()
    if not data:
        print(key1, key2, key3)
        return render_template('data.html')
    else:
        print(data)
        return render_template('result.html', polCode=key1, podCode=key2, platDate=key3, datas=data)

    # return render_template('index.html')

# 엔드포인트: 크롤링 및 데이터 저장
## freightos, icontainer
@bp.route('/crawl', methods=['GET'])
def crawl():
    #get을 통해 전달받은 데이터를 확인
    key1 = request.args.get('keyword1')
    key2 = request.args.get('keyword2')
    key3 = request.args.get('keyword3')
    key4 = request.args.get('keyword4')

    if key1 == None or key2 == None or key3 == None or key4 == None:
        print(key1, key2, key3, key4)
        return render_template('data.html')
    else:
        if key1 == "" or key2 == "" or key3 == "" or key4 == "":
            return render_template('data.html')
        
    #키워드 크롤링

    ## freightos
    data_f = data_freightos.search(key1, key2, key3, key4)
    ## 샘플 데이터 : data = data_freightos.search('Korea, Republic of', 'KRPUS','United States', 'USLGB'

    if isinstance(data_f, str):  # 에러 메시지라면
        print("Freightos : Failed to crawl data")
    # 데이터를 JSON 파일로 저장
    file_path = 'freightos_data.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_f, f, ensure_ascii=False, indent=4)


    ## icontainers
    data_i = data_icontainers.select_container_and_search(key2, key4, 0)
    if isinstance(data_i, str):  # 에러 메시지라면
        print("Icontainers : Failed to crawl data")
    elif data_i == None:
        print("Icontainers : Failed to crawl data")
    else:
        data_i_40 = data_icontainers.select_container_and_search(key2, key4, 1)
        if isinstance(data_i_40, str):  # 에러 메시지라면
            print("Icontainers : Failed to crawl data")

        print(data_i_40)
        if data_i and data_i_40:
            print("Icontainers : Data crawled successfully")
            data_i['freightInfo'][0]['billList'].append(data_i_40)

        file_path = 'icontainers_data.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_i, f, ensure_ascii=False, indent=4)

    
    return render_template('store.html', data=data_f, data_i_20=data_i)    

## searates
@bp.route('/crawl_searates', methods=['GET'])
def crawl_searates():
    #get을 통해 전달받은 데이터를 확인
    key1 = request.args.get('keyword5')
    key2 = request.args.get('keyword6')
    key3 = request.args.get('keyword7')
    key4 = request.args.get('keyword8')

    if key1 == None or key2 == None or key3 == None or key4 == None:
        print(key1, key2, key3, key4)
        return render_template('data.html')
    else:
        if key1 == "" or key2 == "" or key3 == "" or key4 == "":
            return render_template('data.html')
        
        #키워드 크롤링
    
    ## searates
    data_s = data_searates.home_search(key1, key2, key3, key4)

    if isinstance(data_s, str):  # 에러 메시지라면
        print("Searates : Failed to crawl data")
    # 데이터를 JSON 파일로 저장
    file_path = 'searates_data.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_s, f, ensure_ascii=False, indent=4)

    return render_template('store.html', data=data_s)
        
# 엔드포인트: 저장된 JSON 파일 데이터을 데이터베이스에 저장
@bp.route('/store_data', methods=['GET'])
def show_data():
    # freightos 데이터 저장
    file_path = 'freightos_data.json'
    if not os.path.exists(file_path):
        print("freightos File not found")
    # 파일이 비어있는지 확인
    elif os.path.getsize(file_path) == 4:
        print("Freightos : No data to save")
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data['RESPONSE'] == "SUCCESS":
                # 데이터베이스 중복확인
                existing_freight = FreightInfo.query.filter_by(plat_date=data['platDate'],valid_date=data['validToDate'], pol_code=data['polCode'], pod_code=data['podCode']).first()
                if existing_freight:
                    print("Freight info already exists")
                else:
                    # 데이터베이스에 저장
                    for freight in data['freightInfo']:
                        print(freight)
                        new_freight = FreightInfo(
                            data_source=data['dataSource'],
                            plat_date=data['platDate'],
                            valid_date=data['validToDate'],
                            pol_code=freight['polCode'],
                            pod_code=freight['podCode'],
                            lead_time=freight['leadtime']
                        )
                        db.session.add(new_freight)
                        db.session.commit()

                        for bill in freight['billList']:
                            new_bill = Bill(
                                tariff_group_code=bill['tariffGroupCode'],
                                bill_name=bill['billName'],
                                bill_div_code=bill['billDivCode'],
                                bill_unit=bill['billUnit'],
                                cntr_size=bill['cntrSize'],
                                cntr_type=bill['cntrType'],
                                currency_code=bill['currencyCode'],
                                bill_rate=bill['billRate'],
                                freight_info_id=new_freight.id
                            )
                            db.session.add(new_bill)
                        db.session.commit()
                    print("Freightos : Data saved successfully")
            else:
                print('Freightos :Failed to save data')

    # icontainers 데이터 저장
    file_path = 'icontainers_data.json'
    if not os.path.exists(file_path):
        print("icontaiers File not found")
    # 파일이 비어있는지 확인
    elif os.path.getsize(file_path) == 4:
        print("Icontainers : No data to save")
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data['RESPONSE'] == "SUCCESS":
                # 데이터베이스 중복확인
                existing_freight = FreightInfo.query.filter_by(plat_date=data['platDate'],valid_date=data['validToDate'], pol_code=data['polCode'], pod_code=data['podCode']).first()
                if existing_freight:
                    print("Icontainer info already exists")
                else:
                    # 데이터베이스에 저장
                    for freight in data['freightInfo']:
                        print(freight)
                        new_freight = FreightInfo(
                            data_source=data['dataSource'],
                            plat_date=data['platDate'],
                            valid_date=data['validToDate'],
                            pol_code=freight['polCode'],
                            pod_code=freight['podCode'],
                            lead_time=freight['leadtime']
                        )
                        db.session.add(new_freight)
                        db.session.commit()

                        for bill in freight['billList']:
                            new_bill = Bill(
                                tariff_group_code=bill['tariffGroupCode'],
                                bill_name=bill['billName'],
                                bill_div_code=bill['billDivCode'],
                                bill_unit=bill['billUnit'],
                                cntr_size=bill['cntrSize'],
                                cntr_type=bill['cntrType'],
                                currency_code=bill['currencyCode'],
                                bill_rate=bill['billRate'],
                                freight_info_id=new_freight.id
                            )
                            db.session.add(new_bill)
                        db.session.commit()
                    print("Icontainer : Data saved successfully")
            else:
                print('Icontainers :Failed to save data')

    # searates 데이터 저장
    file_path = 'searates_data.json'
    if not os.path.exists(file_path):
        print("searates File not found")
    # 파일이 비어있는지 확인
    elif os.path.getsize(file_path) == 4:
        print("Searates : No data to save")
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data['RESPONSE'] == "SUCCESS":
                # 데이터베이스 중복확인
                existing_freight = FreightInfo.query.filter_by(plat_date=data['platDate'],valid_date=data['validToDate'], pol_code=data['polCode'], pod_code=data['podCode']).first()
                if existing_freight:
                    print("Searates info already exists")
                else:
                    # 데이터베이스에 저장
                    for freight in data['freightInfo']:
                        print(freight)
                        new_freight = FreightInfo(
                            data_source=data['dataSource'],
                            plat_date=data['platDate'],
                            valid_date=data['validToDate'],
                            pol_code=freight['polCode'],
                            pod_code=freight['podCode'],
                            lead_time=freight['leadtime']
                        )
                        db.session.add(new_freight)
                        db.session.commit()

                        for bill in freight['billList']:
                            new_bill = Bill(
                                tariff_group_code=bill['tariffGroupCode'],
                                bill_name=bill['billName'],
                                bill_div_code=bill['billDivCode'],
                                bill_unit=bill['billUnit'],
                                cntr_size=bill['cntrSize'],
                                cntr_type=bill['cntrType'],
                                currency_code=bill['currencyCode'],
                                bill_rate=bill['billRate'],
                                freight_info_id=new_freight.id
                            )
                            db.session.add(new_bill)
                        db.session.commit()
                    print("Searates : Data saved successfully")
            else:
                print('Searates :Failed to save data')

    return render_template('index.html')

