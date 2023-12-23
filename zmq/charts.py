import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из файла .dat
file_path = 'subscriber_logs.dat'
data = []

with open(file_path, 'r') as file:
    for line in file:
        data.append(line.strip())

# Разбор данных и создание списков значений для каждого типа сообщений
dates = []
values_t = []
values_m = []
values_p = []

for entry in data:
    date_str, message = entry.split('] Message: ')
    date = pd.to_datetime(date_str[1:], format='%Y-%m-%d %H:%M:%S')
    dates.append(date)

    if message.startswith('t'):
        values_t.append(1)
    else:
        values_t.append(0)

    if message.startswith('m'):
        values_m.append(1)
    else:
        values_m.append(0)

    if message.startswith('p'):
        p_value = int(message.split()[1])
        values_p.append(p_value)
    else:
        values_p.append(0)

# Построение графиков
plt.figure(figsize=(15, 8))

# График для Message: t
plt.subplot(3, 1, 1)
plt.plot(dates, values_t, marker='o', color='blue')
plt.title('График для Message: t')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.grid(True)

# График для Message: m
plt.subplot(3, 1, 2)
plt.plot(dates, values_m, marker='o', color='green')
plt.title('График для Message: m')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.grid(True)

# График для Message: p
plt.subplot(3, 1, 3)
plt.plot(dates, values_p, marker='o', color='red')
plt.title('График для Message: p')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.grid(True)

plt.tight_layout()
plt.show()
