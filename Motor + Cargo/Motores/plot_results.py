# plot_results_cargo.py (NUEVO - PARA CARGO)
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def find_data_file():
    """Buscar el archivo de datos con cargo"""
    possible_paths = [
        "results/datos_motor_con_cargo.txt",
        "../results/datos_motor_con_cargo.txt",
        "./results/datos_motor_con_cargo.txt",
        "datos_motor_con_cargo.txt"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Archivo de datos encontrado: {path}")
            return path
    
    print("❌ No se pudo encontrar el archivo de datos con cargo.")
    return None

def plot_schematic_model_with_cargo():
    """Crear gráfica esquemática del modelo con partícula pasiva"""
    print("Generando gráfica esquemática del modelo con partícula pasiva...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # --- Panel izquierdo: Modelo sin cargo ---
    x = np.linspace(-0.5, 1.5, 1000)
    k0, k1 = 0.1, 10.0
    x0, x1 = 0.0, 0.5
    
    U0 = 0.5 * k0 * (x - x0)**2
    U1 = 0.5 * k1 * (x - x1)**2
    
    ax1.plot(x, U0, 'b-', linewidth=3, label='$U_0(x)$', alpha=0.8)
    ax1.plot(x, U1, 'r-', linewidth=3, label='$U_1(x)$', alpha=0.8)
    
    # Motor como círculo
    motor_x = 0.25
    motor_y = min(0.5 * k0 * motor_x**2, 0.5 * k1 * (motor_x - x1)**2)
    ax1.plot(motor_x, motor_y, 'ko', markersize=12, label='Motor')
    
    ax1.axvline(x=x0, color='blue', linestyle='--', alpha=0.5)
    ax1.axvline(x=x1, color='red', linestyle='--', alpha=0.5)
    
    ax1.set_xlabel('Posición $x$', fontsize=12)
    ax1.set_ylabel('Energía Potencial $U(x)$', fontsize=12)
    ax1.set_title('Modelo Original (Sin Cargo)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # --- Panel derecho: Modelo con cargo ---
    ax2.plot(x, U0, 'b-', linewidth=3, alpha=0.5)
    ax2.plot(x, U1, 'r-', linewidth=3, alpha=0.5)
    
    # Motor y cargo
    cargo_x = 0.0
    motor_y = 0.5 * k0 * motor_x**2
    cargo_y = 0.5 * k0 * cargo_x**2
    
    ax2.plot(motor_x, motor_y, 'ko', markersize=12, label='Motor')
    ax2.plot(cargo_x, cargo_y, 'go', markersize=12, label='Partícula Pasiva (Cargo)')
    
    # Resorte entre ellos
    spring_x = np.linspace(cargo_x, motor_x, 20)
    spring_y = np.interp(spring_x, [cargo_x, motor_x], [cargo_y, motor_y])
    ax2.plot(spring_x, spring_y, 'k--', linewidth=2, alpha=0.7, label='Resorte')
    
    ax2.axvline(x=x0, color='blue', linestyle='--', alpha=0.5)
    ax2.axvline(x=x1, color='red', linestyle='--', alpha=0.5)
    
    ax2.set_xlabel('Posición $x$', fontsize=12)
    ax2.set_ylabel('Energía Potencial $U(x)$', fontsize=12)
    ax2.set_title('Modelo con Partícula Pasiva', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '00_esquema_modelo_con_cargo.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ Gráfica esquemática con cargo generada")

def plot_cargo_trajectories(data):
    """Gráficas específicas para el modelo con cargo"""
    print("Generando gráficas con cargo...")
    
    # Columnas: t, x_motor, v_motor, x_cargo, v_cargo, s, E_motor_kin, E_cargo_kin, E_pot_motor, E_spring, E_total
    t = data[:, 0]
    x_motor = data[:, 1]
    v_motor = data[:, 2]
    x_cargo = data[:, 3]
    v_cargo = data[:, 4]
    s = data[:, 5]
    E_motor_kin = data[:, 6]
    E_cargo_kin = data[:, 7]
    E_pot_motor = data[:, 8]
    E_spring = data[:, 9]
    E_total = data[:, 10]
    
    # 1. Posiciones del motor y cargo vs tiempo
    plt.figure(figsize=(14, 8))
    
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(t, x_motor, 'b-', linewidth=1.5, label='Motor', alpha=0.8)
    ax1.plot(t, x_cargo, 'g-', linewidth=1.5, label='Cargo', alpha=0.8)
    ax1.set_ylabel('Posición ($x$)', fontsize=12)
    ax1.set_title('Posiciones del Motor y Cargo vs Tiempo', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.plot(t, x_motor - x_cargo, 'r-', linewidth=1.5, label='Distancia Motor-Cargo', alpha=0.8)
    ax2.set_ylabel('Distancia ($x_m - x_c$)', fontsize=12)
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    plt.setp(ax2.get_xticklabels(), visible=False)
    
    ax3 = plt.subplot(3, 1, 3, sharex=ax1)
    ax3.plot(t, s, drawstyle='steps-post', color='purple', linewidth=2, label='Estado Motor')
    ax3.set_xlabel('Tiempo ($t$)', fontsize=12)
    ax3.set_ylabel('Estado ($s$)', fontsize=12)
    ax3.set_yticks([0, 1])
    ax3.set_ylim(-0.1, 1.1)
    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '01_posiciones_motor_cargo.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Velocidades del motor y cargo
    plt.figure(figsize=(14, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(t, v_motor, 'b-', linewidth=1, alpha=0.7, label='Motor')
    plt.plot(t, v_cargo, 'g-', linewidth=1, alpha=0.7, label='Cargo')
    plt.xlabel('Tiempo ($t$)', fontsize=12)
    plt.ylabel('Velocidad ($v$)', fontsize=12)
    plt.title('Velocidades', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.hist(v_motor, bins=50, density=True, alpha=0.5, color='blue', label='Motor')
    plt.hist(v_cargo, bins=50, density=True, alpha=0.5, color='green', label='Cargo')
    plt.xlabel('Velocidad ($v$)', fontsize=12)
    plt.ylabel('Densidad de Probabilidad', fontsize=12)
    plt.title('Distribución de Velocidades', fontsize=13, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '02_velocidades_motor_cargo.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Energías
    plt.figure(figsize=(14, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(t, E_motor_kin, 'b-', alpha=0.7, label='K_motor')
    plt.plot(t, E_cargo_kin, 'g-', alpha=0.7, label='K_cargo')
    plt.plot(t, E_spring, 'r-', alpha=0.7, label='U_spring')
    plt.plot(t, E_pot_motor, 'm-', alpha=0.7, label='U_motor')
    plt.ylabel('Energía', fontsize=12)
    plt.title('Componentes de Energía', fontsize=13, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(3, 1, 2)
    E_kin_total = E_motor_kin + E_cargo_kin
    E_pot_total = E_pot_motor + E_spring
    plt.plot(t, E_kin_total, 'c-', label='K_total')
    plt.plot(t, E_pot_total, 'y-', label='U_total')
    plt.ylabel('Energía', fontsize=12)
    plt.title('Energía Cinética y Potencial Totales', fontsize=13, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(3, 1, 3)
    plt.plot(t, E_total, 'k-', linewidth=1.5, label='E_total')
    plt.xlabel('Tiempo ($t$)', fontsize=12)
    plt.ylabel('Energía Total', fontsize=12)
    plt.title('Energía Total del Sistema', fontsize=13, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '03_energias_sistema.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. Espacio de fase motor vs cargo
    plt.figure(figsize=(12, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(x_motor, v_motor, 'b-', linewidth=0.5, alpha=0.7)
    plt.xlabel('$x_{motor}$', fontsize=12)
    plt.ylabel('$v_{motor}$', fontsize=12)
    plt.title('Espacio de Fase: Motor', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.plot(x_cargo, v_cargo, 'g-', linewidth=0.5, alpha=0.7)
    plt.xlabel('$x_{cargo}$', fontsize=12)
    plt.ylabel('$v_{cargo}$', fontsize=12)
    plt.title('Espacio de Fase: Cargo', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.plot(x_motor, x_cargo, 'k-', linewidth=0.5, alpha=0.7)
    plt.xlabel('$x_{motor}$', fontsize=12)
    plt.ylabel('$x_{cargo}$', fontsize=12)
    plt.title('Correlación de Posiciones', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    plt.plot(v_motor, v_cargo, 'r-', linewidth=0.5, alpha=0.7)
    plt.xlabel('$v_{motor}$', fontsize=12)
    plt.ylabel('$v_{cargo}$', fontsize=12)
    plt.title('Correlación de Velocidades', fontsize=13, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, '04_espacios_fase.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. Estadísticas finales
    print("\n📊 Estadísticas del sistema:")
    print(f"   Motor - Posición media: {np.mean(x_motor):.4f} ± {np.std(x_motor):.4f}")
    print(f"   Cargo - Posición media: {np.mean(x_cargo):.4f} ± {np.std(x_cargo):.4f}")
    print(f"   Distancia media: {np.mean(x_motor - x_cargo):.4f}")
    print(f"   Energía media total: {np.mean(E_total):.6f}")
    print(f"   Energía media resorte: {np.mean(E_spring):.6f}")

# Configuración
FIGURES_DIR = "results/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Configurar matplotlib para evitar problemas de backend
plt.switch_backend('Agg')

try:
    print("=== GENERANDOR DE GRÁFICAS PARA MOTOR CON CARGO ===")
    
    # Generar esquema
    plot_schematic_model_with_cargo()
    
    # Buscar datos
    DATA_FILE = find_data_file()
    
    if DATA_FILE:
        print(f"\n📁 Cargando datos de: {DATA_FILE}")
        data = np.loadtxt(DATA_FILE)
        
        print(f"📊 Datos cargados: {len(data)} puntos")
        print(f"📝 Columnas detectadas: {data.shape[1]}")
        
        if data.shape[1] >= 11:  # Verificar que tiene columnas de cargo
            plot_cargo_trajectories(data)
            print(f"\n✅ Todas las gráficas generadas en: {FIGURES_DIR}")
        else:
            print("❌ El archivo no tiene el formato esperado para cargo")
            print("💡 Verifica que sea la simulación con cargo")
    else:
        print("⚠️  No se encontraron datos de simulación")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()