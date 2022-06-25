ET5 모델    
  
**최종모델 : ET5모델에 train data 290,000개, epochs 12로 fine-tuning**  
    
  
추가학습으로 fine-tuning진행 / 학습 후 모델 저장, 모델 불러와서 추가 학습 진행   
  
** google colab pro plus 사용  
runtime이 최대 24시간이므로,  
여건상 시간에 맞춰 데이터를 분할하여 학습 후 모델을 저장하고, 저장한 모델에 추가학습 하는 방식으로 진행  
(추가학습한 모델과 한번에 학습한 모델을 비교한 결과 비슷한 성능을 보였음)  
10 일에 걸쳐 총 train data 290,000 개, epochs 12로 fine-tuning  
  
  
학습 과정  
  
train_data 60,000개 epochs 8씩 추가학습  
1.train_data 60,000 epochs 8  
2.train_data 120,000 epochs 8  
3.train_data 180,000 epochs 8  
4.train_data 240,000 epochs 8  
  
train_data 240,000 epochs 8 모델에 train_data 30,000 개 추가학습  
5. train_data 270,000 epochs 8  
  
train_data 270,000 epochs 8 모델에 train_data 270,000 개 epochs4 추가학습  
6. train_data 270,000 epochs 9  
7. train_data 270,000 epochs 10  
8. train_data 270,000 epochs 11  
9. train_data 270,000 epochs 12  
  
train_data 270,000 epochs 12 모델에 train_data 2,0000 개 추가학습  
**10.train_data 290,000 epochs 12**  
