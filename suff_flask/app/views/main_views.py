from flask import Blueprint, render_template, request, jsonify, render_template_string
import data_freightos
import json
import os

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
                print(key1, key2, key3, key4)
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
            
            return jsonify({'message': 'Data successfully crawled and saved', 'file_path': file_path})
            
            # feedback data
            # return render_template('data.html', data=data)

# 엔드포인트: 저장된 JSON 파일 데이터를 웹 페이지에 보여주기
@bp.route('/show_data', methods=['GET'])
def show_data():
    file_path = 'crawled_data.json'
    if not os.path.exists(file_path):
        return jsonify({'error': 'No data available. Please crawl data first.'}), 404
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
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