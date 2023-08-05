"""Example 7: Estimation using measured concentration data with new KipetModel"""

# Standard library imports
import sys # Only needed for running the example from the command line

# Third party imports

# Kipet library imports
from kipet import KipetModel
                                                                                                    
if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2:
        if int(sys.argv[1]):
            with_plots = False
 
    kipet_model = KipetModel()
 
    r1 = kipet_model.new_reaction('reaction-1')   
 
    # Add the model parameters
    r1.add_parameter('k1', value=2.0, bounds=(0.0, 5.0))
    r1.add_parameter('k2', value=0.2, bounds=(0.0, 2.0))
    
    # Declare the components and give the initial values
    r1.add_component('A', value=0.001, variance=1e-10)
    r1.add_component('B', value=0.0, variance=1e-11)
    r1.add_component('C', value=0.0, variance=1e-8)
   
    # Use this function to replace the old filename set-up
    filename = 'example_data/delayed_data.csv'
    full_data = kipet_model.read_data_file(filename)
    
    data_set = full_data.iloc[::3]
    r1.add_data('C_data', data=data_set)
    
    # Use step functions to turn on the reactions
    r1.add_step('b1', time=2, fixed=False, switch='on')
    r1.add_step('b2', time=2.1, fixed=False, switch='on')
    
    c = r1.get_model_vars()
    
    R1 = c.b1 * (c.k1 * c.A)
    R2 = c.b2 * (c.k2 * c.B)
    
    # Define the reaction model
    r1.add_ode('A', -R1 )
    r1.add_ode('B', R1 - R2 )
    r1.add_ode('C', R2 )
    
    # Settings
    r1.settings.collocation.nfe = 60
    r1.settings.collocation.ncp = 3
    
    r1.settings.solver.linear_solver = 'ma57'
    r1.settings.parameter_estimator.sim_init = True
    
    # # Run KIPET
    r1.run_opt()  
    
    # Display the results
    r1.results.show_parameters

    if with_plots:
        r1.plot()