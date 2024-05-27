import numpy as np
import matplotlib.pyplot as plt

# Параметры модели
alpha = 0.2470
beta = 0.8847

# Функция линейной регрессии для пульса на выдохе
def heart_rate(x):
    return beta + alpha * x

# Функция эластичности для предсердий
def e_a(t, RR, t_ar, T_ar, t_ac, T_ac):
    if 0 <= t <= t_ar + T_ar - RR:
        return 0.5 * (1 + np.cos(np.pi * (t + RR - t_ar) / T_ar))
    elif t_ar + T_ar - RR < t <= t_ac:
        return 0
    elif t_ac < t <= t_ac + T_ac:
        return 0.5 * (1 - np.cos(np.pi * (t - t_ac) / T_ac))
    else:
        return 0.5 * (1 + np.cos(np.pi * (t - t_ar) / T_ar))

# Функция эластичности для желудочков
def e_v(t, T_vc, T_vr):
    if 0 <= t <= T_vc:
        return 0.5 * (1 - np.cos(np.pi * t / T_vc))
    elif T_vc < t <= T_vc + T_vr:
        return 0.5 * (1 + np.cos(np.pi * (t - T_vc) / T_vr))
    else:
        return 0

# Модель давления в сердечных камерах
def heart_chamber_pressure(t, V_ch, V_0_ch, HR):
    RR = 60 / HR
    E_ch = e_a(t, RR, 0.1, 0.3, 0.4, 0.2) + e_v(t, 0.2, 0.3)
    return E_ch * (V_ch - V_0_ch)

# Интеграция модели
def integrate_model(V_ch, V_0_ch, x_values):
    pressures = []
    for x in x_values:
        HR = heart_rate(x)
        RR = 60 / HR
        t_values = np.linspace(0, RR, 100)
        pressures_t = [heart_chamber_pressure(t, V_ch, V_0_ch, HR) for t in t_values]
        pressures.append(pressures_t)
    return pressures

# Параметры
V_ch = 140  # объем камеры
V_0_ch = 70  # ненапряженный объем камеры
x_values = np.linspace(1, 10, 10)  # пример значений длительности выдоха

# Интеграция модели
pressures = integrate_model(V_ch, V_0_ch, x_values)

# Визуализация результатов
plt.figure(figsize=(10, 6))
for i, pressure in enumerate(pressures):
    plt.plot(np.linspace(0, 60 / heart_rate(x_values[i]), 100), pressure, label=f"x = {x_values[i]:.2f}")

plt.title("Давление в сердечных камерах при различных значениях длительности выдоха")
plt.xlabel("Время (с)")
plt.ylabel("Давление (Па)")
plt.legend()
plt.show()