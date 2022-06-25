from flask import Flask, request, jsonify
import re
import pandas as pd
import schedule

from crawling import Crawling

crawl = Crawling()

asa = schedule.every().day.at("8:50").do(crawl.timer())# 아침마다 보낼거

total = schedule.every().hour.at(":30").do(crawl.timer()) #30분마다 요약할거 뽑아옴

application = Flask(__name__)

@application.route("/")
def hello():
    return "서버 실행중"

@application.route("/politics", methods=['POST'])
def politics():
    pol = total.loc[total['topic'] == '정치']
    if len(pol) == 4:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": pol['media'][i] + ""
                                               "" + pol['generate_text'][i]
                        } for i in range(len(pol))
                    }
                ]
            }
        }

        # 답변 전송
        return jsonify(res)
    elif len(pol) == 3:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": pol['media'][i] + ""
                                               "" + pol['generate_text'][i]
                        }
                    } for i in range(len(pol))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)



@application.route("/economy", methods=['POST'])
def economy():
    eco = crawl.make_df('경제')

    if len(eco) == 4:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": eco['media'][i] + ""
                                               "" + eco['generate_text'][i]
                        }
                    } for i in range(len(eco))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)
    elif len(eco) == 3:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": eco['media'][i] + ""
                                               "" + eco['generate_text'][i]
                        }
                    } for i in range(len(eco))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)


@application.route("/society", methods=['POST'])
def society():
    soc = total.loc[total['topic'] == '사회']
    if len(soc) == 4:
            
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": soc['media'][i] + ""
                                               "" + soc['generate_text'][i]
                        }
                    } for i in range(len(soc))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)
    elif len(soc) == 3:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": soc['media'][i] + ""
                                               "" + soc['generate_text'][i]
                        }
                    } for i in range(len(soc))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)

@application.route("/culture", methods=['POST'])
def living():
    liv = total.loc[total['topic'] == '생활/문화']
    if len(liv) == 4:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": liv['media'][i] + ""
                                               "" + liv['generate_text'][i]
                        } for i in range(len(liv))
                    }
                ]
            }
        }

        # 답변 전송
        return jsonify(res)
    elif len(liv) == 3:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": liv['media'][0] + ""
                                               "" + liv['generate_text'][0]
                        }
                    } for i in range(len(liv))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)



@application.route("/sports", methods=['POST'])
def sport():
    spo = total.loc[total['topic'] == '스포츠']
    if len(spo) == 4:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": spo['media'][0] + ""
                                               "" + spo['generate_text'][0]
                        }
                    } for i in range(len(spo))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)
    elif len(spo) == 3:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": spo['media'][0] + ""
                                               "" + spo['generate_text'][0]
                        }
                    } for i in range(len(spo))
                ]
            }
        }

        # 답변 전송
        return jsonify(res)


@application.route('/search', methods = ['POST'])
def text():
    req = request.get_json()
    text = req["action"]["detailParams"]["sys_text"]["origin"]
    answer = crawl.query(text)
    answer1 = answer['generate_text']

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer1
                    }
                }
            ]
        }
    }
    return jsonify(res)

@application.route('/urlink', methods = ['POST'])
def urlink():
    req = request.get_json()
    url = req["action"]["detailParams"]["sys_url"]["origin"]
    if re.match('https://news.naver.com'):
        final_df = crawl.choice_url(url)
    else:
        answer = '네이버 뉴스 url를 입력해주세요'
    answer = final_df['generate_text']
    answer = crawl.choice_url('https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=100&oid=586&aid=0000032061')

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer['generate_text']
                    }
                }
            ]
        }
    }
    return jsonify(res)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)