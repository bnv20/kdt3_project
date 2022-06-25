from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import numpy as np
from datetime import datetime
from generate import Generate




class Topic:
    def __init__(self):
        model_url = './etri_et5'
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
        self.generate = Generate(model_url)

    def main_page(self, url,topic):
        # 모듈 import
        import re
        import numpy as np
        from datetime import datetime
        
        # 정치면 메인 페이지 요청 -> html로 파싱
        
        req = requests.get(url, headers = self.headers)
        target = BeautifulSoup(req.content, 'html.parser')

        url_main = 'https://news.naver.com/'

        total = {}
        link = {}
        if topic == '정치':
            select = target.select('div.cluster_foot_inner > a')
        else:
            select = target.select('div.cluster_head_inner > a')
            
        for idx, tag in enumerate(select):

            each_url = url_main + tag['href'] # 각 헤드라인 서브 페이지 링크

            try: 
                news_num = int(re.match('[0-9]+', tag.text).group()) # 관련 기사 갯수
            except:
                news_num = np.nan

            # 헤드라인 서브 페이지 요청 -> html로 파싱
            sub_req = requests.get(each_url, headers = self.headers)
            page = BeautifulSoup(sub_req.content, 'html.parser')

            # 헤드라인 서브 페이지에서 가장 첫번째 기사 제목 (편의상 넣음 꼭 필요한 것은 아님)
            topic = page.select('div > ul > li > dl > dt')[1].text.strip() 

            # link 딕셔너리에 헤드라인 서브 페이지 링크, 관련 기사 건수, 첫번째 기사 제목  
            link[idx] = {'head_link':each_url, '관련기사':news_num, 'topic': topic} 

            # 헤드라인 서브 페이지 별로 언론사 리스트 추출
            np_list = page.select('span.writing')
            counter = {}
            for np_name in np_list:
                if np_name.text in ['조선일보', '중앙일보', '경향신문', '한겨레', '한국일보', '동아일보']:
                    if np_name.text not in counter:
                        counter[np_name.text] = 0
                    counter[np_name.text] += 1
                else:
                    pass
            total[idx] = counter # key: index / value : 언론사 별 기사 

        df1 = pd.DataFrame.from_dict(link, orient = 'index') # 링크, 관련기사 수, topic 있는 dataframe
        df2 = pd.DataFrame.from_dict(total, orient = 'index') # 각 언론사별 기사 갯수 있는 dataframe

        # merge
        df3 = pd.merge(df1.reset_index(), df2.reset_index(), on = 'index', how = 'outer').drop('index', axis = 1)

        global con
        global pro
        con = ['조선일보', '중앙일보']
        pro = ['경향신문', '한겨레']
        

        for name in con+pro:
            df3[f'{name}_presence'] = df3[f'{name}'].apply(lambda x :1 if x>0 else 0)
        df3['보수'] = df3['조선일보_presence'] + df3['중앙일보_presence'] # 보수신문 2개 있는지
        df3['진보'] = df3['경향신문_presence'] + df3['한겨레_presence'] # 진보신문 2개 있는지
        df3['합계'] = df3['보수'] + df3['진보']
        df3 = df3.drop(['조선일보_presence','중앙일보_presence','경향신문_presence','한겨레_presence'], axis=1)
        
        return df3

    def choice_title(self, url,topic):
        df3 = self.main_page(url,topic)
        
        global max_idx
        global selected_url
        
        if df3['합계'].argmax() == df3['관련기사'].argmax():
            max_idx = df3['합계'].argmax()
            selected_url = df3['head_link'][max_idx]
        elif len(df3[(df3['진보'] > 0) & (df3['보수'] > 0)]) > 0:
            max_idx = df3['관련기사'].argmax()
            selected_url = df3['head_link'][max_idx]
        else:
            max_idx = df3['합계'].argmax()
            selected_url = df3['head_link'][max_idx]


        global new_con
        global new_pro
        
        if df3['합계'][max_idx] == 4:
            print('관련기사 건수', df3['관련기사'].max())
            print('기사 4개, 선택된 url', selected_url)

            # 기사 4개 일때 언론사는 원래 그대로 
            new_con = con
            new_pro = pro
            print('선택한 언론사', new_pro + new_con)

        # 보수, 진보 합쳐서 3개 있는 df - 관련기사 가장 많은 헤드라인의 링크
        elif df3['합계'][max_idx] == 3:
            print('관련기사 건수', df3['관련기사'].max())
            print('기사 3개, 선택된 url', selected_url)
            # 여기에 포함 안된 언론사
            absent_name = df3.loc[max_idx][pro+con].notna().idxmin()
            print('제외된 언론사', absent_name)

            # 기사 3개 일때 선택할 언론사
            if absent_name in pro:
                new_pro = list(set(pro) - {absent_name}) + ['한국일보']
                new_con = con
            else:
                new_pro = pro
                new_con = list(set(con) - {absent_name}) + ['동아일보']
            print('선택한 언론사', new_pro + new_con)

        # 보수, 진보 각각 1개 있는 df - 관련기사 가장 많은 헤드라인의 링크
        elif (df3['합계'][max_idx] < 3) &( df3['합계'][max_idx]>0):
            print('관련기사 건수', df3['관련기사'].max())
            print('기사 2개, 선택된 url', selected_url)
            # 여기에 포함 안된 언론사
            absent_name_con = df3.loc[max_idx][con].notna().idxmin()
            absent_name_pro = df3.loc[max_idx][pro].notna().idxmin()
            print('제외된 언론사', absent_name_con, absent_name_pro)

            # 보수, 진보 각각 1개씩 있을 때 선택할 언론사
            new_pro = list(set(pro) - {absent_name_pro}) + ['한국일보']
            new_con = list(set(con) - {absent_name_con}) + ['동아일보']
            print('선택한 언론사', new_pro + new_con)

        return selected_url
    # 선택된 헤드라인 페이지에서 신문사별로 링크 따오기
    
    def compare_time(self,links):
        article_times = {} 
        for key, url in links.items():
            req = requests.get(url, headers = self.headers)
            target = BeautifulSoup(req.content, 'html.parser')
            time = target.select('span.t11')[-1].text # 기사 입력 시간 추출 (최초 작성 후 수정본이 있을때 수정된 시간으로 추출 / 만약 최초 작성 시간 기준을 하고 싶으면 인덱스[0]) 
            time = time.replace('오후', 'PM').replace('오전', 'AM') # 오후 -> PM, 오전 -> AM 변경
            time = datetime.strptime(time, '%Y.%m.%d. %p %I:%M') # datetime 으로 파싱
            article_times[key] = time # key: 원래 딕셔너리의 key 입력, value: 기사 입력 시간
        
        selected_article = links[max(article_times, key = article_times.get)] # article_times 딕셔너리의 value가 max인(가장 최근인) key로 con_link1 딕셔너리의 value(링크)찾기
        return selected_article

    def choice_link(self,url,topic):
        
        import requests
        from bs4 import BeautifulSoup as bs
        import re
        import pandas as pd
        import numpy as np
        from datetime import datetime
        
        selected_url = self.choice_title(url,topic)
        req = requests.get(selected_url, headers = self.headers)
        target = BeautifulSoup(req.content, 'html.parser')

        con_link1 = {} # 보수 언론사 1
        con_link2 = {} # 보수 언론사 2
        pro_link1 = {} # 진보 언론사 1
        pro_link2 = {} # 진보 언론사 2
        con_num1 = 0 
        con_num2 = 0
        pro_num1 = 0
        pro_num2 = 0

        for tag in target.select('div > ul > li > dl'):
            if tag.select_one('dd > span.writing').text == new_con[0]: # 보수 언론사 1 이름과 동일할 경우
                con_num1 += 1 # 기사 번호
                con_link1[con_num1] = tag.select_one('dt > a')['href'] # 기사 번호 당 링크
            if tag.select_one('dd > span.writing').text == new_con[1]: # 보수 언론사 2 이름과 동일할 경우
                con_num2 += 1 # 기사 번호
                con_link2[con_num2] = tag.select_one('dt > a')['href'] # 기사 번호 당 링크
            if tag.select_one('dd > span.writing').text == new_pro[0]: # 진보 언론사 1 이름과 동일할 경우
                pro_num1 += 1 # 기사 번호
                pro_link1[pro_num1] = tag.select_one('dt > a')['href'] # 기사 번호 당 링크
            if tag.select_one('dd > span.writing').text == new_pro[1]: # 진보 언론사 2 이름과 동일할 경우
                pro_num2 += 1 # 기사 번호
                pro_link2[pro_num2] = tag.select_one('dt > a')['href'] # 기사 번호 당 링크
            else:
                pass

        total_links = {new_con[0]: con_link1, new_con[1]: con_link2, new_pro[0]: pro_link1, new_pro[1]: pro_link2}
            

        final_links = {}
        for name, link in total_links.items():
            try:
                final_links[name] = self.compare_time(link)
            except:
                pass

        return final_links

    def query_url(self, query):
        url = f'https://search.naver.com/search.naver?query={query}&where=news&ie=utf8&sm=nws_hty'
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        all_link = soup.select('a.info')
        link = []
        for j in range(len(all_link)):
            link.append(all_link[j]['href'])
        news_link = pd.DataFrame(link, columns = ['link'])
        naver_news_link = news_link[news_link['link'].str.contains('https://news.naver.com')]
        
        try:
            naver_news_link.iloc[0,0]
        except:
            return None
        
        return naver_news_link.iloc[0,0]


    def naver_news_crawling(self, url):
        req = requests.get(url,headers=self.headers)
        if re.search('https://sports.news.naver.com/',req.url):
            time, media_name, title, text = self.sport_contents(url)
            
        elif re.search('https://entertain.naver.com/',req.url):
            time, media_name, title, text = self.entertain_contents(url)
        
        else:
            try:
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')   
                title = soup.find(id= 'articleTitle').text
                
                text = soup.find(id = 'articleBodyContents').text
                text = text.split('_flash_removeCallback() {}\n\n')[-1]
                
                media_name = soup.select_one('div.article_header > div.press_logo > a > img')['title']
                time = soup.select_one('span.t11').text
                
            except:
                pass

        return time, media_name, title, text
        
    def sport_contents(self, url):
        req = requests.get(url, headers=self.headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        time = soup.find(class_='info').text.split('최종수정')[1].split('기사원문')[0].strip() # time
        time = time.replace('오전','AM').replace('오후','PM')
        time = datetime.strptime(time, '%Y.%m.%d. %p %I:%M') # datetime 으로 파싱
        title = soup.find(class_='title').text
        text = soup.find(id='newsEndContents').text.split('기사제공')[0].strip('\n')
        media = media_name = soup.select_one('#pressLogo > a > img')['alt']
        
        return time, media, title, text
        
    def entertain_contents(self, url):
        req = requests.get(url, headers=self.headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        
        time = soup.select_one('#content > div.end_ct > div > div.article_info > span > em').text.strip() # time
        time = time.replace('오전','AM').replace('오후','PM')
        
        media_name = soup.select_one('#content > div.end_ct > div > div.press_logo > a > img')['alt']
        title = soup.select_one('h2').text
        text = soup.select_one('#articeBody').text
        
        return time, media_name, title, text
        

    def sport_news(self, url):
        
        time_li = []; time_list= []
        media_li = []; title_li = []
        document_li = []

        req = requests.get(url, headers=self.headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        contents = soup.find_all(class_='today_item')
        for content in contents[:4]:
            link = url+content.find(class_='link_today')['href']  
            
            time, media, title, text = self.sport_contents(link)
            
            time_li.append(time)
            time_list.append(time) # 순서정렬용
            media_li.append(media) # media
            title_li.append(title) # title
            document_li.append(text)

        df = pd.DataFrame({'time_list':time_list,'time':time_li,'media':media_li,'title':title_li,'document':document_li})
        df.sort_values(by='time_list',ascending=False,inplace=True) # (시간 기준) 최신 순으로 정렬
        df.drop(['time_list'],axis=1,inplace=True) # 필요없는 컬럼 삭제
        return df


class Crawling(Topic):
    def __init__(self):
        super().__init__()

    def make_df(self, topic):
        
        if topic == '경제':
            url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'
        elif topic == '정치':
            url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
        elif topic == '사회':
            url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102'
        elif topic == "생활/문화":
            url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103'
        elif topic == '스포츠':
            url = 'https://sports.news.naver.com'
        else:
            return print ('"경제", "정치", "사회", "생활/문화","스포츠" 중에 골라주세요')


        if topic == '스포츠':
            final_df = super().sport_news(url)


        else:
            final_links = super().choice_link(url,topic)

            time = []
            media = []
            head = []
            body = []
            for name, link in final_links.items():
                t, media_name, title, text = self.naver_news_crawling(link)
                time.append(t); media.append(media_name)
                head.append(title); body.append(text)

            final_df = pd.DataFrame({'time':time,'media':media,'title':head,'document':body})
            final_df.document = final_df.document.apply(lambda x: re.sub('\n','',x))
            final_df.document = final_df.document.apply(lambda x: re.sub('\t','',x))
        final_df = self.generate.input_generate(final_df, 'document')

        return final_df


    def query(self, query):
        url = super().query_url(query)
        if url:
            time, media_name, title, text = super().naver_news_crawling(url)
            
            final_df = pd.DataFrame({'time':[time],'media':[media_name],'title':[title],'document':[text]})
            final_df.document = final_df.document.apply(lambda x: re.sub('\n','',x))
            final_df.document = final_df.document.apply(lambda x: re.sub('\t','',x))
            final_df = self.generate.input_generate(final_df, 'document')

            return final_df
        else:
            return None

    def choice_url(self,url):
        time, media, title, text = self.naver_news_crawling(url)
        final_df = pd.DataFrame({'time':[time],'media':[media],'title':[title],'document':[text]})
        final_df.document = final_df.document.apply(lambda x: re.sub('\n','',x))
        final_df.document = final_df.document.apply(lambda x: re.sub('\t','',x))
        final_df = self.generate.input_generate(final_df, 'document')

        return final_df

    def timer(self):
        final_df = pd.DataFrame()
        for topic in ["경제", "정치", "사회", "생활/문화","스포츠"]:
            df = self.make_df(topic)
            df['topic'] = topic
            df.document = df.document.apply(lambda x: re.sub('\n','',x))
            df.document = df.document.apply(lambda x: re.sub('\t','',x))

            final_df= pd.concat([final_df, df], ignore_index=True)
        final_df = self.generate.input_generate(final_df, 'document')
        return final_df
