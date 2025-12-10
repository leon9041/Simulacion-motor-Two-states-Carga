# MOTOR MOLECULAR DE DOS ESTADOS CON CARGO
# =========================================

## DESCRIPCIÓN
Simulación de un motor molecular browniano que opera entre dos estados químicos
(U₀ y U₁), acoplado a una partícula pasiva (cargo) mediante un resorte elástico.

## ESTRUCTURA DEL PROYECTO
motor_molecular/

├── include/
│ ├── ChemicalState.h
│ ├── Integrator.h
│ ├── MotorModel.h
│ ├── Particle.h
│ └── Potential.h
├── src/
│ ├── ChemicalState.cpp
│ ├── Integrator.cpp
│ ├── MotorModel.cpp
│ ├── main.cpp
│ ├── Potential.cpp
│ └── Simulator.cpp
├── results/
│ ├── animations/
│ ├── figures/
│ └── datos_motor_con_cargo.txt
├── animations_cargo.py
├── plot_results_cargo.py
├── build.py
├── run_animation_cargo.py
└── README.txt

COMPILACIÓN Y EJECUCIÓN
MÉTODO 1: Automático (recomendado)

python build.py
