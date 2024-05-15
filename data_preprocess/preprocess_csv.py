import os
import pandas as pd

def filter_csv(input_csv, output_csv):
    # CSV 파일 읽기
    df = pd.read_csv(input_csv)

    # 1열에 내용이 있는 행만 필터링 (1열이 빈 값이 아닌 행만 선택)
    filtered_df = df[df.iloc[:, 0].notna()]

    # 필터링된 DataFrame을 새로운 CSV 파일로 저장
    filtered_df.to_csv(output_csv, index=False)
    print(f"Filtered rows saved to '{output_csv}'")

def main(input_directory, output_directory):
    # 입력 디렉토리 내의 파일 중 이름에 '반'이 포함된 CSV 파일 처리
    for filename in os.listdir(input_directory):
        input_csv = os.path.join(input_directory, filename)
        output_csv = os.path.join(output_directory, filename)
        filter_csv(input_csv, output_csv)

if __name__ == "__main__":
    # 예제 입력 및 출력 디렉토리 경로
    input_directory = '../data/csv'
    output_directory = '../data/csv_preprocessed'

    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 함수 호출
    main(input_directory, output_directory)
