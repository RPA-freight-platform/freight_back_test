from flask import Flask, render_template, request
import google_keywoed
#앱 서버 인스턴스

app = Flask(__name__)
 
#라우팅 - 데코레이터
@app.route('/')
def index():
    #get을 통해 전달받은 데이터를 확인
    key1 = request.args.get('keyword1')
    key2= request.args.get('keyword2')
    print(key1, key2)

    if key1 is None or key2 is None:
        return render_template('index.html')
    else:
        #키워드 크롤링
        value1 = google_keywoed.get_keyword_number(key1)
        value2 = google_keywoed.get_keyword_number(key2)

        # feedback data
        data = {'key1:': value1, 'key2' : value2}
        return render_template('index.html', data=data)

#메인 테스트
if __name__== "__main__":
    app.run(debug=True)