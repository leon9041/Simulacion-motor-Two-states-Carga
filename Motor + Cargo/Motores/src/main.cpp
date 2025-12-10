// main.cpp (MODIFICADO)
#include "MotorModel.h"
#include "Integrator.h"
#include "Simulator.h"
#include <iostream>
#include <stdexcept>

int main() {
    std::cout << "Iniciando simulacion del Motor de Dos Estados CON PARTICULA PASIVA...\n";

    // --- PARAMETROS FISICOS ---
    // --- PARÁMETROS FÍSICOS ---
    double m = 0.5;           // Masa motor
    double cargo_mass = 3.0;  // Masa carga
    double k_spring = 1.0;    // Resorte moderado (¡AJUSTADO!)
    double L0 = 0.1;          // Longitud natural NO CERO (¡IMPORTANTE!)
    
    // Motor
    double k0 = 5.0;    // Estado 0
    double k1 = 5.0;   // Estado 1 (más rígido)
    double l = 1.0;     // Distancia entre mínimos
    
    // Tiempos de conmutación
    double T_off = 0.5;
    double T_on = 0.5;
    
    // Medio viscoso
    double gamma = 0.5;  // ¡REDUCIDO para ver movimiento!
    double kBT = 0.01;
    
    // Simulación
    double T_total = 5.0;
    double dt = 0.001;

    // --- CONDICIONES INICIALES ---
    double initial_x = 0.0; 
    double initial_v = 0.0;     
    double cargo_initial_x = L0;  // ¡Posición inicial separada por L0!
    double cargo_initial_v = 0.0;
    try {
        // Crear modelo con cargo
        MotorModel motor(m, k0, k1, l, T_off, T_on, gamma, kBT, 
                        k_spring, L0, cargo_mass,
                        initial_x, initial_v,
                        cargo_initial_x, cargo_initial_v);
        
        StochasticVelocityVerletIntegrator pv_integrator; 
        
        Simulator simulator(motor, pv_integrator, T_total, dt, 
                           "results/datos_motor_con_cargo.txt");
        simulator.run();
        
        std::cout << "Simulacion completada. Datos guardados en results/datos_motor_con_cargo.txt\n";
        
    } catch (const std::exception& e) {
        std::cerr << "Error en la simulacion: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Error desconocido durante la simulación." << std::endl;
        return 1;
    }

    return 0;
}