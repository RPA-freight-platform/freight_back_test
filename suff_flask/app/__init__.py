from flask import Flask, render_template, request
import google_keywoed
#앱 서버 인스턴스

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        #get을 통해 전달받은 데이터를 확인
        key1 = request.args.get('keyword1')
        key2 = request.args.get('keyword2')
        key3 = request.args.get('keyword3')
        key4 = request.args.get('keyword4')
        key5 = request.args.get('keyword5')

        print(type(key1), key2, key3, key4, key5)

        if key1 == "" or key2 == "" or key3 == "" or key4 == "" or key5 == "":
            return render_template('index.html')
        else:
            #키워드 크롤링
            value1 = google_keywoed.get_keyword_number(key1)
            value2 = google_keywoed.get_keyword_number(key2)
            value3 = google_keywoed.get_keyword_number(key3)
            value4 = google_keywoed.get_keyword_number(key4)
            value5 = google_keywoed.get_keyword_number(key5)

            # feedback data
            data = {'key1:': value1, 'key2' : value2, 'key3' : value3, 'key4' : value4, 'key5' : value5}
            return render_template('index.html', data=data)
    return app
#라우팅 - 데코레이터
