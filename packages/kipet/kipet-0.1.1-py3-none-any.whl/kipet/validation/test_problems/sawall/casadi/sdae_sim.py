#  _________________________________________________________________________
#
#  Kipet: Kinetic parameter estimation toolkit
#  Copyright (c) 2016 Eli Lilly.
#  _________________________________________________________________________

# Sample Problem 2 (From Sawall et.al.)
# Basic simulation of ODE with spectral data using multistep-integrator 
#
#		\frac{dZ_a}{dt} = -k*Z_a	Z_a(0) = 1
#		\frac{dZ_b}{dt} = k*Z_a		Z_b(0) = 0
#
#               C_k(t_i) = Z_k(t_i) + w_k(t_i)    for all t_i in measurement points
#               D_{i,j} = \sum_{k=0}^{Nc}C_k(t_i)S_k(l_j) + \xi_{i,j} for all t_i, for all l_j 


from kipet.library.TemplateBuilder import *
from kipet.library.CasadiSimulator import *
from kipet.library.data_tools import *
import matplotlib.pyplot as plt
import os
import sys
import inspect

if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2:
        if int(sys.argv[1]):
            with_plots = False
            
    # read 200x500 D matrix
    # this defines the measurement points t_i and l_j as well
    dataDirectory = os.path.abspath(
        os.path.join( os.path.dirname( os.path.abspath( inspect.getfile(
            inspect.currentframe() ) ) ), '..','..','data_sets'))
    filename = os.path.join(dataDirectory,'Slk_sawall.txt')
    S_frame = read_absorption_data_from_txt(filename)
    
    # create template model 
    builder = TemplateBuilder()    
    builder.add_mixture_component({'A':1,'B':0})
    builder.add_parameter('k',0.01)
    # includes spectra data in the template and defines measurement sets
    builder.add_absorption_data(S_frame)
    builder.add_measurement_times([i for i in range(200)])
    # define explicit system of ODEs
    def rule_odes(m,t):
        exprs = dict()
        exprs['A'] = -m.P['k']*m.Z[t,'A']
        exprs['B'] = m.P['k']*m.Z[t,'A']
        return exprs

    builder.set_odes_rule(rule_odes)

    # create an instance of a casadi model template
    # the template includes
    #   - Z variables indexed over time and components names e.g. m.Z[t,'A']
    #   - C variables indexed over measurement t_i and components names e.g. m.C[t_i,'A']
    #   - P parameters indexed over the parameter names m.P['k']
    #   - D spectra data indexed over the t_i, l_j measurement points m.D[t_i,l_j]
    casadi_model = builder.create_casadi_model(0.0,200.0)

    # create instance of simulator
    sim = CasadiSimulator(casadi_model)
    # defines the discrete points wanted in the profiles (does not include measurement points)
    sim.apply_discretization('integrator',nfe=500)
    # simulate
    
    sigmas = {'device':1e-6,
              'A':1e-5,
              'B':1e-5}
    results_casadi = sim.run_sim("cvodes",variances=sigmas, seed=123453256)

    if with_plots:
        # displary concentrations and absorbances results
        results_casadi.C.plot.line(legend=True)
        plt.xlabel("time (s)")
        plt.ylabel("Concentration (mol/L)")
        plt.title("Concentration Profile")

        # take a look at the data
        results_casadi.D.T.plot()
        #plot_spectral_data(results_casadi.D,dimension='3D')
        # basic principal component analysis of the data
        #basic_pca(results_casadi.D,n=4)
        plt.show()

