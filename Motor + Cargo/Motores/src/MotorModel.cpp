// MotorModel.cpp (MODIFICADO)
#include "MotorModel.h"
#include <random>
#include <iostream>

static std::random_device rd;
static std::mt19937 generator(rd());
static std::normal_distribution<> normal_dist(0.0, 1.0); 

// CONSTRUCTOR MODIFICADO
MotorModel::MotorModel(double mass, double k0, double k1, double l, double t_off, double t_on, 
                       double gamma_val, double kBT_val,
                       double k_spring_val, double L0_val, double cargo_mass,
                       double initial_x, double initial_v,
                       double cargo_initial_x, double cargo_initial_v)
    : p(mass, initial_x, initial_v), 
      cargo(cargo_mass, cargo_initial_x, cargo_initial_v),  // NUEVO
      chemicalState(t_off, t_on),
      U0(k0, 0.0),
      U1(k1, l),
      gamma(gamma_val), 
      kBT(kBT_val),
      k_spring(k_spring_val),  // NUEVO
      L0(L0_val)               // NUEVO
{
    currentPotential = &U0;
    std::cout << "Motor creado con partícula pasiva:" << std::endl;
    std::cout << "  - Estado 0: U0(k=" << k0 << ", x_min=0.0)" << std::endl;
    std::cout << "  - Estado 1: U1(k=" << k1 << ", x_min=" << l << ")" << std::endl;
    std::cout << "  - Resorte: k_spring=" << k_spring << ", L0=" << L0 << std::endl;
    std::cout << "  - Masa cargo: " << cargo_mass << std::endl;
}

// Fuerza del motor (solo del potencial)
double MotorModel::motorForce(double t) const {
    return currentPotential->F(p.x); 
}

// NUEVO: Fuerza del resorte
double MotorModel::springForce() const {
    double dx = p.x - cargo.x;
    double force = -k_spring * (dx - L0);
    
    // DEBUG: Imprimir fuerzas
    static int count = 0;
    if (count++ % 1000 == 0) {
        std::cout << "DEBUG SPRING: dx=" << dx 
                  << ", force=" << force 
                  << ", motor.x=" << p.x 
                  << ", cargo.x=" << cargo.x << std::endl;
    }
    
    return force;
}

void MotorModel::updateChemicalState(double t, double dt) {
    chemicalState.update(t, dt);
    if (chemicalState.getState() == 0) {
        currentPotential = &U0;
    } else {
        currentPotential = &U1;
    }
}

// Energía potencial del motor
double MotorModel::getPotentialEnergy() const {
    return currentPotential->U(p.x);
}

// NUEVO: Energía del resorte
double MotorModel::getSpringEnergy() const {
    double dx = p.x - cargo.x;
    return 0.5 * k_spring * (dx - L0) * (dx - L0);
}

double MotorModel::getGamma() const { return gamma; }
double MotorModel::getKBT() const { return kBT; }
double MotorModel::generateGaussianNoise() const {
    return normal_dist(generator);
}