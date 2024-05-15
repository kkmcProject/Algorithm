import pandas as pd
import os

def excel_to_csv(excel_file, output_directory):
    # Excel 파일 읽기
    xls = pd.ExcelFile(excel_file)

    # 파일 이름 추출 (확장자 제외)
    base_filename = os.path.splitext(os.path.basename(excel_file))[0]

    # 각 시트별로 CSV 파일로 저장
    for sheet_name in xls.sheet_names:
        if '반' in sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            csv_file = os.path.join(output_directory, f"{base_filename}_{sheet_name}.csv")
            df.to_csv(csv_file, index=False)
            print(f"Sheet '{sheet_name}' saved as '{csv_file}'")

def process_directory(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            excel_file = os.path.join(input_directory, filename)
            excel_to_csv(excel_file, output_directory)

def main():
    # 예제 디렉토리 경로
    input_directory = '../data/original'
    output_directory = '../data/csv'

    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 함수 호출
    process_directory(input_directory, output_directory)

if __name__ == "__main__":
    main()
