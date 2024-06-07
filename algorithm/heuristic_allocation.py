import pandas as pd
from collections import defaultdict


def combine_fruits(rows):
    # 과일 종류별로 작업을 합침
    combined = defaultdict(int)
    for row in rows:
        fruit = row['fruit']
        combined[fruit] += row['hard']

    combined_rows = [{'fruit': fruit, 'hard': hard} for fruit, hard in combined.items()]
    return combined_rows


def adjust_large_hard_values(combined_rows, num_teams):
    # 과일 hard 값 중 상위 (팀 개수 // 2)개의 값을 찾아서 반으로 나눔
    df = pd.DataFrame(combined_rows)
    df = df.sort_values(by='hard', ascending=False).reset_index(drop=True)
    num_large_values = num_teams // 2

    for i in range(num_large_values):
        df.at[i, 'hard'] = df.at[i, 'hard'] / 2

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
        print(f"Group {group} eta: {eta}, fruits: {fruits}")

    return allocation, group_eta


def main():
    rows = [
        {'fruit': 'Kiwi', 'hard': 8200}, {'fruit': 'Kiwi', 'hard': 6600},
        {'fruit': 'Kiwi', 'hard': 2680}, {'fruit': 'Kiwi', 'hard': 2160},
        {'fruit': 'Kiwi', 'hard': 29120}, {'fruit': 'Kiwi', 'hard': 33600},
        {'fruit': 'Kiwi', 'hard': 2780}, {'fruit': 'Kiwi', 'hard': 12960},
        {'fruit': 'Kiwi', 'hard': 4420}, {'fruit': 'Kiwi', 'hard': 2400},
        {'fruit': 'Kiwi', 'hard': 44800}, {'fruit': 'Kiwi', 'hard': 1080},
        {'fruit': 'Kiwi', 'hard': 120}, {'fruit': 'Kiwi', 'hard': 60},
        {'fruit': 'Kiwi', 'hard': 340}, {'fruit': 'Kiwi', 'hard': 1380},
        {'fruit': 'Kiwi', 'hard': 3520}, {'fruit': 'Kiwi', 'hard': 480},
        {'fruit': 'Kiwi', 'hard': 1320}, {'fruit': 'Kiwi', 'hard': 640},
        {'fruit': 'Kiwi', 'hard': 800}, {'fruit': 'Kiwi', 'hard': 32640},
        {'fruit': 'Kiwi', 'hard': 39600}, {'fruit': 'Kiwi', 'hard': 600},
        {'fruit': 'Kiwi', 'hard': 2160}, {'fruit': 'Kiwi', 'hard': 800},
        {'fruit': 'Kiwi', 'hard': 1800}, {'fruit': 'Lime', 'hard': 1440},
        {'fruit': 'Lime', 'hard': 240}, {'fruit': 'Lime', 'hard': 3120},
        {'fruit': 'Lime', 'hard': 560}, {'fruit': 'Lime', 'hard': 720},
        {'fruit': 'Lime', 'hard': 300}, {'fruit': 'Lime', 'hard': 180},
        {'fruit': 'Kiwi', 'hard': 6360}, {'fruit': 'Kiwi', 'hard': 3480},
        {'fruit': 'Kiwi', 'hard': 2280}, {'fruit': 'Kiwi', 'hard': 480},
        {'fruit': 'Kiwi', 'hard': 160}, {'fruit': 'Kiwi', 'hard': 120},
        {'fruit': 'Kiwi', 'hard': 240}, {'fruit': 'Kiwi', 'hard': 5120},
        {'fruit': 'Kiwi', 'hard': 7920}, {'fruit': 'Lemon', 'hard': 8040},
        {'fruit': 'Mango', 'hard': 2080}, {'fruit': 'Mango', 'hard': 1200},
        {'fruit': 'Mango', 'hard': 7040}, {'fruit': 'Mango', 'hard': 800},
        {'fruit': 'Mango', 'hard': 1760}, {'fruit': 'Mango', 'hard': 2760},
        {'fruit': 'Mango', 'hard': 1320}, {'fruit': 'Mango', 'hard': 2700},
        {'fruit': 'Mango', 'hard': 3700}, {'fruit': 'Mango', 'hard': 1440},
        {'fruit': 'Avocado', 'hard': 6000}, {'fruit': 'Avocado', 'hard': 4320},
        {'fruit': 'Avocado', 'hard': 1320}, {'fruit': 'Orange', 'hard': 33820},
        {'fruit': 'Orange', 'hard': 2400}, {'fruit': 'Sweet Potato', 'hard': 5280},
        {'fruit': 'Sweet Potato', 'hard': 6240}, {'fruit': 'Sweet Potato', 'hard': 11760},
        {'fruit': 'Sweet Potato', 'hard': 4320}, {'fruit': 'Sweet Potato', 'hard': 1200},
        {'fruit': 'Sweet Potato', 'hard': 8200}, {'fruit': 'Sweet Potato', 'hard': 20},
        {'fruit': 'Sweet Potato', 'hard': 4800}, {'fruit': 'Sweet Potato', 'hard': 40},
        {'fruit': 'Sweet Potato', 'hard': 2380}, {'fruit': 'Sweet Potato', 'hard': 240},
        {'fruit': 'Sweet Potato', 'hard': 7240}, {'fruit': 'Sweet Potato', 'hard': 1400},
        {'fruit': 'Grapefruit', 'hard': 2020}, {'fruit': 'Cherry', 'hard': 17280},
        {'fruit': 'Cherry', 'hard': 2880}, {'fruit': 'Sweet Potato', 'hard': 2080},
        {'fruit': 'Sweet Potato', 'hard': 1920}
    ]

    group_info = [
        {"name": "a", "size": 17},
        {"name": "b", "size": 18},
        {"name": "c", "size": 20},
        {"name": "d", "size": 19}
    ]

    # 과일 종류별로 합친 후 큰 hard 값을 조정
    combined_rows = combine_fruits(rows)
    adjusted_rows = adjust_large_hard_values(combined_rows, len(group_info))

    # eta 계산 및 출력
    allocation, group_eta = heuristic_allocation(adjusted_rows, group_info)


if __name__ == "__main__":
    main()