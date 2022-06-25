from flask import Flask, request, jsonify
import re
import pandas as pd
# import schedule

from crawling import Crawling

crawl = Crawling()

# asa = schedule.every().day.at("8:50").do(crawl.timer())# 아침마다 보낼거

# total = schedule.every().hour.at(":30").do(crawl.timer()) #30분마다 요약할거 뽑아옴

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


@application.route("/society", methods=['GET','POST'])
def society():
    img_url  = 'C:/Users/han71/Documents/카카오톡 받은 파일/dd.jpg'

    t1 = "는 9억원 이하 주택을 2년 이상 보유하고 되팔 경우 시세 차익에 붙는 양도소득세를 면제받고, 12억원 초과 집을 파는 사람들도 이와 달리 양도소득세가 줄어들게 됨에 따라,부는 국무회의에서 양도소득세 비과세 기준을 상향하는 개정 소득세법의 공포일을 8일로 확정했다."
    
    t2 = "대통령은 시장의 대기 매물이 늘어나자 여러 개정법을 시행하기 위해 1세대 1주택에 대한 양도소득세 비과세 기준 상향 조치를 8일부터 시행한다."

    t3 = "는 8일부터 1가구 1암동에 대한 양도소득세 비과세 기준 상향 조치가 실거래 양도가격이 12억원 이하인 경우 비과세 혜택을 주는 개정 소득세법의 공포일을 8일로 확정했다."

    t4 = "과 국민힘은 정부의 부동산시장 안정을 해칠 수 있다는 반대 목소리와 정의당 등 소수 정당의 조세형평성 악화 등으로 인한 반대에도 불구하고 오는 8일 상향 조정된 1세대 1마스에 대한 양도소득세 비과세기준이 적용될 전망이며, 주택 매도 잔금 청산일과 등기일 중 빠른 날이 기준점이 된다."
            
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                      {
                        "carousel": {
                            "type":"basicCard",
                            "items":[
                                    {"title" : '조선일보',
                                    "description":t1[:73]+"..." if len(t1) > 76 else t1,
                                    "thumbnail":{
                                        "imageUrl" : img_url
                                        },
                                    "buttons" : [{
                                        "action":"message",
                                        "label":"전체 text",
                                        "messageText" : t1
                                    }]
                                },
                                {   "title" : '중앙일보',
                                    "description":t2[:73]+"..." if len(t2) > 76 else t2,
                                    "thumbnail":{
                                        "imageUrl" : img_url
                                        },
                                    "buttons" : [{
                                        "action":"message",
                                        "label":"전체 text",
                                        "messageText" : t2
                                    }]
                                },
                                {   "title" : '경향신문',
                                    "description":t3[:73]+"..." if len(t3) > 76 else t3,
                                    "thumbnail":{
                                        "imageUrl" : img_url
                                        },
                                    "buttons" : [{
                                        "action":"message",
                                        "label":"전체 text",
                                        "messageText" : t3
                                    }]
                                },
                                {   'title':'한겨례',
                                    "description":t4[:73]+"..." if len(t4) > 76 else t4,
                                    "thumbnail":{
                                        "imageUrl" : img_url
                                        },
                                    "buttons" : [{
                                        "action":"message",
                                        "label":"전체 text",
                                        "messageText" : t4
                                    }]
                                }
                            ]
                        }
                    }
                ]
            }
        }
    {
    "version": "2.0",
    "template": {
        "outputs": [
        {
            "carousel": {
            "type": "basicCard",
            "items": [
                {
                "title": "보물상자",
                "description": "보물상자 안에는 뭐가 있을까",
                "thumbnail": {
                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                },
                "buttons": [
                    {
                    "action": "message",
                    "label": "열어보기",
                    "messageText": "짜잔! 우리가 찾던 보물입니다"
                    },
                    {
                    "action":  "webLink",
                    "label": "구경하기",
                    "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                    }
                ]
                },
                {
                "title": "보물상자2",
                "description": "보물상자2 안에는 뭐가 있을까",
                "thumbnail": {
                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                },
                "buttons": [
                    {
                    "action": "message",
                    "label": "열어보기",
                    "messageText": "짜잔! 우리가 찾던 보물입니다"
                    },
                    {
                    "action":  "webLink",
                    "label": "구경하기",
                    "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                    }
                ]
                },
                {
                "title": "보물상자3",
                "description": "보물상자3 안에는 뭐가 있을까",
                "thumbnail": {
                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                },
                "buttons": [
                    {
                    "action": "message",
                    "label": "열어보기",
                    "messageText": "짜잔! 우리가 찾던 보물입니다"
                    },
                    {
                    "action":  "webLink",
                    "label": "구경하기",
                    "webLinkUrl": "https://e.kakao.com/t/hello-ryan"
                    }
                ]
                }
            ]
            }
        }
        ]
    }
}
    # 답변 전송
    return jsonify(res)

    # elif len(soc) == 3:
    #     res = {
    #         "version": "2.0",
    #         "template": {
    #             "outputs": [
    #                 {
    #                     "simpleText": {
    #                         "text": soc['media'][i] + ""
    #                                            "" + soc['generate_text'][i]
    #                     }
    #                 } for i in range(len(soc))
    #             ]
    #         }
    #     }

    #     # 답변 전송
    #     return jsonify(res)

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