import pandas as pd
import os


def excel_to_csv(excel_file):
    # Excel 파일 읽기
    xls = pd.ExcelFile(excel_file)

    # 파일 이름 추출 (확장자 제외)
    base_filename = os.path.splitext(os.path.basename(excel_file))[0]

    # 각 시트별로 CSV 파일로 저장
    for sheet_name in xls.sheet_names:
        if '반' in sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            csv_file = f"../data/csv/{base_filename}_{sheet_name}.csv"
            df.to_csv(csv_file, index=False)
            print(f"Sheet '{sheet_name}' saved as '{csv_file}'")


def main():
    # 예제 파일 경로
    excel_file = '../data/original/작업계획서(2023-09-26).xlsx'

    # 함수 호출
    excel_to_csv(excel_file)


if __name__ == "__main__":
    main()
