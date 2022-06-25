# AI 기반 데일리 뉴스 요약 챗봇 서비스 
### 참조 폴더
- Crawling-main: N사 포털의 뉴스 기사를 크롤링하는 코드입니다.
- Flask-main: API의 기반이 되는 Flask 코드입니다.
- NLP-model-main-scoring: bert score를 측정하는 코드입니다.
- model_ET5: 최종 모델(epoch:12, data:290,000건)의 학습 과정이 담긴 코드 폴더입니다.



## 요약
- 발표 영상: 
#### 1. 서비스 개요
- AI 기반 뉴스 요약기 구축 후 다양한 신문사의 기사를 요약하여 전달하는 챗봇 서비스 진행

![image](https://user-images.githubusercontent.com/86218931/145512459-1cf1a794-c475-4be1-bc13-4c50d386d33b.png)

#### 2. 모델 개발
- 개발 환경: VScode(크롤링), Google Colab(딥러닝 모델), PyCharm(서비스 구현)
- 주요 사용 라이브러리 PyTorch, Transformers, Sentencepiece(0.1.91), Flask 등
- 학습 데이터셋(Fine-tuning): AI Hub 문서요약 텍스트(https://aihub.or.kr/aidata/8054) 다운로드 후, 뉴스텍스트 총 30만 건(train, validation 포함) 중에 기사 원본(sentence), 생성요약문(abstractive) 을 추출하여 데이터셋을 구축함(train 29만 건, test 1만 건)

#### 3. 모델 구축
- 2019년 Google에서 출시한 T5(Text To Text Transfer Transformer) 모델을 이용하여 요약 모델 구축

![image](https://user-images.githubusercontent.com/86218931/145512439-a9d28981-5666-4055-bf63-db40d6693c6b.png)

- ETRI(https://aiopen.etri.re.kr/service_dataset.php) 에서 제공하는 한국어 언어모델 ET5의 API를 신청하여 사용 승인을 받은 후 Fine-tuning을 진행 

![image](https://user-images.githubusercontent.com/86218931/145513113-d6db307a-a385-426e-ba65-7e405b7154d2.png)

- 생성 요약문 예시

![image](https://user-images.githubusercontent.com/86218931/145513288-257d10f6-e142-40de-9c29-936d5d96e466.png)

#### 4. 모델 성능 비교
- 모델 성능 비교를 위해 BERT Score 활용(https://github.com/Tiiiger/bert_score)
- 서비스 구현에는 29만 건 데이터를 epochs 12로 학습한 ET5 모델을 선정

![image](https://user-images.githubusercontent.com/86218931/145513802-641ed1d7-5cca-4c82-9da1-4c10166d3ecd.png)

- Colab 런타임 24시간 제한으로 인해 데이터를 나누어 Fine-tuning 진행 후 모델을 저장한 뒤 추가 학습 진행

![image](https://user-images.githubusercontent.com/86218931/145513998-31dfca55-f752-4d5d-bfff-bec50a5c36be.png)

#### 5. 서비스 배포
- 포털에서 뉴스기사를 크롤링하고 Fine-tuning으로 구축한 모델을 통해 요약문을 생성한 뒤 kakao i open builder를 이용하여 사용자에게 챗봇으로 뉴스 기사 요약문 서비스를 배포함

![image](https://user-images.githubusercontent.com/86218931/145514090-89c30bce-dd47-4457-a431-29f83e12e908.png)
