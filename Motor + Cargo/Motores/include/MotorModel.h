// MotorModel.h (MODIFICADO)
#ifndef MOTORMODEL_H
#define MOTORMODEL_H

#include "Particle.h"
#include "Potential.h"
#include "ChemicalState.h"

class MotorModel {
private:
    Particle p;                  // Partícula del motor
    CargoParticle cargo;         // Partícula pasiva (NUEVA)
    Potential* currentPotential;
    ChemicalState chemicalState;
    HarmonicPotential U0;
    HarmonicPotential U1;
    double gamma, kBT;
    double k_spring;            // Constante del resorte (NUEVA)
    double L0;                  // Longitud natural del resorte (NUEVA)

public:
    // Constructor modificado para incluir parámetros del cargo
    MotorModel(double mass, double k0, double k1, double l, double t_off, double t_on, 
               double gamma_val, double kBT_val, 
               double k_spring_val, double L0_val, double cargo_mass,  // NUEVOS PARÁMETROS
               double initial_x = 0.0, double initial_v = 0.0,
               double cargo_initial_x = 0.0, double cargo_initial_v = 0.0);  // NUEVOS
    
    double motorForce(double t = 0.0) const;  // Renombrado
    double springForce() const;  // NUEVO: fuerza del resorte
    
    void updateChemicalState(double t, double dt);
    double getPotentialEnergy() const; 
    double getSpringEnergy() const;  // NUEVO: energía del resorte
    
    // Métodos de acceso
    Particle& getParticle() { return p; }
    CargoParticle& getCargoParticle() { return cargo; }  // NUEVO
    int getCurrentState() const { return chemicalState.getState(); }

    // Métodos para parámetros de Langevin
    double getGamma() const;
    double getKBT() const;
    double generateGaussianNoise() const;
    
    // Métodos para el resorte
    double getSpringConstant() const { return k_spring; }
    double getSpringLength() const { return L0; }
};

#endif // MOTORMODEL_H