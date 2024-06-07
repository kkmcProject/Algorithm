import sys
import json
import pandas as pd
from collections import defaultdict
import codecs


def heuristic_allocation(rows, group_info):
    print("Starting heuristic allocation")

    # 데이터 프레임 생성
    df = pd.DataFrame(rows)
    print("DataFrame created")

    # 그룹 정보 디버깅
    print("Group info:", group_info)

    # 그룹 정보
    group_names = [group['name'] for group in group_info]
    group_sizes = {group['name']: group['count'] for group in group_info}
    group_hard = {group['name']: 0 for group in group_info}
    group_counts = {group['name']: 0 for group in group_info}
    group_fruit_counts = {group['name']: defaultdict(int) for group in group_info}

    # 작업을 hard 값 기준으로 내림차순 정렬
    df = df.sort_values(by='hard', ascending=False).reset_index(drop=True)

    allocation = {}

    for i in range(len(df)):
        task = df.loc[i]
        # 각 그룹의 eta와 fruit 종류 수를 고려하여 그룹 선택
        min_eta_group = min(group_names,
                            key=lambda g: (group_hard[g] / group_sizes[g], group_fruit_counts[g][task['fruit']]))

        allocation[task['index']] = min_eta_group
        group_hard[min_eta_group] += task['hard']
        group_counts[min_eta_group] += 1
        group_fruit_counts[min_eta_group][task['fruit']] += 1

    print("Initial allocation from heuristic:")
    for group in group_names:
        eta = group_hard[group] / group_sizes[group]
        fruit_variety = len(group_fruit_counts[group])
        print(f"Group {group} eta: {eta}, fruit variety: {fruit_variety}")

    # 할당 결과를 데이터프레임에 추가
    df['group'] = df['index'].map(allocation)

    print("Allocation:")
    print(df[['index', 'group']])
    print(df)
    return df


def main():
    print(f"Received {len(sys.argv) - 1} arguments.")
    if len(sys.argv) != 3:
        print("Usage: script.py <rows_json> <workGroup_json>")
        return

    rows_json = sys.argv[1]
    workGroup_json = sys.argv[2]

    print(f"workGroup_json path: {workGroup_json}")

    try:
        with codecs.open(rows_json, 'r', encoding='utf-8-sig') as f:
            rows_data = f.read()
            if not rows_data:
                raise ValueError("Empty rows JSON file")
            rows = json.loads(rows_data)

        with codecs.open(workGroup_json, 'r', encoding='utf-8-sig') as f:
            workGroup_data = f.read()
            if not workGroup_data:
                raise ValueError("Empty workGroup JSON file")
            workGroup = json.loads(workGroup_data)

        print("Received rows and workGroup JSON data from files.")
        result_df = heuristic_allocation(rows, workGroup)

        # 결과를 원래 rows_json 파일에 저장
        result_df.to_json(rows_json, orient='records', force_ascii=False)
        print(f"Result saved to {rows_json}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()