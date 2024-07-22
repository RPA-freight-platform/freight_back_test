from flask import Blueprint, render_template, request, jsonify, render_template_string
import data_freightos, data_icontainers
import json
import os
from app import db
from app.models import FreightInfo, Bill

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def homePage():
    return render_template('index.html')

# 엔드포인트: 크롤링 및 데이터 저장
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



            ## freightos
            data_f = data_freightos.search(key1, key2, key3, key4)
            ## 샘플 데이터 : data = data_freightos.search('Korea, Republic of', 'KRPUS','United States', 'USLGB'

            if isinstance(data_f, str):  # 에러 메시지라면
                print("Freightos : Failed to crawl data")
            # 데이터를 JSON 파일로 저장
            file_path = 'freightos_data.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_f, f, ensure_ascii=False, indent=4)
            
            return render_template('store.html', data=data_f, data_i_20=data_i)
        

# 엔드포인트: 저장된 JSON 파일 데이터을 데이터베이스에 저장
@bp.route('/store_data', methods=['GET'])
def show_data():
    # freightos 데이터 저장
    file_path = 'freightos_data.json'
    if not os.path.exists(file_path):
        print("File not found")
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
        print("File not found")
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
    return render_template('index.html')