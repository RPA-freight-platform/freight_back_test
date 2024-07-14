from flask import Blueprint, render_template, request, jsonify, render_template_string
import data_freightos
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
            data = data_freightos.search(key1, key2, key3, key4)

            ## 샘플 데이터 : data = data_freightos.search('Korea, Republic of', 'KRPUS','United States', 'USLGB')
            if isinstance(data, str):  # 에러 메시지라면
                return jsonify({'error': data}), 500
        
            # 데이터를 JSON 파일로 저장
            file_path = 'crawled_data.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            return render_template('store.html', data=data)
            
            # feedback data
            # return render_template('data.html', data=data)

# 엔드포인트: 저장된 JSON 파일 데이터을 데이터베이스에 저장
@bp.route('/store_data', methods=['GET'])
def show_data():
    file_path = 'crawled_data.json'
    if not os.path.exists(file_path):
        return jsonify({'error': 'No data available. Please crawl data first.'}), 404
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        #existing_freight = FreightInfo.query.filter_by(pol_code=data['polCode'],pod_code=data['podCode']).first()
        #print(existing_freight)

        #if existing_freight:
        #    print("Freight info already exists")
        #    return "Freight info already exists", 409
        
        if data['RESPONSE'] == "SUCCESS":
            # 데이터베이스 중복확인
            existing_freight = FreightInfo.query.filter_by(plat_date=data['platDate'],valid_date=data['validToDate'], pol_code=data['polCode'], pod_code=data['podCode']).first()
            if existing_freight:
                print("Freight info already exists")
                return jsonify({'message': 'data is already exist.'}), 409

            # 데이터베이스에 저장
            for freight in data['freightInfo']:
                new_freight = FreightInfo(
                    data_source=data['dataSource'],
                    plat_date=data['platDate'],
                    valid_date=data['validToDate'],
                    pol_code=freight['polCode'],
                    pod_code=freight['podCode'],
                    lead_time=freight['leadTime']
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
            return jsonify({'message': 'Data saved successfully'}), 200

        return jsonify({'message': 'Failed to save data'}), 400
    
    # 간단한 HTML 템플릿으로 데이터 보여주기
    html_template = '''

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crawled Data</title>
    </head>
    <body>
        <h1>Crawled Data</h1>
        <ul>
            {% for item in data %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
        <p>{{data.freightInfo}}</p>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, data=data)