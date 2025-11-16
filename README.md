# Minimum-Energy Crossing Point calculator for UMA + ASE

A simple calculator to find the MECP of two energy surfaces (e.g. different spins) using UMA calculator in ASE.
The optimization objective (i.e., the energy reported by the calculator to the optimizer) for systems $s_1$ and $s_2$ is simply:
$$
\mathcal{L}= E = \frac{1}{2} \( E_{s_1} + E_{s_2} \) \frac{1}{2} \lambda \( E_{s_1} - E_{s_2} \)^2.
$$

The forces reported by the calculator are
$$
\vec{F} = \frac{1}{2} \( \vec{F}_{s_1} + \vec{F}_{s_2} \) + \frac{1}{2} \lambda \( E_{s_1} - E_{s_2} \) \( \vec{F}_{s_1} - \vec{F}_{s_2} \)
$$