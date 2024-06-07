import os
import pandas as pd

def remove_non_numeric_rows_from_csv(file_path):
    # CSV 파일을 DataFrame으로 읽어옴
    df = pd.read_csv(file_path)

    # 첫 번째 열 값이 숫자가 아닌 행을 모두 제거
    df = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()]

    # 수정된 DataFrame을 다시 CSV 파일로 저장
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Processed {file_path}")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                remove_non_numeric_rows_from_csv(file_path)

# 사용 예시
directory_path = "/tmp/pycharm_project_138/data/merged"
process_directory(directory_path)
