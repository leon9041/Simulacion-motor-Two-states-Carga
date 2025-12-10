# run_animation_cargo.py (NUEVO - PARA CARGO)
import os
import sys

def main():
    print("=== EJECUTOR RÁPIDO DE ANIMACIONES CON CARGO ===")
    
    # Verificar scripts
    if not os.path.exists("animations_cargo.py"):
        print("❌ No se encuentra animations_cargo.py")
        print("💡 Asegúrate de que esté en el mismo directorio")
        return
    
    # Verificar datos
    data_file = "results/datos_motor_con_cargo.txt"
    if not os.path.exists(data_file):
        print(f"❌ No se encuentran datos: {data_file}")
        print("💡 Primero ejecuta la simulación con cargo:")
        print("   python build.py")
        
        # Verificar si existe simulación anterior
        old_data = "results/datos_motor_dos_estados_langevin.txt"
        if os.path.exists(old_data):
            print(f"\n⚠️  Se encontraron datos antiguos: {old_data}")
            print("💡 Ejecuta primero la compilación para generar datos con cargo")
        
        return
    
    print("✅ Datos con cargo encontrados")
    print("🚀 Ejecutando animaciones...")
    
    # Ejecutar con modo automático
    os.system(f'"{sys.executable}" animations_cargo.py auto')

if __name__ == "__main__":
    main()