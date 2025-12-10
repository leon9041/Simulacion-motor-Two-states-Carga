# debug_cargo.py
import numpy as np
import matplotlib.pyplot as plt

print("🔍 DIAGNÓSTICO DETALLADO DEL CARGO")
print("="*50)

# Cargar datos
data = np.loadtxt("results/datos_motor_con_cargo.txt")
t = data[:, 0]
x_motor = data[:, 1]
v_motor = data[:, 2]
x_cargo = data[:, 3]
v_cargo = data[:, 4]
s = data[:, 5]

# 1. Análisis de tendencias
print("\n1. TENDENCIA DEL CARGO:")
trend = np.polyfit(t, x_cargo, 1)
print(f"   Tendencia lineal: {trend[0]:.6f}x + {trend[1]:.6f}")
print(f"   Pendiente: {trend[0]:.6f} (debe ser ~0)")

if abs(trend[0]) > 0.001:
    print(f"   ⚠️  ¡CARGO TIENDE A {'IZQUIERDA' if trend[0] < 0 else 'DERECHA'}!")
else:
    print("   ✅ Cargo oscila sin tendencia")

# 2. Posiciones medias
print("\n2. POSICIONES MEDIAS:")
print(f"   Motor: media={np.mean(x_motor):.4f}, std={np.std(x_motor):.4f}")
print(f"   Cargo: media={np.mean(x_cargo):.4f}, std={np.std(x_cargo):.4f}")

# 3. Correlación motor-cargo
print("\n3. CORRELACIÓN MOTOR-CARGO:")
corr = np.corrcoef(x_motor, x_cargo)[0, 1]
print(f"   Correlación: {corr:.4f}")
if corr > 0.7:
    print("   ✅ Cargo sigue al motor")
elif corr < -0.7:
    print("   ⚠️  Cargo se mueve opuesto al motor")
else:
    print("   ⚠️  Poca correlación")

# 4. Energías
print("\n4. ENERGÍAS (últimas columnas):")
print(f"   Columnas en archivo: {data.shape[1]}")
if data.shape[1] > 10:
    E_spring = data[:, 9]  # Energía del resorte
    print(f"   Energía media del resorte: {np.mean(E_spring):.6f}")
    print(f"   Energía max del resorte: {np.max(E_spring):.6f}")

# 5. Gráficas detalladas
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

# 5.1 Posiciones
ax = axes[0, 0]
ax.plot(t, x_motor, 'b-', alpha=0.7, label='Motor')
ax.plot(t, x_cargo, 'r-', alpha=0.7, label='Cargo')
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Posición')
ax.set_title('POSICIONES - ¿Cargo sigue al motor?')
ax.legend()
ax.grid(True, alpha=0.3)

# 5.2 Distancia motor-cargo
ax = axes[0, 1]
distancia = x_motor - x_cargo
ax.plot(t, distancia, 'g-')
ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Distancia Motor-Cargo')
ax.set_title('ESTIRAMIENTO DEL RESORTE')
ax.grid(True, alpha=0.3)

# 5.3 Velocidades
ax = axes[1, 0]
ax.plot(t, v_motor, 'b-', alpha=0.5, label='v_motor')
ax.plot(t, v_cargo, 'r-', alpha=0.5, label='v_cargo')
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Velocidad')
ax.set_title('VELOCIDADES')
ax.legend()
ax.grid(True, alpha=0.3)

# 5.4 Espacio de fase motor
ax = axes[1, 1]
ax.plot(x_motor, v_motor, 'b-', alpha=0.5)
ax.set_xlabel('x_motor')
ax.set_ylabel('v_motor')
ax.set_title('ESPACIO FASE - MOTOR')
ax.grid(True, alpha=0.3)

# 5.5 Espacio de fase cargo
ax = axes[2, 0]
ax.plot(x_cargo, v_cargo, 'r-', alpha=0.5)
ax.set_xlabel('x_cargo')
ax.set_ylabel('v_cargo')
ax.set_title('ESPACIO FASE - CARGO')
ax.grid(True, alpha=0.3)

# 5.6 Histograma de posiciones
ax = axes[2, 1]
ax.hist(x_motor, bins=50, alpha=0.5, color='blue', density=True, label='Motor')
ax.hist(x_cargo, bins=50, alpha=0.5, color='red', density=True, label='Cargo')
ax.set_xlabel('Posición')
ax.set_ylabel('Densidad')
ax.set_title('DISTRIBUCIÓN DE POSICIONES')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/diagnostico_detallado_cargo.png', dpi=150)
plt.show()

# 6. Análisis de Fourier (¿qué frecuencias?)
print("\n5. ANÁLISIS DE FRECUENCIAS:")
# Calcular FFT rápida
from scipy.fft import fft, fftfreq

N = len(t)
dt_sim = t[1] - t[0]
freqs = fftfreq(N, dt_sim)[:N//2]

# FFT del motor
fft_motor = np.abs(fft(x_motor - np.mean(x_motor)))[:N//2]
freq_motor = freqs[np.argmax(fft_motor[1:]) + 1]  # Ignorar DC

# FFT del cargo
fft_cargo = np.abs(fft(x_cargo - np.mean(x_cargo)))[:N//2]
freq_cargo = freqs[np.argmax(fft_cargo[1:]) + 1]

print(f"   Frecuencia dominante motor: {freq_motor:.3f} Hz")
print(f"   Frecuencia dominante cargo: {freq_cargo:.3f} Hz")

# Frecuencia esperada del resorte
# f = (1/2π) * sqrt(k/m_efectiva)
print("\n" + "="*50)
print("CONCLUSIÓN:")
if abs(trend[0]) > 0.01:
    print("❌ PROBLEMA: Cargo tiene tendencia clara (bug probable)")
    print("💡 Revisa: L0=0, condiciones iniciales, fuerzas en el código")
elif corr > 0.5:
    print("✅ Cargo sigue al motor (comportamiento esperado)")
else:
    print("⚠️  Comportamiento extraño, revisar implementación")