from ase.io import read, write
from ase.optimize import LBFGS
from fairchem.core import pretrained_mlip, FAIRChemCalculator
from MECPCalculator import MECPCalculator

atoms = read("singlet.xyz")

# Define two calculators for different spin states
predictor_singlet = pretrained_mlip.get_predict_unit("uma-s-1", device="cuda")
calc_singlet = FAIRChemCalculator(predictor_singlet, task_name="omol")
sys_1 = {'calc': calc_singlet, 'spin': 1, 'charge': 0}

predictor_quintet = pretrained_mlip.get_predict_unit("uma-s-1", device="cuda")
calc_quintet = FAIRChemCalculator(predictor_quintet, task_name="omol")
sys_2 = {'calc': calc_quintet, 'spin': 2, 'charge': 0}

# Assign the MECP calculator
mecp_calc = MECPCalculator(sys_1, sys_2, penalty_weight=100.0)
atoms.calc = mecp_calc

# Optimize
opt = LBFGS(atoms, trajectory='mecp.traj', logfile='mecp.log', memory=10, damping=1.0, maxstep=0.1)
opt.run(fmax=0.005)

write('MECP.xyz', atoms)