import pandas as pd
import os
import re


def merge_csv_files(directory, common_part, output_file):
    # 디렉토리 내의 모든 파일 목록을 가져옴
    files = os.listdir(directory)

    # 공통 부분을 포함하는 파일만 필터링
    matching_files = [f for f in files if common_part in f and f.endswith(".csv")]

    # 빈 데이터프레임 생성
    merged_df = pd.DataFrame()

    # 각 파일을 읽어 데이터프레임에 추가
    for file in matching_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    # 최종 병합된 데이터프레임을 CSV 파일로 저장
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Merged file saved as '{output_file}'")


def process_directory(input_directory, output_directory):
    # 파일 이름에서 공통 부분 추출
    common_parts = set()
    for filename in os.listdir(input_directory):
        match = re.match(r'(.+?)(_\d+반)?\.csv', filename)
        if match:
            common_parts.add(match.group(1))

    # 각 공통 부분에 대해 파일 병합
    for common_part in common_parts:
        output_file = os.path.join(output_directory, f"{common_part}_merged.csv")
        merge_csv_files(input_directory, common_part, output_file)


def main():
    # 예제 디렉토리 경로
    input_directory = '../data/csv_preprocessed'
    output_directory = '../data/merged'

    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 함수 호출
    process_directory(input_directory, output_directory)


if __name__ == "__main__":
    main()
