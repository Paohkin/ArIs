<div align="center">
  
  # ArIs Chronicle
  
  ### 아리스와 함께 마왕을 무찌르고 보물을 획득하자!!

  [Link] https://paohkin.pythonanywhere.com/
  
  <p>$\rm{\normalsize{\color{#FF0000}모바일에서는\ 실행이\ 어렵습니다.\ PC에서\ 플레이해주세요!}}$</p>
  
</div>


## Extract Text Data

인게임 대사를 추출하기 위해 인게임 스토리 영상을 프레임 단위로 캡쳐한 뒤, EasyOCR을 사용하여 텍스트 추출

[KMS 유튜브] https://youtube.com/@kms3628?si=WQVfYy2fS_TxgUq1

[EasyOCR] https://github.com/JaidedAI/EasyOCR

캡쳐한 이미지 중 출력 완료된 대사만을 필터하기 위해 대사가 완료되면 나타나는 삼각형 아이콘을 reference로 사용

![chrome_Jin1yS5xsL](https://github.com/user-attachments/assets/5cbc67ce-de6e-4b60-bedc-5f990df49d34)

사용한 인게임 텍스트
- 태엽감는 꽃의 파반느 편 1장
- 태엽감는 꽃의 파반느 편 2장
- 아리스 인연 스토리
- 아리스(메이드) 인연 스토리
- 아리스 모모톡
- 아리스(메이드) 모모톡


## Data Preprocessing

1. 대화 쌍(pair) 작성

   아리스의 대사와 그 직전 대사로 이루어진 대화 쌍을 작성 (e.g. "찾았다. 꼬맹이" / "야, 야생의 꼬마 메이드님이 나타났습니다! (깜짝)")
  
2. Conversational Chat Format으로 전환

   대화 쌍을 각각 user와 assistant(아리스)에 대응하여 instruction을 추가한 형태로 전환
   
   (e.g. {"role": "system", "content": "너는 '블루 아카이브'라는 게임에 등장하는 캐릭터 '아리스'야. 내가 묻는 질문에 대해 '아리스' 답게 대답해 줘."},
   {"role": "user", "content": "아리스?"},
   {"role": "assistant", "content": "용사여…… 정말로 와 버린 것인가……")

   Please refer to [OpenAI official guides] https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset


## Dataset

대화의 주체가 선생과 아리스라는 점을 고려해, 실제 학습에는 인연 스토리와 모모톡 데이터만 사용

실제 dataset은 jsonl 형태지만 Hugging Face에는 csv 형태로 업로드하였음

[Hugging Face Link] https://huggingface.co/datasets/Paohkin/BlueArchive-Aris-Scripts


## Train

사용한 모델 : gpt-4o-mini

[About gpt-4o-mini] https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/

API를 통해 fine-tuning을 진행

![chrome_j73SAA8HRR](https://github.com/user-attachments/assets/4bede174-aed3-4187-99cf-cf9b36dbde6f)

Trained tokens : 18,978 / Epochs : 3 / Batch size : 1 / LR multiplier : 1.8


## Develop Game

pythonanywhere(https://www.pythonanywhere.com/) 에서 flask 기반으로 개발
