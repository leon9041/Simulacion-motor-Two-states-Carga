// Simulator.cpp (MODIFICADO)
#include "Simulator.h"
#include "MotorModel.h"
#include "Integrator.h"
#include <stdexcept>
#include <cmath>

Simulator::Simulator(MotorModel& m, Integrator& i, double T_t, double delta_t, const std::string& filename)
    : motor(m), integrator(i), T_total(T_t), dt(delta_t)
{
    system("mkdir -p results");
    data_file.open(filename);
    if (!data_file.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo de salida para la simulación.");
    }
    // NUEVO ENCABEZADO CON CARGO
    data_file << "# t\tx_motor\tv_motor\tx_cargo\tv_cargo\ts\tE_motor_kin\tE_cargo_kin\tE_pot_motor\tE_spring\tE_total\n";
}

void Simulator::logData(double t) {
    Particle& p = motor.getParticle();
    CargoParticle& cargo = motor.getCargoParticle();
    int s = motor.getCurrentState();
    
    double E_motor_kin = p.getKineticEnergy();
    double E_cargo_kin = cargo.getKineticEnergy();
    double E_pot_motor = motor.getPotentialEnergy();
    double E_spring = motor.getSpringEnergy();
    
    double E_total = E_motor_kin + E_cargo_kin + E_pot_motor + E_spring;
    
    data_file << t << "\t" 
              << p.x << "\t" << p.v << "\t"
              << cargo.x << "\t" << cargo.v << "\t"
              << s << "\t"
              << E_motor_kin << "\t" << E_cargo_kin << "\t"
              << E_pot_motor << "\t" << E_spring << "\t"
              << E_total << "\n";
}

void Simulator::run() {
    double t = 0.0;
    while (t < T_total) {
        motor.updateChemicalState(t, dt);
        logData(t);
        integrator.step(motor, dt);
        t += dt;
    }
    data_file.close();
}