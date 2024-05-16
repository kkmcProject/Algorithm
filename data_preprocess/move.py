import os
import shutil

def move_files(input_directory, output_directory):
    # 파일 이름에 "제함반" 또는 "세척반"이 포함된 파일 찾기
    matching_files = [f for f in os.listdir(input_directory) if "제함반" in f or "세척반" in f]

    # 각 파일을 출력 디렉토리로 이동
    for filename in matching_files:
        source_path = os.path.join(input_directory, filename)
        destination_path = os.path.join(output_directory, filename)
        shutil.move(source_path, destination_path)
        print(f"Moved '{filename}' to '{output_directory}'")

def main():
    # 예제 디렉토리 경로
    input_directory = '../data/csv_preprocessed'
    output_directory = '../data/moved'

    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 함수 호출
    move_files(input_directory, output_directory)

if __name__ == "__main__":
    main()
