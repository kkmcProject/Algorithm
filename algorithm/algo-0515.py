from mip import Model, xsum, BINARY, INTEGER, OptimizationStatus
import pandas as pd
import numpy as np

# 예제 데이터 생성
data = {
    '과일 종류': ['사과', '사과', '바나나', '바나나', '딸기', '딸기', '포도', '포도', '오렌지', '오렌지'],
    '작업 시간': [3, 2, 4, 5, 1, 2, 6, 3, 4, 1]
}
df = pd.DataFrame(data)

# 작업반 수
n_groups = 3
n_tasks = len(df)

# MIP 모델 생성
m = Model()

# 변수 생성
x = [[m.add_var(var_type=BINARY) for j in range(n_groups)] for i in range(n_tasks)]
z = [m.add_var(var_type=BINARY) for j in range(n_groups)]
workload = [m.add_var(var_type=INTEGER) for j in range(n_groups)]

# 목표 함수: 각 반의 과일 종류를 최소화
m.objective = xsum(z[j] for j in range(n_groups))

# 제약 조건: 각 작업은 한 작업반에만 할당
for i in range(n_tasks):
    m += xsum(x[i][j] for j in range(n_groups)) == 1

# 제약 조건: 각 작업반의 작업 시간 계산
for j in range(n_groups):
    m += workload[j] == xsum(df['작업 시간'][i] * x[i][j] for i in range(n_tasks))

# 제약 조건: 각 작업반의 작업 시간은 거의 동일해야 함
avg_workload = sum(df['작업 시간']) / n_groups
for j in range(n_groups):
    m += workload[j] <= avg_workload * 1.1
    m += workload[j] >= avg_workload * 0.9

# 제약 조건: 각 작업반의 과일 종류 수를 최소화
for j in range(n_groups):
    for fruit in df['과일 종류'].unique():
        m += z[j] >= xsum(x[i][j] for i in range(n_tasks) if df['과일 종류'][i] == fruit)

# 최적화 수행
status = m.optimize()

# 결과 출력
if status == OptimizationStatus.OPTIMAL:
    print('Optimal solution found:')
elif status == OptimizationStatus.FEASIBLE:
    print('Feasible solution found:')
else:
    print('No solution found')

for j in range(n_groups):
    print(f'작업반 {j + 1}:')
    assigned_tasks = [i for i in range(n_tasks) if x[i][j].x >= 0.99]
    print(f' - 할당된 작업: {assigned_tasks}')
    print(f' - 작업 시간: {workload[j].x}')
    assigned_fruits = set(df['과일 종류'][i] for i in assigned_tasks)
    print(f' - 할당된 과일 종류: {assigned_fruits}')
else:
    print('Solution could not be found')
