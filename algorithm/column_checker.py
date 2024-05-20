import pandas as pd
import glob
import numpy as np

# CSV 파일들이 있는 디렉토리 경로
directory_path = '../checker/merged/'

# 디렉토리 내의 모든 CSV 파일 경로를 리스트로 가져오기
csv_files = glob.glob(directory_path + '*.csv')

# 빈 딕셔너리 생성
items_dict = {}

# 각 CSV 파일 읽어들이고 필요한 열 추출하여 딕셔너리에 추가
for file in csv_files:
    df = pd.read_csv(file)
    extracted_columns = df[['품목', '작업난도']]

    # 각 행의 (품목, 작업난도) 값을 딕셔너리에 추가
    for row in extracted_columns.itertuples(index=False, name=None):

        품목, 작업난도 = row

        if 품목 in items_dict:
            items_dict[품목].add(작업난도)
        else:
            items_dict[품목] = set()
            items_dict[품목].add(작업난도)

# 딕셔너리 순회하면서 nan 값 제거
for key, value in items_dict.items():
    items_dict[key] = {v for v in value if not np.isnan(v)}

# nan 값이 제거된 딕셔너리 출력
for key, value in items_dict.items():
    print(f"{key}: {value}")
