// Integrator.h - CORRECCIÓN
#ifndef INTEGRATOR_H
#define INTEGRATOR_H

class MotorModel; // Declaración adelantada

class Integrator {
public:
    virtual void step(MotorModel& motor, double dt) = 0;
    virtual ~Integrator() {}
};

class StochasticVelocityVerletIntegrator : public Integrator {
public:
    void step(MotorModel& motor, double dt) override;
};

#endif // INTEGRATOR_H