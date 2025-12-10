# build.py (MODIFICADO)
import os
import subprocess
import sys

def run_command(cmd, description):
    print(f"\n📍 {description}...")
    print(f"   Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error en {description}:")
            if result.stderr:
                print(result.stderr)
            return False
        else:
            print(f"✅ {description} completado")
            if result.stdout.strip():
                print(result.stdout)
            return True
    except Exception as e:
        print(f"❌ Excepción en {description}: {e}")
        return False

def main():
    print("=== CONSTRUCCIÓN COMPLETA DE MOTOR MOLECULAR CON PARTÍCULA PASIVA ===")
    print("Incluye: Compilación + Simulación + Gráficas + Animaciones\n")
    
    # Obtener el directorio actual
    current_dir = os.getcwd()
    print(f"Directorio actual: {current_dir}")
    
    # Crear directorios necesarios
    print("\n📁 Creando directorios...")
    os.makedirs("bin", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)
    os.makedirs("results/animations", exist_ok=True)
    print("✅ Directorios creados")
    
    # 1. COMPILAR C++ (CON CARGO)
    print("\n" + "="*50)
    print("🔧 ETAPA 1: COMPILACIÓN C++ CON CARGO")
    print("="*50)
    
    # Lista de archivos fuente
    source_files = [
        "src/main.cpp", "src/Potential.cpp", "src/ChemicalState.cpp",
        "src/MotorModel.cpp", "src/Integrator.cpp", "src/Simulator.cpp",
        "src/Particle.cpp"  # NUEVO: si existe, si no, integrar en otros
    ]
    
    # Filtrar archivos que existen
    existing_files = [f for f in source_files if os.path.exists(f)]
    
    compile_cmd = [
        "g++", "-o", "bin/motor_cargo_sim.exe", 
        "-Iinclude", "-std=c++11", "-O2"
    ] + existing_files
    
    if not run_command(compile_cmd, "Compilación C++ con cargo"):
        print("❌ Falla en compilación - deteniendo proceso")
        return
    
    # 2. EJECUTAR SIMULACIÓN CON CARGO
    print("\n" + "="*50)
    print("🚀 ETAPA 2: SIMULACIÓN C++ CON CARGO")
    print("="*50)
    
    sim_cmd = ["bin/motor_cargo_sim.exe"]
    
    if not run_command(sim_cmd, "Simulación C++ con cargo"):
        print("❌ Falla en simulación - deteniendo proceso")
        return
    
    # 3. VERIFICAR QUE SE GENERARON LOS DATOS
    print("\n" + "="*50)
    print("📊 ETAPA 3: VERIFICACIÓN DE DATOS")
    print("="*50)
    
    # Archivo de datos con cargo
    data_file = "results/datos_motor_con_cargo.txt"
    if not os.path.exists(data_file):
        print(f"❌ No se encontró el archivo de datos: {data_file}")
        print("Buscando archivos en results/:")
        if os.path.exists("results"):
            for item in os.listdir("results"):
                if item.endswith(".txt"):
                    print(f"   - {item}")
        return
    
    # Verificar tamaño del archivo
    file_size = os.path.getsize(data_file)
    print(f"✅ Archivo de datos verificado: {data_file}")
    print(f"📏 Tamaño del archivo: {file_size} bytes")
    
    # Verificar estructura del archivo
    with open(data_file, 'r') as f:
        first_line = f.readline().strip()
        second_line = f.readline().strip() if not f.readline().startswith('#') else f.readline()
    
    print(f"📝 Encabezado: {first_line[:80]}...")
    
    # 4. GENERAR GRÁFICAS CON CARGO
    print("\n" + "="*50)
    print("🎨 ETAPA 4: GENERACIÓN DE GRÁFICAS CON CARGO")
    print("="*50)
    
    # Verificar que existe plot_results.py modificado
    if not os.path.exists("plot_results_cargo.py"):
        print("⚠️  No se encuentra plot_results_cargo.py")
        print("💡 Usando plot_results.py existente (puede no funcionar bien)")
        plot_script = "plot_results.py"
    else:
        plot_script = "plot_results_cargo.py"
    
    print(f"✅ Script de gráficas: {plot_script}")
    
    # Ejecutar script de gráficas
    plot_cmd = [sys.executable, plot_script]
    
    print(f"🚀 Ejecutando script de gráficas...")
    success = run_command(plot_cmd, "Generación de gráficas con cargo")
    
    # 5. GENERAR ANIMACIONES CON CARGO
    print("\n" + "="*50)
    print("🎬 ETAPA 5: GENERACIÓN DE ANIMACIONES CON CARGO")
    print("="*50)
    
    # Verificar que existe animations.py modificado
    if not os.path.exists("animations_cargo.py"):
        print("⚠️  No se encuentra animations_cargo.py")
        print("💡 Usando animations.py existente (puede no funcionar bien)")
        anim_script = "animations.py"
    else:
        anim_script = "animations_cargo.py"
    
    print(f"✅ Script de animaciones: {anim_script}")
    
    # Ejecutar script de animaciones
    anim_cmd = [sys.executable, anim_script, "auto"]
    
    print(f"🚀 Ejecutando script de animaciones...")
    anim_success = run_command(anim_cmd, "Generación de animaciones con cargo")
    
    # 6. RESULTADO FINAL
    print("\n" + "="*50)
    print("📋 RESUMEN FINAL")
    print("="*50)
    
    if success or anim_success:
        print("🎉🎉🎉 PROCESO COMPLETADO EXITOSAMENTE 🎉🎉🎉")
        print("✅ Compilación C++ con cargo: ✓")
        print("✅ Simulación con cargo: ✓")
        print(f"📊 Datos generados: {data_file}")
        print(f"🖼️  Figuras: results/figures/")
        print(f"🎬 Animaciones: results/animations/")
        
        # Mostrar archivos generados
        print("\n📋 Archivos generados:")
        
        # Figuras
        figures_dir = "results/figures"
        if os.path.exists(figures_dir):
            figures = [f for f in os.listdir(figures_dir) if f.endswith('.png')]
            if figures:
                print("  📍 Figuras:")
                for fig in sorted(figures)[:5]:  # Mostrar solo primeras 5
                    print(f"     - {fig}")
                if len(figures) > 5:
                    print(f"     ... y {len(figures)-5} más")
        
        # Animaciones
        anim_dir = "results/animations"
        if os.path.exists(anim_dir):
            anims = [f for f in os.listdir(anim_dir) if f.endswith(('.mp4', '.gif'))]
            if anims:
                print("  🎬 Animaciones:")
                for anim in sorted(anims):
                    print(f"     - {anim}")
    else:
        print("⚠️  PROCESO PARCIALMENTE COMPLETO")
        print("\n💡 SOLUCIÓN: Ejecuta manualmente:")
        print(f"   python {plot_script}")
        print(f"   python {anim_script}")
    
    print("\n🚀 Para ejecutar solo animaciones:")
    print(f"   python run_animation_cargo.py")

if __name__ == "__main__":
    main()