// Integrator.cpp (CORREGIDO - con include de cmath)
#include "Integrator.h"
#include "MotorModel.h"
#include <cmath>  // <--- ¡FALTABA ESTA INCLUSIÓN!
#include <iostream>

void StochasticVelocityVerletIntegrator::step(MotorModel& motor, double dt) {
    Particle& p = motor.getParticle();
    CargoParticle& cargo = motor.getCargoParticle();
    
    double m_motor = p.m;
    double m_cargo = cargo.m;
    double gamma = motor.getGamma();
    double kBT = motor.getKBT();
    
    // ======= DEBUG 1: Estado antes =======
    std::cout << "\n🔍 DEBUG INTEGRATOR - ANTES:" << std::endl;
    std::cout << "Motor: x=" << p.x << ", v=" << p.v << ", m=" << m_motor << std::endl;
    std::cout << "Cargo: x=" << cargo.x << ", v=" << cargo.v << ", m=" << m_cargo << std::endl;
    
    // --- Coeficientes ---
    double c1 = std::exp(-gamma * dt);  // ¡Ahora funciona con cmath!
    double sigma = std::sqrt(kBT * (1.0 - c1 * c1));  // ¡Ahora funciona con cmath!
    
    // ======= DEBUG 2: Fuerzas =======
    double F_motor = motor.motorForce();
    double F_spring = motor.springForce();
    double dx = p.x - cargo.x;
    
    std::cout << "Fuerzas: F_motor=" << F_motor << ", F_spring=" << F_spring;
    std::cout << ", dx=" << dx << std::endl;
    
    // ¡IMPORTANTE! Verifica estos signos:
    double F_motor_total = F_motor - F_spring;  // Motor: potencial - resorte
    double F_cargo_total = F_spring;            // Cargo: solo resorte
    
    std::cout << "F_total motor: " << F_motor_total;
    std::cout << ", F_total cargo: " << F_cargo_total << std::endl;
    
    // --- 1. Paso B (Force Half-Step) ---
    p.v += F_motor_total / m_motor * (0.5 * dt);
    cargo.v += F_cargo_total / m_cargo * (0.5 * dt);
    
    std::cout << "Después B1/2: v_motor=" << p.v << ", v_cargo=" << cargo.v << std::endl;
    
    // --- 2. Paso A (Friction & Noise) ---
    double R_motor = motor.generateGaussianNoise();
    double R_cargo = motor.generateGaussianNoise();  // Ruido independiente
    
    p.v = c1 * p.v + sigma * R_motor / std::sqrt(m_motor);  // ¡cmath incluido!
    cargo.v = c1 * cargo.v + sigma * R_cargo / std::sqrt(m_cargo);  // ¡cmath incluido!
    
    std::cout << "Después A: v_motor=" << p.v << ", v_cargo=" << cargo.v << std::endl;
    
    // --- 3. Paso O (Position Full-Step) ---
    p.x += p.v * dt;
    cargo.x += cargo.v * dt;
    
    std::cout << "Después O: x_motor=" << p.x << ", x_cargo=" << cargo.x << std::endl;
    
    // --- 4. Paso B (Force Half-Step) ---
    double F_motor_new = motor.motorForce();
    double F_spring_new = motor.springForce();
    
    double F_motor_total_new = F_motor_new - F_spring_new;
    double F_cargo_total_new = F_spring_new;
    
    p.v += F_motor_total_new / m_motor * (0.5 * dt);
    cargo.v += F_cargo_total_new / m_cargo * (0.5 * dt);
    
    // ======= DEBUG 3: Estado después =======
    std::cout << "🔍 DEBUG INTEGRATOR - DESPUÉS:" << std::endl;
    std::cout << "Motor: x=" << p.x << ", v=" << p.v << std::endl;
    std::cout << "Cargo: x=" << cargo.x << ", v=" << cargo.v << std::endl;
    std::cout << "==================================" << std::endl;
}