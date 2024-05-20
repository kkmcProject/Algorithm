import pandas as pd
import os
import re


def merge_csv_files_by_date(input_directory, output_directory):
    # 날짜를 키로 하고 해당 날짜의 파일들을 리스트로 저장할 딕셔너리
    date_files_dict = {}

    # 새로운 열 이름 설정
    new_columns = [
        '품목번호', '업체', '품목', '과수', '원산지', '포장형태', '상품명', '입수', '단량',
        '제고/예비 생산 수량', '수량', '중량', '바코드', '상품명2', '작업인원', '작업시간', '품종',
        '원산지', '바코드2', '진열기간', '입수*수량', '작업난도', 'eta'
    ]

    # 디렉토리 내 모든 파일을 순회
    for filename in os.listdir(input_directory):
        # 날짜 부분 추출
        match = re.match(r'작업계획서\((\d{4}-\d{2}-\d{2})\).*\.csv', filename)
        if match:
            date = match.group(1)
            if date not in date_files_dict:
                date_files_dict[date] = []
            date_files_dict[date].append(filename)

    # 각 날짜에 대해 파일 병합
    for date, files in date_files_dict.items():
        dataframes = []
        for file in files:
            print(file, "시작")
            file_path = os.path.join(input_directory, file)
            df = pd.read_csv(file_path)

            # 열 이름 개수가 맞는지 확인하고 설정
            if df.shape[1] == len(new_columns):
                df.columns = new_columns
            elif df.shape[1] > len(new_columns):
                print(f"Warning: {file} has more columns than expected. Dropping extra columns.")
                df = df.iloc[:, :len(new_columns)]  # 필요한 열만 선택
                df.columns = new_columns  # 열 이름 설정
            else:
                print(f"Warning: {file} does not match the expected number of columns.")
                continue
            dataframes.append(df)

        # 모든 DataFrame을 행으로 합치기
        merged_df = pd.concat(dataframes, ignore_index=True)

        # 합쳐진 DataFrame을 새로운 CSV 파일로 저장
        output_file = os.path.join(output_directory, f"작업계획서({date}).csv")
        merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Merged file saved as '{output_file}'")


def main():
    # 예제 디렉토리 경로
    input_directory = '../data/csv_preprocessed'
    output_directory = '../data/merged'

    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 함수 호출
    merge_csv_files_by_date(input_directory, output_directory)


if __name__ == "__main__":
    main()
