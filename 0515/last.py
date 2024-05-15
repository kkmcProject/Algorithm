import os
import pandas as pd


def filter_csv(input_csv, output_csv):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # CSV 파일 읽기
    df = pd.read_csv(input_csv)
    print(df)
    # 첫 열이 숫자인 행만 필터링
    filtered_df = df[df.iloc[:, 0].apply(lambda x: str(x).isdigit())]
    print(filtered_df)
    # 필터링된 DataFrame을 새로운 CSV 파일로 저장하거나 모든 행이 삭제된 경우 파일 삭제
    if filtered_df.empty:
        print(f"All rows in '{input_csv}' have non-numeric first columns. Deleting the file.")
        os.remove(input_csv)
    else:
        filtered_df.to_csv(output_csv, index=False)
        print(f"Filtered rows saved to '{output_csv}'")


def process_directory(directory):
    for filename in os.listdir(directory):
        input_csv = os.path.join(directory, filename)
        output_csv = os.path.join(directory, filename)
        filter_csv(input_csv, output_csv)


def main():
    # 예제 디렉토리 경로
    input_directory = '../data/csv_preprocessed'

    # 함수 호출
    process_directory(input_directory)


if __name__ == "__main__":
    main()
