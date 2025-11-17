from ase.calculators.calculator import Calculator, all_changes

class MECPCalculator(Calculator):
    """ASE calculator wrapper for MECP optimization"""

    implemented_properties = ['energy', 'forces']

    def __init__(
            self, 
            sys_1: dict, 
            sys_2: dict, 
            penalty_weight: float=10.0,  
            logfilename: str='MECP.log', 
            **kwargs):
        super().__init__(**kwargs)
        self.calc_1 = sys_1.get['calc', None]
        self.spin_1 = sys_1.get('spin', 1)
        self.charge_1 = sys_1.get('charge', 0)
        self.calc_2 = sys_2.get['calc', None]
        self.spin_2 = sys_2.get('spin', 1)
        self.charge_2 = sys_2.get('charge', 0)
        self.penalty_weight = penalty_weight
        self.logfilename = logfilename

        # Initialize log file with header
        with open(self.logfilename, 'w') as f:
            f.write(f"{'Step':>6} {'E_sys1':>15} {'E_sys2':>15} {'ΔE':>12} {'Penalty':>12} {'Total':>15}\n")

        self.step_count = 0

    def calculate(self, atoms=None, properties=['energy'], system_changes=all_changes):
        # Calculate singlet and quintlet properties
        atoms_sys1 = atoms.copy()
        atoms_sys1.info.update({"spin": self.spin_1, "charge": self.charge_1})
        atoms_sys2 = atoms.copy()
        atoms_sys2.info.update({"spin": self.spin_2, "charge": self.charge_2})
        atoms_sys1.calc = self.calc_1
        atoms_sys2.calc = self.calc_2

        e1 = atoms_sys1.get_potential_energy()
        e2 = atoms_sys2.get_potential_energy()
        f1 = atoms_sys1.get_forces()
        f2 = atoms_sys2.get_forces()

        # Average energy
        e_avg = 0.5 * (e1 + e2)
        # Energy difference
        delta = e1 - e2
        # Penalty
        penalty = 0.5 * self.penalty_weight * delta**2

        # Forces for the penalty term (chain rule)
        f_penalty = self.penalty_weight * delta * (f1 - f2)

        # Effective forces
        f_avg = 0.5 * (f1 + f2)
        forces = f_avg + f_penalty

        # Total energy with penalty
        energy = e_avg + 0.5 * self.penalty_weight * delta**2

        self.results['energy'] = energy
        self.results['forces'] = forces

        # Log energy data
        with open(self.logfilename, 'a') as f:
            f.write(f"{self.step_count:6d} {e1:15.6f} {e2:15.6f} {delta:12.6f} {penalty:12.6f} {energy:15.6f}\n")

        self.step_count += 1
