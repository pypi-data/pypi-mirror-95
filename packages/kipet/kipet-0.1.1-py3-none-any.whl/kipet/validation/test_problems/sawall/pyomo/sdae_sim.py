
#  _________________________________________________________________________
#
#  Kipet: Kinetic parameter estimation toolkit
#  Copyright (c) 2016 Eli Lilly.
#  _________________________________________________________________________

# Sample Problem 2 (From Sawall et.al.)
# Basic simulation of ODE with spectral data using pyomo discretization 
#
#		\frac{dZ_a}{dt} = -k*Z_a	Z_a(0) = 1
#		\frac{dZ_b}{dt} = k*Z_a		Z_b(0) = 0
#
#               C_a(t_i) = Z_a(t_i) + w(t_i)    for all t_i in measurement points
#               D_{i,j} = \sum_{k=0}^{Nc}C_k(t_i)S(l_j) + \xi_{i,j} for all t_i, for all l_j 

from kipet.library.TemplateBuilder import *
from kipet.library.PyomoSimulator import *
import matplotlib.pyplot as plt

from kipet.library.data_tools import *
import os
import sys
import inspect

if __name__ == "__main__":

    with_plots = True
    if len(sys.argv)==2:
        if int(sys.argv[1]):
            with_plots = False
            
    # read 500x2 S matrix
    # this defines the measurement lambdas l_j but the t_i still need to be passed
    dataDirectory = os.path.abspath(
        os.path.join( os.path.dirname( os.path.abspath( inspect.getfile(
            inspect.currentframe() ) ) ), '..','..','data_sets'))
    filename = os.path.join(dataDirectory,'Slk_sawall.txt')
    S_frame = read_absorption_data_from_txt(filename)
    
    # create template model 
    builder = TemplateBuilder()    
    builder.add_mixture_component('A',1)
    builder.add_mixture_component('B',0)
    builder.add_parameter('k',0.01)
    # includes absorption data in the template and defines measurement sets
    builder.add_absorption_data(S_frame)
    builder.add_measurement_times([i for i in range(200)])
    
    # define explicit system of ODEs
    def rule_odes(m,t):
        exprs = dict()
        exprs['A'] = -m.P['k']*m.Z[t,'A']
        exprs['B'] = m.P['k']*m.Z[t,'A']
        return exprs

    builder.set_odes_rule(rule_odes)
    
    # create an instance of a pyomo model template
    # the template includes
    #   - Z variables indexed over time and components names e.g. m.Z[t,'A']
    #   - C variables indexed over measurement t_i and components names e.g. m.C[t_i,'A']
    #   - P parameters indexed over the parameter names m.P['k']
    #   - S fixed variables over measurement l_j and component names m.S[l_j,'A']
    pyomo_model = builder.create_pyomo_model(0.0,200.0)
    
    # create instance of simulator
    simulator = PyomoSimulator(pyomo_model)
    # defines the discrete points wanted in the profiles (does not include measurement points)
    simulator.apply_discretization('dae.collocation',nfe=10,ncp=1,scheme='LAGRANGE-RADAU')

    # simulate
    sigmas = {'device':0,
              'A':1e-8,
              'B':1e-8}
    results_pyomo = simulator.run_sim('ipopt',tee=True,variances=sigmas, seed=123453256)

    if with_plots:
    # display concentration and absorbance results
        results_pyomo.C.plot.line(legend=True)
        plt.xlabel("time")
        plt.ylabel("Concentration")
        plt.title("Concentration Profile")
        plt.show()
        #plt.savefig("portada2.png")
        results_pyomo.S.plot.line(legend=True)
        plt.xlabel("Wave length (s)")
        plt.ylabel("Absorbance (mol/L)")
        plt.title("Absorbance Profile")
        plt.show()
        #plt.savefig("portada1.png")
        # take a look at the data
        plot_spectral_data(results_pyomo.D,dimension='3D')
        plt.show()
        #plt.savefig("portada.png")
        #plt.figure()
        # basic principal component analysis of the data
        #basic_pca(results_pyomo.D,n=4)
        #plt.show()



