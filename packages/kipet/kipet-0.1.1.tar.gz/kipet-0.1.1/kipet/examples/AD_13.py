"""
Advanced Demonstration 13: How to solve problems with unknown initial conditions
"""
# Standard library imports
import sys

# Third party imports

# KIPET library imports
from kipet import KipetModel

if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2:
        if int(sys.argv[1]):
            with_plots = False
    
    kipet_model = KipetModel()
 
    r1 = kipet_model.new_reaction('reaction-1')   
 
    # Add the model parameters
    r1.add_parameter('k1', value=1.0, bounds=(0.0, 10.0), fixed=False)
    r1.add_parameter('k2', value=0.224, bounds=(0.0, 10.0), fixed=False)
    
    # Declare the components and give the initial values
    r1.add_component('A', value=0.001, known=False, bounds=(0.0, 0.1))
    r1.add_component('B', value=0.0)
    r1.add_component('C', value=0.0)
   
    # Use this function to replace the old filename set-up
    filename = 'example_data/Ex_1_C_data_withoutA.csv'
    
    r1.add_data(file=filename)
    
    # Define the reaction model
    c = r1.get_model_vars()
    # define explicit system of ODEs
    rates = {}
    rates['A'] = -c.k1 * c.A
    rates['B'] = c.k1 * c.A - c.k2 * c.B
    rates['C'] = c.k2 * c.B
    
    r1.add_odes(rates)

    # Repeat for the second model - the only difference is the dataset    
    r2 = kipet_model.new_reaction(name='reaction-2', model=r1)
    # Simulated second dataset with noise
    noised_data = kipet_model.add_noise_to_data(r1.datasets['ds1'].data, 0.0001) 
    
    # Add the dataset for the second model
    r2.add_data(data=noised_data)

    kipet_model.settings.solver.solver = 'ipopt_sens'

    r1.variances = {'device':1e-10,'A':1e-10,'B':1e-10,'C':1e-10}
    r2.variances = {'device':1e-4,'A':1e-4,'B':1e-4,'C':1e-4}
    
    kipet_model.run_opt()
    
    # Plot the results
    if with_plots:
        for name, model in kipet_model.models.items():
            kipet_model.results[name].show_parameters
            model.plot()