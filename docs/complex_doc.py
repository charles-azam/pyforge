from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

from pyforge.note import (Citation, DocumentConfig, Figure, Reference, Table,
                          Title, display)

# Document configuration
config = DocumentConfig(
    title="Harmonic Oscillator Systems in Classical Mechanics",
    author="Dr. Jane Smith",
    date="2025-05-17",
    bib_path=Path("docs/refs.bib"),
)
display(config)

# Function to create a simple harmonic oscillator plot
def create_sho_plot():
    """Create a simple harmonic oscillator plot"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Time points
    t = np.linspace(0, 10, 1000)

    # Parameters
    omega = 2.0  # angular frequency
    A = 1.0  # amplitude
    phi = 0.0  # phase

    # Position and velocity
    x = A * np.cos(omega * t + phi)
    v = -A * omega * np.sin(omega * t + phi)

    # Energy
    E_kinetic = 0.5 * v**2
    E_potential = 0.5 * (omega**2) * x**2
    E_total = E_kinetic + E_potential

    # Plot
    ax.plot(t, x, label="Position (x)", color="blue")
    ax.plot(t, v, label="Velocity (v)", color="red")
    ax.plot(t, E_kinetic, label="Kinetic Energy", color="green", linestyle="--")
    ax.plot(t, E_potential, label="Potential Energy", color="purple", linestyle="--")
    ax.plot(t, E_total, label="Total Energy", color="black")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.set_title("Simple Harmonic Oscillator")
    ax.grid(True)
    ax.legend()

    return fig


# Function to create a phase space plot
def create_phase_space_plot():
    """Create a phase space plot for a simple harmonic oscillator"""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Parameters
    omega = 2.0  # angular frequency

    # Different initial conditions (different energies)
    amplitudes = [0.5, 1.0, 1.5, 2.0, 2.5]

    for A in amplitudes:
        # Phase space trajectory (circle with radius A)
        theta = np.linspace(0, 2 * np.pi, 100)
        x = A * np.cos(theta)
        v = -A * omega * np.sin(theta)
        ax.plot(x, v, label=f"E = {0.5 * (omega**2) * A**2:.2f}")

    ax.set_xlabel("Position (x)")
    ax.set_ylabel("Velocity (v)")
    ax.set_title("Phase Space Trajectories for Simple Harmonic Oscillator")
    ax.grid(True)
    ax.legend(title="Energy Levels")
    ax.set_aspect("equal")

    return fig


# Function to create a damped oscillator plot
def create_damped_oscillator_plot():
    """Create a damped harmonic oscillator plot"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Time points
    t = np.linspace(0, 20, 1000)

    # Parameters
    omega0 = 2.0  # natural frequency

    # Different damping ratios
    damping_ratios = [0.0, 0.1, 0.5, 1.0, 2.0]
    labels = ["Undamped", "Underdamped", "Critically damped", "Overdamped"]

    for i, zeta in enumerate(damping_ratios[:-1]):  # Skip the last one for the plot
        if zeta == 0:
            # Undamped
            x = np.cos(omega0 * t)
        elif zeta < 1:
            # Underdamped
            omega_d = omega0 * np.sqrt(1 - zeta**2)
            x = np.exp(-zeta * omega0 * t) * np.cos(omega_d * t)
        elif zeta == 1:
            # Critically damped
            x = np.exp(-omega0 * t) * (1 + omega0 * t)
        else:
            # Overdamped
            alpha = omega0 * (zeta + np.sqrt(zeta**2 - 1))
            beta = omega0 * (zeta - np.sqrt(zeta**2 - 1))
            x = (np.exp(-alpha * t) - np.exp(-beta * t)) / (beta - alpha)

        ax.plot(t, x, label=labels[i])

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Position (x)")
    ax.set_title("Damped Harmonic Oscillator")
    ax.grid(True)
    ax.legend()

    return fig


# Function to create a driven oscillator plot
def create_driven_oscillator_plot():
    """Create a driven harmonic oscillator plot showing resonance"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Frequency range
    omega_range = np.linspace(0.1, 3.0, 1000)

    # Parameters
    omega0 = 1.0  # natural frequency

    # Different damping ratios
    damping_ratios = [0.05, 0.1, 0.2, 0.5]

    for zeta in damping_ratios:
        # Amplitude response
        amplitude = 1.0 / np.sqrt(
            (1 - (omega_range / omega0) ** 2) ** 2
            + (2 * zeta * omega_range / omega0) ** 2
        )

        ax.plot(omega_range / omega0, amplitude, label=f"ζ = {zeta}")

    ax.set_xlabel("Frequency Ratio (ω/ω₀)")
    ax.set_ylabel("Amplitude Ratio (A/F₀)")
    ax.set_title("Resonance in Driven Harmonic Oscillator")
    ax.grid(True)
    ax.legend()
    ax.set_ylim(0, 10)

    return fig


# Function to simulate a double pendulum
def double_pendulum(t, y, L1, L2, m1, m2, g):
    """Equations of motion for a double pendulum"""
    theta1, omega1, theta2, omega2 = y

    c = np.cos(theta1 - theta2)
    s = np.sin(theta1 - theta2)

    # Derivatives
    dtheta1 = omega1
    dtheta2 = omega2

    # Equations of motion
    domega1 = (
        m2 * g * np.sin(theta2) * c
        - m2 * s * (L1 * omega1**2 * c + L2 * omega2**2)
        - (m1 + m2) * g * np.sin(theta1)
    ) / (L1 * (m1 + m2 * s**2))

    domega2 = (
        (m1 + m2) * (L1 * omega1**2 * s - g * np.sin(theta2) + g * np.sin(theta1) * c)
        + m2 * L2 * omega2**2 * s * c
    ) / (L2 * (m1 + m2 * s**2))

    return [dtheta1, domega1, dtheta2, domega2]


def create_double_pendulum_plot():
    """Create a double pendulum trajectory plot"""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Parameters
    L1, L2 = 1.0, 1.0  # lengths
    m1, m2 = 1.0, 1.0  # masses
    g = 9.81  # gravity

    # Initial conditions: [theta1, omega1, theta2, omega2]
    y0 = [np.pi / 2, 0, np.pi / 2, 0]  # Start with both pendulums at 90 degrees

    # Time span
    t_span = (0, 10)
    t_eval = np.linspace(*t_span, 1000)

    # Solve the differential equations
    sol = solve_ivp(
        lambda t, y: double_pendulum(t, y, L1, L2, m1, m2, g),
        t_span,
        y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-8,
    )

    # Extract solutions
    theta1, omega1, theta2, omega2 = sol.y

    # Convert to Cartesian coordinates
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)

    # Plot the trajectory of the second pendulum
    ax.plot(x2, y2, "b-", alpha=0.5, label="Pendulum 2 Trajectory")

    # Plot the final position
    ax.plot(
        [0, x1[-1], x2[-1]], [0, y1[-1], y2[-1]], "ko-", lw=2, label="Final Position"
    )

    # Plot the pendulum rods
    ax.plot([0, x1[0], x2[0]], [0, y1[0], y2[0]], "ro-", lw=2, label="Initial Position")

    ax.set_xlim(-L1 - L2 - 0.5, L1 + L2 + 0.5)
    ax.set_ylim(-L1 - L2 - 0.5, L1 + L2 + 0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Double Pendulum Trajectory")
    ax.grid(True)
    ax.legend()
    ax.set_aspect("equal")

    return fig


# Create all the figures
sho_fig = Figure.from_matplotlib(
    create_sho_plot(),
    "simple_harmonic_oscillator.png",
    "Position, velocity, and energy of a simple harmonic oscillator",
    "fig-sho"
)

phase_space_fig = Figure.from_matplotlib(
    create_phase_space_plot(),
    "phase_space.png",
    "Phase space trajectories for a simple harmonic oscillator at different energy levels",
    "fig-phase"
)

damped_fig = Figure.from_matplotlib(
    create_damped_oscillator_plot(),
    "damped_oscillator.png",
    "Response of damped harmonic oscillators with different damping ratios",
    "fig-damped"
)

resonance_fig = Figure.from_matplotlib(
    create_driven_oscillator_plot(),
    "resonance.png",
    "Resonance curves for driven harmonic oscillators with different damping ratios",
    "fig-resonance"
)

double_pendulum_fig = Figure.from_matplotlib(
    create_double_pendulum_plot(),
    "double_pendulum.png",
    "Trajectory of a double pendulum system",
    "fig-double-pendulum"
)

# Create data for the table
oscillator_types = pd.DataFrame(
    {
        "Type": ["Simple Harmonic", "Damped", "Driven", "Coupled"],
        "Equation": [
            "m\\ddot{x} + kx = 0",
            "m\\ddot{x} + c\\dot{x} + kx = 0",
            "m\\ddot{x} + c\\dot{x} + kx = F_0\\cos(\\omega t)",
            "System of coupled ODEs",
        ],
        "Natural Frequency": [
            "\\omega_0 = \\sqrt{k/m}",
            "\\omega_d = \\omega_0\\sqrt{1-\\zeta^2}",
            "\\omega_0 = \\sqrt{k/m}",
            "Multiple frequencies",
        ],
        "Applications": [
            "Springs, pendulums",
            "Shock absorbers, RLC circuits",
            "Forced vibrations, resonance",
            "Coupled pendulums, molecules",
        ],
    }
)

# Document content
display(
    Title("# Introduction to Harmonic Oscillators"),
    """Harmonic oscillators are fundamental systems in classical mechanics that describe 
periodic motion where a restoring force is proportional to the displacement from 
equilibrium. These systems are ubiquitous in physics and engineering, from simple 
pendulums to complex molecular vibrations.""",
    """The study of harmonic oscillators provides insights into many physical phenomena 
and serves as a foundation for understanding more complex dynamical systems. This 
document explores various types of harmonic oscillators and their behavior.""",
    Citation("taylor2005", "Taylor (2005)"),
    Title("## Simple Harmonic Oscillator"),
    """The simple harmonic oscillator (SHO) is the most basic oscillatory system, 
described by the differential equation:

$$m\\ddot{x} + kx = 0$$

where $m$ is the mass, $k$ is the spring constant, and $x$ is the displacement. 
The solution to this equation is a sinusoidal function with a natural frequency 
$\\omega_0 = \\sqrt{k/m}$.

The following figure shows the position, velocity, and energy of a simple harmonic 
oscillator over time:""",
    sho_fig,
    """As shown in """,
    Reference("fig-sho", "Figure 1"),
    """, the total energy (kinetic + potential) remains constant throughout the motion, 
while the kinetic and potential energies oscillate out of phase with each other.""",
    Title("## Phase Space Representation"),
    """The dynamics of a harmonic oscillator can be visualized in phase space, where 
position and velocity form the axes. For a simple harmonic oscillator, the phase 
space trajectory is an ellipse (or circle if properly normalized):""",
    phase_space_fig,
    """Each closed curve in """,
    Reference("fig-phase", "Figure 2"),
    """ represents a different energy level of the oscillator. The area enclosed by 
each curve is proportional to the total energy of the system.""",
    Title("## Damped Harmonic Oscillator"),
    """In real physical systems, energy is dissipated through friction or other 
resistive forces. A damped harmonic oscillator includes a velocity-dependent 
damping term:

$$m\\ddot{x} + c\\dot{x} + kx = 0$$

where $c$ is the damping coefficient. The behavior of the system depends on the 
damping ratio $\\zeta = \\frac{c}{2\\sqrt{km}}$:""",
    damped_fig,
    """As shown in """,
    Reference("fig-damped", "Figure 3"),
    """, the system can exhibit underdamped (oscillatory), critically damped, or 
overdamped behavior depending on the damping ratio.""",
    Title("## Driven Harmonic Oscillator and Resonance"),
    """When an external periodic force is applied to a harmonic oscillator, we have 
a driven (or forced) harmonic oscillator:

$$m\\ddot{x} + c\\dot{x} + kx = F_0\\cos(\\omega t)$$

where $F_0$ is the amplitude of the driving force and $\\omega$ is its frequency. 
A key phenomenon in driven oscillators is resonance, which occurs when the driving 
frequency approaches the natural frequency of the system:""",
    resonance_fig,
    """As shown in """,
    Reference("fig-resonance", "Figure 4"),
    """, the amplitude of oscillation peaks near the natural frequency, with the peak 
becoming sharper for lower damping ratios. Resonance has important applications in 
many fields, from mechanical engineering to electrical circuits.""",
    Citation("feynman1963", "Feynman et al. (1963)"),
    Title("## Complex Oscillatory Systems: Double Pendulum"),
    """While simple harmonic oscillators exhibit regular, predictable behavior, many 
real-world systems involve coupled oscillators that can display complex dynamics. 
The double pendulum is a classic example of a system that can exhibit chaotic 
behavior:""",
    double_pendulum_fig,
    """The double pendulum shown in """,
    Reference("fig-double-pendulum", "Figure 5"),
    """ consists of two pendulums attached end to end. The motion is governed by a 
system of coupled differential equations and is highly sensitive to initial 
conditions—a hallmark of chaotic systems.""",
    Title("## Types of Oscillatory Systems"),
    """The following table summarizes the key characteristics of different types of 
oscillatory systems:""",
    Table(
        oscillator_types,
        "Comparison of different types of oscillatory systems",
        "table-oscillators",
    ),
    """As shown in """,
    Reference("table-oscillators", "Table 1"),
    """, oscillatory systems range from simple to complex, with applications across 
various domains of physics and engineering.""",
    Title("# Conclusion"),
    """Harmonic oscillators are fundamental to our understanding of periodic motion in 
physical systems. From the simple pendulum to complex coupled systems, the principles 
of oscillatory motion help explain phenomena ranging from mechanical vibrations to 
electromagnetic waves.

The mathematical tools developed for analyzing harmonic oscillators—differential 
equations, phase space representations, and frequency analysis—form the foundation 
for understanding more complex dynamical systems in classical and quantum mechanics.""",
    Citation("goldstein2002", "Goldstein et al. (2002)"),
)
