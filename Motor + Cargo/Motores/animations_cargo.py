# animations_cargo.py (MODIFICADO - TIEMPO REAL SIN SISTEMA FÍSICO)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import os
import sys
import time

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

def calculate_real_time_params(data_file):
    """Calcular parámetros para animación en tiempo real"""
    data = np.loadtxt(data_file)
    t = data[:, 0]
    
    # Duración total de la simulación
    sim_duration = t[-1] - t[0]
    total_points = len(t)
    
    print(f"📊 INFORMACIÓN DE LA SIMULACIÓN:")
    print(f"   Duración simulada: {sim_duration:.3f} segundos")
    print(f"   Puntos calculados: {total_points}")
    print(f"   Paso temporal (Δt): {t[1]-t[0]:.6f} s" if len(t) > 1 else "   Paso temporal: N/A")
    
    # Configurar para animación en tiempo real
    TARGET_FPS = 30  # Frames por segundo objetivo
    TARGET_DURATION = sim_duration  # ¡Misma duración que la simulación!
    
    # Calcular cuántos frames necesitamos para mostrar sim_duration segundos a TARGET_FPS
    target_frames = int(TARGET_FPS * TARGET_DURATION)
    
    # Si tenemos más puntos que frames objetivo, submuestrear
    if total_points > target_frames:
        n = max(1, total_points // target_frames)
        actual_frames = total_points // n
        print(f"   Submuestreo: 1 de cada {n} puntos")
    else:
        n = 1
        actual_frames = total_points
        # Si tenemos pocos puntos, reducir FPS para mantener duración
        TARGET_FPS = actual_frames / TARGET_DURATION if TARGET_DURATION > 0 else 30
        print(f"   Usando todos los puntos, FPS ajustado: {TARGET_FPS:.1f}")
    
    # Intervalo entre frames en milisegundos
    interval_ms = 1000 / TARGET_FPS if TARGET_FPS > 0 else 33
    
    print(f"\n🎯 CONFIGURACIÓN DE ANIMACIÓN (TIEMPO REAL):")
    print(f"   Duración objetivo: {TARGET_DURATION:.2f} s")
    print(f"   FPS objetivo: {TARGET_FPS:.1f}")
    print(f"   Frames en animación: {actual_frames}")
    print(f"   Intervalo entre frames: {interval_ms:.1f} ms")
    print(f"   Duración real estimada: {actual_frames * interval_ms/1000:.2f} s")
    
    return {
        'sim_duration': sim_duration,
        'total_points': total_points,
        'target_fps': TARGET_FPS,
        'target_duration': TARGET_DURATION,
        'n': n,
        'actual_frames': actual_frames,
        'interval_ms': interval_ms
    }

def animate_complete_realtime():
    """Animación completa EN TIEMPO REAL - SIN SISTEMA FÍSICO VISUAL"""
    print("🎬 PREPARANDO ANIMACIÓN COMPLETA EN TIEMPO REAL...")
    
    # Cargar datos
    data_file = find_data_file()
    if not data_file:
        return
    
    # Calcular parámetros de tiempo real
    params = calculate_real_time_params(data_file)
    
    # Cargar todos los datos
    data = np.loadtxt(data_file)
    t = data[:, 0]
    x_motor = data[:, 1]
    v_motor = data[:, 2]
    x_cargo = data[:, 3]
    v_cargo = data[:, 4]
    s = data[:, 5]
    
    # Submuestrear si es necesario
    n = params['n']
    if n > 1:
        t_sub = t[::n]
        x_motor_sub = x_motor[::n]
        v_motor_sub = v_motor[::n]
        x_cargo_sub = x_cargo[::n]
        v_cargo_sub = v_cargo[::n]
        s_sub = s[::n]
    else:
        t_sub = t
        x_motor_sub = x_motor
        v_motor_sub = v_motor
        x_cargo_sub = x_cargo
        v_cargo_sub = v_cargo
        s_sub = s
    
    actual_frames = len(t_sub)
    
    # Configurar la figura (ahora 2x2 en lugar de 2x3, sin sistema físico)
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Posiciones vs tiempo (arriba izquierda)
    ax1 = plt.subplot(2, 2, 1)
    ax1.set_xlim(np.min(t), np.max(t))
    ax1.set_ylim(min(np.min(x_motor), np.min(x_cargo)) - 0.1, 
                max(np.max(x_motor), np.max(x_cargo)) + 0.1)
    ax1.set_xlabel('Tiempo $t$ (s)', fontsize=12)
    ax1.set_ylabel('Posición $x$', fontsize=12)
    ax1.set_title(f'Posiciones vs Tiempo ({params["sim_duration"]:.1f}s simulación)', 
                 fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    motor_pos_line, = ax1.plot([], [], 'b-', linewidth=1.5, alpha=0.8, label='Motor')
    cargo_pos_line, = ax1.plot([], [], 'g-', linewidth=1.5, alpha=0.8, label='Cargo')
    motor_pos_point, = ax1.plot([], [], 'bo', markersize=8)
    cargo_pos_point, = ax1.plot([], [], 'go', markersize=8)
    time_vertical, = ax1.plot([], [], 'r--', alpha=0.5)
    ax1.legend(loc='upper right')
    
    # 2. Espacio de fase (arriba derecha)
    ax2 = plt.subplot(2, 2, 2)
    ax2.set_xlim(min(np.min(x_motor), np.min(x_cargo)) - 0.1, 
                max(np.max(x_motor), np.max(x_cargo)) + 0.1)
    ax2.set_ylim(min(np.min(v_motor), np.min(v_cargo)) - 0.1, 
                max(np.max(v_motor), np.max(v_cargo)) + 0.1)
    ax2.set_xlabel('Posición $x$', fontsize=12)
    ax2.set_ylabel('Velocidad $v$', fontsize=12)
    ax2.set_title('Espacio de Fase', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    phase_motor, = ax2.plot([], [], 'b-', linewidth=0.7, alpha=0.6, label='Motor')
    phase_cargo, = ax2.plot([], [], 'g-', linewidth=0.7, alpha=0.6, label='Cargo')
    phase_motor_point, = ax2.plot([], [], 'bo', markersize=8)
    phase_cargo_point, = ax2.plot([], [], 'go', markersize=8)
    ax2.legend(loc='upper right')
    
    # 3. Estado del motor y distancia (abajo izquierda)
    ax3 = plt.subplot(2, 2, 3)
    ax3.set_xlim(np.min(t), np.max(t))
    ax3.set_ylim(-0.1, 1.1)
    ax3.set_xlabel('Tiempo $t$ (s)', fontsize=12)
    ax3.set_ylabel('Estado $s$', fontsize=12)
    ax3.set_title('Estado del Motor', fontsize=14, fontweight='bold')
    ax3.set_yticks([0, 1])
    ax3.grid(True, alpha=0.3)
    
    state_line, = ax3.plot([], [], 'purple', drawstyle='steps-post', linewidth=2)
    state_point, = ax3.plot([], [], 'ro', markersize=8)
    
    # 4. Distancia motor-cargo (abajo derecha)
    ax4 = plt.subplot(2, 2, 4)
    distance = x_motor - x_cargo
    ax4.set_xlim(np.min(t), np.max(t))
    ax4.set_ylim(np.min(distance) - 0.1, np.max(distance) + 0.1)
    ax4.set_xlabel('Tiempo $t$ (s)', fontsize=12)
    ax4.set_ylabel('Distancia $x_m - x_c$', fontsize=12)
    ax4.set_title('Distancia Motor-Cargo', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    dist_line, = ax4.plot([], [], 'r-', linewidth=1.5, alpha=0.8)
    dist_point, = ax4.plot([], [], 'ro', markersize=8)
    
    # Texto informativo con tiempo (en la parte superior de la figura)
    info_text = fig.text(0.02, 0.98, '', fontsize=10,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Función de inicialización
    def init():
        motor_pos_line.set_data([], [])
        cargo_pos_line.set_data([], [])
        motor_pos_point.set_data([], [])
        cargo_pos_point.set_data([], [])
        time_vertical.set_data([], [])
        
        phase_motor.set_data([], [])
        phase_cargo.set_data([], [])
        phase_motor_point.set_data([], [])
        phase_cargo_point.set_data([], [])
        
        state_line.set_data([], [])
        state_point.set_data([], [])
        
        dist_line.set_data([], [])
        dist_point.set_data([], [])
        
        info_text.set_text(f'Tiempo: 0.00 / {params["sim_duration"]:.1f} s\nProgreso: 0%')
        
        return (motor_pos_line, cargo_pos_line, motor_pos_point, cargo_pos_point, time_vertical,
                phase_motor, phase_cargo, phase_motor_point, phase_cargo_point,
                state_line, state_point,
                dist_line, dist_point,
                info_text)
    
    # Función de animación
    def animate(i):
        idx = min(i, actual_frames - 1)
        
        # 1. Posiciones vs tiempo
        motor_pos_line.set_data(t_sub[:idx+1], x_motor_sub[:idx+1])
        cargo_pos_line.set_data(t_sub[:idx+1], x_cargo_sub[:idx+1])
        motor_pos_point.set_data([t_sub[idx]], [x_motor_sub[idx]])
        cargo_pos_point.set_data([t_sub[idx]], [x_cargo_sub[idx]])
        
        y_min, y_max = ax1.get_ylim()
        time_vertical.set_data([t_sub[idx], t_sub[idx]], [y_min, y_max])
        
        # 2. Espacio de fase
        phase_motor.set_data(x_motor_sub[:idx+1], v_motor_sub[:idx+1])
        phase_cargo.set_data(x_cargo_sub[:idx+1], v_cargo_sub[:idx+1])
        phase_motor_point.set_data([x_motor_sub[idx]], [v_motor_sub[idx]])
        phase_cargo_point.set_data([x_cargo_sub[idx]], [v_cargo_sub[idx]])
        
        # 3. Estado
        state_line.set_data(t_sub[:idx+1], s_sub[:idx+1])
        state_point.set_data([t_sub[idx]], [s_sub[idx]])
        
        # 4. Distancia
        current_dist = x_motor_sub[idx] - x_cargo_sub[idx]
        dist_line.set_data(t_sub[:idx+1], x_motor_sub[:idx+1] - x_cargo_sub[:idx+1])
        dist_point.set_data([t_sub[idx]], [current_dist])
        
        # 5. Información
        current_time = t_sub[idx]
        progress_percent = (idx + 1) / actual_frames * 100
        state_name = "DÉBIL" if s_sub[idx] == 0 else "FUERTE"
        
        info_text.set_text(
            f'Tiempo: {current_time:.2f} / {params["sim_duration"]:.1f} s\n'
            f'Progreso: {progress_percent:.0f}%\n'
            f'Motor: x={x_motor_sub[idx]:.3f}, v={v_motor_sub[idx]:.3f}\n'
            f'Cargo: x={x_cargo_sub[idx]:.3f}, v={v_cargo_sub[idx]:.3f}\n'
            f'Distancia: {current_dist:.3f}\n'
            f'Estado: {state_name}'
        )
        
        return (motor_pos_line, cargo_pos_line, motor_pos_point, cargo_pos_point, time_vertical,
                phase_motor, phase_cargo, phase_motor_point, phase_cargo_point,
                state_line, state_point,
                dist_line, dist_point,
                info_text)
    
    # Crear animación CON INTERVALO CALCULADO PARA TIEMPO REAL
    print(f"\n⏳ Creando animación de {params['sim_duration']:.2f} segundos...")
    print(f"   Frames: {actual_frames}, Intervalo: {params['interval_ms']:.1f}ms")
    
    anim = FuncAnimation(fig, animate, init_func=init,
                        frames=actual_frames, 
                        interval=params['interval_ms'],
                        blit=False,
                        repeat=False)
    
    # Guardar animación
    os.makedirs("results/animations", exist_ok=True)
    output_file = f"results/animations/completa_{params['sim_duration']:.0f}s_realtime.mp4"
    
    print(f"💾 Guardando: {output_file}")
    print("⏳ Esto puede tardar varios minutos...")
    
    start_time = time.time()
    
    try:
        # Configurar writer con FPS calculado
        fps = 1000 / params['interval_ms']
        writer = animation.FFMpegWriter(
            fps=fps,
            metadata={
                'title': f'Motor-Cargo {params["sim_duration"]:.1f}s',
                'artist': 'Simulación Física',
                'comment': f'Duración real: {params["sim_duration"]:.3f}s'
            },
            extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22']
        )
        
        anim.save(output_file, writer=writer, dpi=150)
        
        end_time = time.time()
        save_time = end_time - start_time
        
        print(f"✅ Animación guardada en {save_time:.1f} segundos")
        print(f"📊 Especificaciones:")
        print(f"   - Duración video: {params['sim_duration']:.2f} s")
        print(f"   - FPS: {fps:.1f}")
        print(f"   - Frames: {actual_frames}")
        
    except Exception as e:
        print(f"❌ Error guardando MP4: {e}")
        print("🔄 Intentando GIF...")
        
        try:
            output_gif = f"results/animations/completa_{params['sim_duration']:.0f}s_realtime.gif"
            
            # Reducir frames para GIF
            gif_frames = min(200, actual_frames)
            gif_fps = min(15, params['target_fps'])
            
            anim_gif = FuncAnimation(fig, animate, init_func=init,
                                    frames=gif_frames,
                                    interval=1000/gif_fps,
                                    blit=False, repeat=False)
            
            anim_gif.save(output_gif, writer='pillow', fps=gif_fps, dpi=100)
            
            print(f"✅ GIF guardado: {output_gif}")
            
        except Exception as e2:
            print(f"❌ Error guardando GIF: {e2}")
            print("💡 Mostrando animación en pantalla...")
            plt.show()
    
    plt.close()
    
    print(f"\n🎬 ¡ANIMACIÓN COMPLETA EN TIEMPO REAL COMPLETADA!")
    return output_file

def animate_simple_realtime():
    """Animación simple en tiempo real CON SISTEMA FÍSICO (como la pediste)"""
    print("🎬 PREPARANDO ANIMACIÓN SIMPLE EN TIEMPO REAL...")
    
    data_file = find_data_file()
    if not data_file:
        return
    
    params = calculate_real_time_params(data_file)
    
    data = np.loadtxt(data_file)
    t = data[:, 0]
    x_motor = data[:, 1]
    x_cargo = data[:, 3]
    s = data[:, 5]
    
    # Submuestrear
    n = params['n']
    if n > 1:
        t_sub = t[::n]
        x_motor_sub = x_motor[::n]
        x_cargo_sub = x_cargo[::n]
        s_sub = s[::n]
    else:
        t_sub = t
        x_motor_sub = x_motor
        x_cargo_sub = x_cargo
        s_sub = s
    
    actual_frames = len(t_sub)
    
    # Figura simple CON SISTEMA FÍSICO (2 gráficos)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Sistema físico (motor y cargo con resorte) - SOLO EN LA SIMPLE
    ax1.set_xlim(min(np.min(x_motor), np.min(x_cargo)) - 0.5,
                max(np.max(x_motor), np.max(x_cargo)) + 0.5)
    ax1.set_ylim(-0.3, 0.3)
    ax1.set_aspect('equal')
    ax1.set_title(f'Sistema Motor-Cargo ({params["sim_duration"]:.1f}s)', 
                 fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    motor = plt.Circle((0, 0), 0.1, color='blue', alpha=0.8)
    cargo = plt.Circle((0, 0), 0.08, color='green', alpha=0.8)
    spring, = ax1.plot([], [], 'k-', linewidth=2, alpha=0.7)
    
    ax1.add_patch(motor)
    ax1.add_patch(cargo)
    
    # Gráfica temporal
    ax2.set_xlim(np.min(t), np.max(t))
    ax2.set_ylim(min(np.min(x_motor), np.min(x_cargo)) - 0.2, 
                max(np.max(x_motor), np.max(x_cargo)) + 0.2)
    ax2.set_xlabel('Tiempo (s)', fontsize=12)
    ax2.set_ylabel('Posición', fontsize=12)
    ax2.set_title('Evolución Temporal', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    motor_line, = ax2.plot([], [], 'b-', label='Motor', linewidth=2)
    cargo_line, = ax2.plot([], [], 'g-', label='Cargo', linewidth=2)
    motor_point, = ax2.plot([], [], 'bo', markersize=8)
    cargo_point, = ax2.plot([], [], 'go', markersize=8)
    ax2.legend(loc='upper right')
    
    # Información
    info_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=10,
                        verticalalignment='top', 
                        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    def init():
        motor.center = (0, 0)
        cargo.center = (0, 0)
        spring.set_data([], [])
        motor_line.set_data([], [])
        cargo_line.set_data([], [])
        motor_point.set_data([], [])
        cargo_point.set_data([], [])
        info_text.set_text(f'Tiempo: 0.00 / {params["sim_duration"]:.1f} s\nProgreso: 0%')
        return motor, cargo, spring, motor_line, cargo_line, motor_point, cargo_point, info_text
    
    def animate(i):
        idx = min(i, actual_frames - 1)
        
        # Sistema físico
        motor_x = x_motor_sub[idx]
        cargo_x = x_cargo_sub[idx]
        
        motor.center = (motor_x, 0)
        cargo.center = (cargo_x, 0)
        spring.set_data([motor_x, cargo_x], [0, 0])
        
        # Gráfica temporal
        motor_line.set_data(t_sub[:idx+1], x_motor_sub[:idx+1])
        cargo_line.set_data(t_sub[:idx+1], x_cargo_sub[:idx+1])
        motor_point.set_data([t_sub[idx]], [x_motor_sub[idx]])
        cargo_point.set_data([t_sub[idx]], [x_cargo_sub[idx]])
        
        # Información
        current_time = t_sub[idx]
        progress = (idx + 1) / actual_frames * 100
        state = "DÉBIL" if s_sub[idx] == 0 else "FUERTE"
        dist = motor_x - cargo_x
        
        info_text.set_text(
            f'Tiempo: {current_time:.2f} / {params["sim_duration"]:.1f} s\n'
            f'Progreso: {progress:.0f}%\n'
            f'Motor: {motor_x:.3f}\n'
            f'Cargo: {cargo_x:.3f}\n'
            f'Dist: {dist:.3f}\n'
            f'Estado: {state}'
        )
        
        return motor, cargo, spring, motor_line, cargo_line, motor_point, cargo_point, info_text
    
    # Crear animación con intervalo calculado
    anim = FuncAnimation(fig, animate, init_func=init,
                        frames=actual_frames,
                        interval=params['interval_ms'],
                        blit=False, repeat=False)
    
    # Guardar
    os.makedirs("results/animations", exist_ok=True)
    output_file = f"results/animations/simple_{params['sim_duration']:.0f}s_realtime.gif"
    
    print("📹 Guardando animación simple...")
    
    try:
        anim.save(output_file, writer='pillow', 
                 fps=1000/params['interval_ms'] if params['interval_ms'] > 0 else 15,
                 dpi=100)
        print(f"✅ Animación simple guardada: {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")
        plt.show()
    
    plt.close()

def main():
    print("="*60)
    print("ANIMACIONES EN TIEMPO REAL - SISTEMA MOTOR-CARGO")
    print("="*60)
    
    # Verificar dependencias
    try:
        import matplotlib.animation as animation
    except ImportError:
        print("❌ matplotlib no tiene soporte para animaciones")
        return
    
    # Verificar datos
    data_file = find_data_file()
    if not data_file:
        print("\n💡 Ejecuta primero la simulación con cargo")
        return
    
    # Obtener duración de simulación
    data = np.loadtxt(data_file, max_rows=2)
    t = data[:, 0] if len(data.shape) > 1 else [0, 0]
    sim_duration = t[-1] - t[0] if len(t) > 1 else 0
    
    print(f"\n📊 Simulación de {sim_duration:.2f} segundos detectada")
    print("   La animación durará aproximadamente lo mismo")
    
    # Argumentos
    auto_mode = len(sys.argv) > 1 and sys.argv[1] == "auto"
    
    if auto_mode:
        print("\n🚀 Modo automático: generando animaciones en tiempo real")
        animate_complete_realtime()  # Renombrada sin sistema físico
        animate_simple_realtime()    # Mantiene sistema físico
        print("✅ Animaciones en tiempo real completadas")
    else:
        while True:
            print("\n🎬 ¿Qué animación en tiempo real quieres generar?")
            print(f"1. Animación completa SIN sistema físico ({sim_duration:.1f}s)")
            print(f"2. Animación simple CON sistema físico ({sim_duration:.1f}s)")
            print("3. Ambas animaciones")
            print("4. Ver duración de simulación")
            print("5. Salir")
            
            choice = input("\nSelecciona (1-5): ").strip()
            
            if choice == '1':
                animate_complete_realtime()  # Renombrada
            elif choice == '2':
                animate_simple_realtime()
            elif choice == '3':
                animate_complete_realtime()
                animate_simple_realtime()
            elif choice == '4':
                params = calculate_real_time_params(data_file)
                print(f"\n⏱️  Duración: {params['sim_duration']:.3f} segundos")
                print(f"📈 Puntos: {params['total_points']}")
                print(f"🎬 Animación: {params['actual_frames']} frames @ {params['target_fps']:.1f} FPS")
            elif choice == '5':
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")
            
            if not auto_mode:
                continuar = input("\n¿Otra animación? (s/n): ").strip().lower()
                if continuar != 's':
                    break
    
    print(f"\n🎬 Animaciones guardadas en: results/animations/")
    print("💡 Nota: La animación dura aproximadamente lo mismo que la simulación")

if __name__ == "__main__":
    main()