import pandas as pd
from collections import defaultdict


def combine_fruits_with_index(rows):
    # 과일 종류별로 작업을 합산하고 index 저장
    combined = defaultdict(lambda: {'hard': 0, 'indices': []})
    for row in rows:
        fruit = row['fruit']
        combined[fruit]['hard'] += row['hard']
        combined[fruit]['indices'].append(row['index'])

    combined_rows = [{'fruit': fruit, 'hard': data['hard'], 'indices': data['indices']} for fruit, data in
                     combined.items()]
    return combined_rows


def split_highest_hard(combined_rows, original_rows):
    # 가장 높은 hard 값을 가진 과일을 찾고, 이를 두 번째로 높은 hard 값에 맞춰 여러 개로 나눔
    df = pd.DataFrame(combined_rows)
    df = df.sort_values(by='hard', ascending=False).reset_index(drop=True)

    highest_hard = df.loc[0, 'hard']
    second_highest_hard = df.loc[1, 'hard']
    highest_fruit = df.loc[0, 'fruit']

    new_rows = []
    remaining_hard = 0
    split_indices = []

    if highest_hard > second_highest_hard:
        for row in original_rows:
            if row['fruit'] == highest_fruit:
                remaining_hard += row['hard']
                split_indices.append(row['index'])
                if remaining_hard >= second_highest_hard:
                    split_hard = remaining_hard - row['hard']
                    if split_hard > 0:
                        new_rows.append({'fruit': highest_fruit, 'hard': split_hard, 'indices': split_indices[:-1]})
                    split_hard = row['hard']
                    new_rows.append({'fruit': highest_fruit, 'hard': split_hard, 'indices': [split_indices[-1]]})
                    remaining_hard = 0
                    split_indices = []

        if remaining_hard > 0:
            new_rows.append({'fruit': highest_fruit, 'hard': remaining_hard, 'indices': split_indices})
        df = df.drop(0).reset_index(drop=True)

    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)

    # 나뉜 과일들의 hard 값 출력
    for row in new_rows:
        print(f"Split fruit: {row['fruit']}, Hard: {row['hard']}, Indices: {row['indices']}")

    return df.to_dict('records')


def calculate_eta(allocation, group_sizes):
    # 각 그룹의 eta 값을 계산
    group_hard = {group: 0 for group in group_sizes}
    for group, tasks in allocation.items():
        group_hard[group] = sum(task['hard'] for task in tasks)

    group_eta = {group: group_hard[group] / group_sizes[group] for group in group_sizes}
    return group_eta


def heuristic_allocation(combined_rows, group_info):
    # 그룹 정보
    group_names = [group['name'] for group in group_info]
    group_sizes = {group['name']: group['size'] for group in group_info}

    # 데이터 프레임 생성
    df = pd.DataFrame(combined_rows)

    # 작업을 hard 값 기준으로 내림차순 정렬
    df = df.sort_values(by='hard', ascending=False).reset_index(drop=True)

    allocation = defaultdict(list)
    group_hard = {group: 0 for group in group_names}

    for i in range(len(df)):
        task = df.loc[i]
        # 각 그룹의 eta를 고려하여 그룹 선택
        min_eta_group = min(group_names, key=lambda g: group_hard[g] / group_sizes[g])

        allocation[min_eta_group].append(task)
        group_hard[min_eta_group] += task['hard']

    # 각 그룹의 eta 값 계산 및 출력
    group_eta = calculate_eta(allocation, group_sizes)

    print("Allocation from heuristic:")
    for group in group_names:
        eta = group_eta[group]
        fruits = [task['fruit'] for task in allocation[group]]
        indices = [index for task in allocation[group] for index in task['indices']]
        print(f"Group {group} eta: {eta}, fruits: {fruits}, indices: {indices}")

    return allocation, group_eta

def main():
    rows = [
        {'fruit': 'Kiwi', 'hard': 8200, 'index': 1}, {'fruit': 'Kiwi', 'hard': 6600, 'index': 2},
        {'fruit': 'Kiwi', 'hard': 2680, 'index': 3}, {'fruit': 'Kiwi', 'hard': 2160, 'index': 4},
        {'fruit': 'Kiwi', 'hard': 29120, 'index': 5}, {'fruit': 'Kiwi', 'hard': 33600, 'index': 6},
        {'fruit': 'Kiwi', 'hard': 2780, 'index': 7}, {'fruit': 'Kiwi', 'hard': 12960, 'index': 8},
        {'fruit': 'Kiwi', 'hard': 4420, 'index': 9}, {'fruit': 'Kiwi', 'hard': 2400, 'index': 10},
        {'fruit': 'Kiwi', 'hard': 44800, 'index': 11}, {'fruit': 'Kiwi', 'hard': 1080, 'index': 12},
        {'fruit': 'Kiwi', 'hard': 120, 'index': 13}, {'fruit': 'Kiwi', 'hard': 60, 'index': 14},
        {'fruit': 'Kiwi', 'hard': 340, 'index': 15}, {'fruit': 'Kiwi', 'hard': 1380, 'index': 16},
        {'fruit': 'Kiwi', 'hard': 3520, 'index': 17}, {'fruit': 'Kiwi', 'hard': 480, 'index': 18},
        {'fruit': 'Kiwi', 'hard': 1320, 'index': 19}, {'fruit': 'Kiwi', 'hard': 640, 'index': 20},
        {'fruit': 'Kiwi', 'hard': 800, 'index': 21}, {'fruit': 'Kiwi', 'hard': 32640, 'index': 22},
        {'fruit': 'Kiwi', 'hard': 39600, 'index': 23}, {'fruit': 'Kiwi', 'hard': 600, 'index': 24},
        {'fruit': 'Kiwi', 'hard': 2160, 'index': 25}, {'fruit': 'Kiwi', 'hard': 800, 'index': 26},
        {'fruit': 'Kiwi', 'hard': 1800, 'index': 27}, {'fruit': 'Lime', 'hard': 1440, 'index': 28},
        {'fruit': 'Lime', 'hard': 240, 'index': 29}, {'fruit': 'Lime', 'hard': 3120, 'index': 30},
        {'fruit': 'Lime', 'hard': 560, 'index': 31}, {'fruit': 'Lime', 'hard': 720, 'index': 32},
        {'fruit': 'Lime', 'hard': 300, 'index': 33}, {'fruit': 'Lime', 'hard': 180, 'index': 34},
        {'fruit': 'Kiwi', 'hard': 6360, 'index': 35}, {'fruit': 'Kiwi', 'hard': 3480, 'index': 36},
        {'fruit': 'Kiwi', 'hard': 2280, 'index': 37}, {'fruit': 'Kiwi', 'hard': 480, 'index': 38},
        {'fruit': 'Kiwi', 'hard': 160, 'index': 39}, {'fruit': 'Kiwi', 'hard': 120, 'index': 40},
        {'fruit': 'Kiwi', 'hard': 240, 'index': 41}, {'fruit': 'Kiwi', 'hard': 5120, 'index': 42},
        {'fruit': 'Kiwi', 'hard': 7920, 'index': 43}, {'fruit': 'Lemon', 'hard': 8040, 'index': 44},
        {'fruit': 'Mango', 'hard': 2080, 'index': 45}, {'fruit': 'Mango', 'hard': 1200, 'index': 46},
        {'fruit': 'Mango', 'hard': 7040, 'index': 47}, {'fruit': 'Mango', 'hard': 800, 'index': 48},
        {'fruit': 'Mango', 'hard': 1760, 'index': 49}, {'fruit': 'Mango', 'hard': 2760, 'index': 50},
        {'fruit': 'Mango', 'hard': 1320, 'index': 51}, {'fruit': 'Mango', 'hard': 2700, 'index': 52},
        {'fruit': 'Mango', 'hard': 3700, 'index': 53}, {'fruit': 'Mango', 'hard': 1440, 'index': 54},
        {'fruit': 'Avocado', 'hard': 6000, 'index': 57}, {'fruit': 'Avocado', 'hard': 4320, 'index': 58},
        {'fruit': 'Avocado', 'hard': 1320, 'index': 59}, {'fruit': 'Orange', 'hard': 33820, 'index': 60},
        {'fruit': 'Orange', 'hard': 2400, 'index': 61}, {'fruit': 'Sweet Potato', 'hard': 5280, 'index': 62},
        {'fruit': 'Sweet Potato', 'hard': 6240, 'index': 63}, {'fruit': 'Sweet Potato', 'hard': 11760, 'index': 64},
        {'fruit': 'Sweet Potato', 'hard': 4320, 'index': 65}, {'fruit': 'Sweet Potato', 'hard': 1200, 'index': 66},
        {'fruit': 'Sweet Potato', 'hard': 8200, 'index': 67}, {'fruit': 'Sweet Potato', 'hard': 20, 'index': 68},
        {'fruit': 'Sweet Potato', 'hard': 4800, 'index': 69}, {'fruit': 'Sweet Potato', 'hard': 40, 'index': 70},
        {'fruit': 'Sweet Potato', 'hard': 2380, 'index': 71}, {'fruit': 'Sweet Potato', 'hard': 240, 'index': 72},
        {'fruit': 'Sweet Potato', 'hard': 7240, 'index': 73}, {'fruit': 'Sweet Potato', 'hard': 1400, 'index': 74},
        {'fruit': 'Grapefruit', 'hard': 2020, 'index': 75}, {'fruit': 'Cherry', 'hard': 17280, 'index': 76},
        {'fruit': 'Cherry', 'hard': 2880, 'index': 77}, {'fruit': 'Sweet Potato', 'hard': 2080, 'index': 78},
        {'fruit': 'Sweet Potato', 'hard': 1920, 'index': 79}
    ]

    group_info = [
        {"name": "a", "size": 17},
        {"name": "b", "size": 18},
        {"name": "c", "size": 20},
        {"name": "d", "size": 19}
    ]

    # 과일 종류별로 합친 후 큰 hard 값을 조정
    combined_rows = combine_fruits_with_index(rows)
    adjusted_rows = split_highest_hard(combined_rows, rows)

    # eta 계산 및 출력
    allocation, group_eta = heuristic_allocation(adjusted_rows, group_info)


if __name__ == "__main__":
    main()
