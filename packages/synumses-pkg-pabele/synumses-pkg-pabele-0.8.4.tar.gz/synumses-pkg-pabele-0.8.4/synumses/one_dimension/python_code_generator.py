"""
This module generates the python code for the
module **scharfetter_gummel_bernoulli.py**.
It solves the *Van Roosbroeck equations* using the 
*Scharfetter Gummel Scheme*.

It uses the SymPy module to generate the Jacobian matrix.
"""

from sympy import symbols, Symbol 
from sympy import Function
from sympy import solve, pretty
from sympy import diff
from sympy import sin, cos, exp, ln, sinh, cosh, sqrt, exp, Abs
from sympy import simplify, trigsimp
from sympy.parsing.sympy_parser import parse_expr

from sympy import srepr

import itertools

import time

#
# activate if simplify() is not to be used
# this results in much faster calculation
#
def simplify(x):
    return x

def bernoulli_poly(expr):
    """
    Returns a polynom to approximate the Bernoulli function. 
    """
    #return 1.0
    return 1.0 - expr/2.0
    #return 1.0 - expr/2.0 + expr**2/12.0 - expr**4/720.0 
    #return 1.0 - expr/2.0 + expr**2/12.0 - expr**4/720.0 + expr**6/30240.0 
    #return 1.0 - expr/2.0 + expr**2/12.0 - expr**4/720.0 + expr**6/30240.0 - expr**8/1209600.0
    #return expr/(exp(expr) - 1)


def bernoulli_exp(expr):
    """
    Returns the Bernoulli-function.
    """
    return expr/(exp(expr) - 1)
    
#
# Global variables
#
bernoulli = Function('bernoulli')
bernoulli_limit = symbols('parameters.bernoulli_limit')

x = Symbol('x')

Phi_n_k, Phi_n_l = symbols('Phi_n_k, Phi_n_l')
Phi_p_k, Phi_p_l = symbols('Phi_p_k, Phi_p_l')
Psi_k, Psi_l     = symbols('Psi_k, Psi_l')

Chi_k, Chi_l = symbols('Chi_k, Chi_l')
Eg_k, Eg_l   = symbols('Eg_k, Eg_l')
Nv_k, Nv_l   = symbols('Nv_k, Nv_l')
Nc_k, Nc_l   = symbols('Nc_k, Nc_l')

mu_n_k, mu_n_l   = symbols('mu_n_k, mu_n_l')
mu_p_k, mu_p_l   = symbols('mu_p_k, mu_p_l')

Psi_m1, Psi_00, Psi_p1       = symbols('parameters.u[3*(i-1)+0], parameters.u[(3*i+0)+0], parameters.u[3*(i+1)+0]')
Phi_p_m1, Phi_p_00, Phi_p_p1 = symbols('parameters.u[3*(i-1)+1], parameters.u[(3*i+0)+1], parameters.u[3*(i+1)+1]')
Phi_n_m1, Phi_n_00, Phi_n_p1 = symbols('parameters.u[3*(i-1)+2], parameters.u[(3*i+0)+2], parameters.u[3*(i+1)+2]')

Psi_old, Phi_p_old,  Phi_n_old = symbols('parameters.u_old[(3*i+0)+0], parameters.u_old[(3*i+0)+1], parameters.u_old[(3*i+0)+2]')

Chi_m1, Chi_00, Chi_p1    = symbols('parameters.Chi[i-1], parameters.Chi[i+0], parameters.Chi[i+1]')
Eg_m1, Eg_00, Eg_p1       = symbols('parameters.Eg[i-1], parameters.Eg[i+0], parameters.Eg[i+1]')

Nv_m1, Nv_00, Nv_p1       = symbols('parameters.Nv[i-1], parameters.Nv[i+0], parameters.Nv[i+1]')
Nc_m1, Nc_00, Nc_p1       = symbols('parameters.Nc[i-1], parameters.Nc[i+0], parameters.Nc[i+1]')

mu_n_m1, mu_n_00, mu_n_p1       = symbols('parameters.mu_n[i-1], parameters.mu_n[i+0], parameters.mu_n[i+1]')
mu_p_m1, mu_p_00, mu_p_p1       = symbols('parameters.mu_p[i-1], parameters.mu_p[i+0], parameters.mu_p[i+1]')

dx = symbols('parameters.dx')
dt = symbols('parameters.dt')

recombination = symbols('parameters.recombination[i]')
generation    = symbols('parameters.generation[i]')


C_00 = symbols('parameters.C[i]')
Epsilon_00 = symbols('parameters.Epsilon[i]')

np_exp  = Function('np.exp')
np_sqrt = Function('np.sqrt')
np_abs  = Function('np.abs')

kB = symbols('parameters.kB')
T  = symbols('parameters.T')
q  = symbols('parameters.q')


Ut = (kB * T) / q


Cau = symbols('parameters.Cau[i]')

#ni = Function('ni')
#p = Function('p')
#n = Function('n')

ni2 =(Nv_00*Nc_00)*exp(-Eg_00/Ut)
p  = Nv_00*exp(( (-Chi_00 - Eg_00) + Phi_p_00 - Psi_00)/Ut)
n  = Nc_00*exp((        +Chi_00    - Phi_n_00 + Psi_00)/Ut)

p_old  = Nv_00*exp(( (-Chi_00 - Eg_00) + Phi_p_old - Psi_old)/Ut)
n_old  = Nc_00*exp((        +Chi_00    - Phi_n_old + Psi_old)/Ut)


# **********************************
# **********************************
#     Van Roosbroeck equations
# **********************************
# **********************************

#
# Poisson equaton
#
poisson = ((Psi_p1 - 2.*Psi_00 + Psi_m1) + q / Epsilon_00 * (C_00 + p - n)*dx**2)


# 
# Electrical hole current density
#
j_p =+kB*T/dx*(mu_p_k + mu_p_l)/2.*(Nv_k + Nv_l)/2.*exp(-(Chi_k + Eg_k + Chi_l + Eg_l)/(2.*Ut))*(
    +bernoulli(+(Psi_l-Psi_k)/(Ut)) * exp((Phi_p_k - Psi_k)/(Ut))
    -bernoulli(-(Psi_l-Psi_k)/(Ut)) * exp((Phi_p_l - Psi_l)/(Ut))
)


j_n = -kB*T/dx*(mu_n_k + mu_n_l)/2.*(Nc_k + Nc_l)/2.*exp((Chi_k + Chi_l)/(2.*Ut))*(
    +bernoulli(-(Psi_l-Psi_k)/(Ut)) * exp((Psi_k - Phi_n_k)/Ut)
    -bernoulli(+(Psi_l-Psi_k)/(Ut)) * exp((Psi_l - Phi_n_l)/Ut)
)

#
# Divergence of current density
# 
div_j_p = (
    - j_p.subs([(Psi_k, Psi_00),(Psi_l, Psi_p1),(Phi_p_k, Phi_p_00),(Phi_p_l,Phi_p_p1),(Eg_k, Eg_00),(Eg_l, Eg_p1),
                (Chi_k, Chi_00),(Chi_l, Chi_p1),(Nv_k, Nv_00),(Nv_l, Nv_p1),(mu_p_k, mu_p_00),(mu_p_l, mu_p_p1)])
    + j_p.subs([(Psi_k, Psi_m1),(Psi_l, Psi_00),(Phi_p_k, Phi_p_m1),(Phi_p_l,Phi_p_00),(Eg_k, Eg_m1),(Eg_l, Eg_00),
                (Chi_k, Chi_m1),(Chi_l, Chi_00),(Nv_k, Nv_m1),(Nv_l, Nv_00),(mu_p_k, mu_p_m1),(mu_p_l, mu_p_00)])
    - q*(Cau*(n*p-ni2)-generation)*dx
)

div_j_n = (
    + j_n.subs([(Psi_k, Psi_00),(Psi_l, Psi_p1),(Phi_n_k, Phi_n_00),(Phi_n_l,Phi_n_p1),
                (Chi_k, Chi_00),(Chi_l, Chi_p1),(Nc_k, Nc_00),(Nc_l, Nc_p1),(mu_n_k, mu_n_00),(mu_n_l, mu_n_p1)])
    - j_n.subs([(Psi_k, Psi_m1),(Psi_l, Psi_00),(Phi_n_k, Phi_n_m1),(Phi_n_l,Phi_n_00),
                (Chi_k, Chi_m1),(Chi_l, Chi_00),(Nc_k, Nc_m1),(Nc_l, Nc_00),(mu_n_k, mu_n_m1),(mu_n_l, mu_n_00)])
    - q*(Cau*(n*p-ni2)-generation)*dx
)

#
# Time dependent divergence of current density
#
div_j_p_t = div_j_p + q*(p - p_old)*(dx/dt)
div_j_n_t = div_j_n + q*(n - n_old)*(dx/dt)

#
# The variable functions is defined before calling the functions
#                   makeUpdate_b and makeJacobi
# 
functions = []

partial_derivatives = [
    ["3*(i-1)+0",Psi_m1  ],
    ["3*(i+0)+0",Psi_00  ],
    ["3*(i+1)+0",Psi_p1  ],
    ["3*(i-1)+1",Phi_p_m1],
    ["3*(i+0)+1",Phi_p_00],
    ["3*(i+1)+1",Phi_p_p1],
    ["3*(i-1)+2",Phi_n_m1],
    ["3*(i+0)+2",Phi_n_00],
    ["3*(i+1)+2",Phi_n_p1]
]


substitutes = {
    "left"  : {
        Psi_m1: Symbol('(ohm_potential(parameters.C[0], parameters.Chi[0], parameters.Eg[0], parameters.Nc[0], parameters.Nv[0]) + Ua)'),
        Phi_p_m1: Symbol('Ua'),
        Phi_n_m1: Symbol('Ua'),

        Chi_m1: Chi_00,
        Eg_m1: Eg_00,
        Nv_m1: Nv_00,
        Nc_m1: Nc_00,
        mu_n_m1: mu_n_00,
        mu_p_m1: mu_p_00,
        
        exp:  np_exp,
        sqrt: np_sqrt,
        Abs:  np_abs
    },
    "right" : {
        Psi_p1: Symbol('(ohm_potential(parameters.C[parameters.n-1], parameters.Chi[parameters.n-1], parameters.Eg[parameters.n-1], parameters.Nc[parameters.n-1], parameters.Nv[parameters.n-1]) + Ub)'),
        Phi_p_p1: Symbol('Ub'),
        Phi_n_p1: Symbol('Ub'),
        
        Chi_p1: Chi_00,
        Eg_p1: Eg_00,
        Nv_p1: Nv_00,
        Nc_p1: Nc_00,
        mu_n_p1: mu_n_00,
        mu_p_p1: mu_p_00,
        
        exp:  np_exp,
        sqrt: np_sqrt,
        Abs:  np_abs
    },
    "center": {
        exp:  np_exp,
        sqrt: np_sqrt,
        Abs:  np_abs
    }
}

#
# Depending on the value of the argument the Bernoulli function is substituded
#
search_sub_function = ({"function"  : bernoulli,
                        "if_states" : ['<','<'],
                        "if_values" : [-bernoulli_limit, bernoulli_limit],
                        "if_subs"   : [bernoulli_exp , bernoulli_poly],
                        "else_sub"  : bernoulli_exp
})


def substituteFunctions(function, sub_function, left_side, sub_args = [], partial_derivative = None, tabs=0, do_simplify = 0):
    """
    Depending on the value of the argument of a function it is substituted.
    """

#    print("### function:", function)
#    print("### sub args:", sub_args)
#    print("### left_side:", left_side)
#    print("### sub_args", sub_args)
#    print()
#    print("### function.subs(sub_args):", function.subs(sub_args))
#    if partial_derivative  is not None:
#        print("### diff(function, partial_derivative).subs(sub_args):", diff(function, partial_derivative).subs(sub_args))
#    print("### srepr(function):", srepr(function))
#    print("### sub_function:", sub_function)


# ****************************************************
# Search for all arguments of sub_function["function"]
# ****************************************************
    
    comb = []
    found_arguments = []
    
    for funcs in function.find(Function): #loop all functions
        if(str(type(funcs)) == str(sub_function["function"])):
                found_arguments.append(funcs.args[0])

    comb = (sub_function, found_arguments)

    perm = list(itertools.product(range(len(sub_function["if_states"])+1), repeat = len(found_arguments)))


    
    if not found_arguments:

        for ii in range(tabs):
            print("\t", end = '')

        print(left_side, "= ", end = '')

        
        if  partial_derivative is not None:
                
            part_der = diff(simplify(function), partial_derivative).subs(sub_args)
            
            if (do_simplify):
                print(simplify(part_der))
            else:
                print(part_der)
        else:

            if (do_simplify):
                print(simplify(function).subs(sub_args))
            else:
                print(function.subs(sub_args))


    else:
        
        for i in range(len(perm)):

            for ii in range(tabs):
                print("\t", end = '')

            if (i==0):
                print("if (", end = '')
            elif(i<(len(perm)-1)):
                print("elif (", end = '')
            else:
                print("else", end = '')

            stateSet = 0;
            substitutes = []
            for j in range(len(found_arguments)): #number of arguments

                #print("comb[0][]:", comb[0]["function"](comb[1][j]))
                #print("comb[0][]:", comb[0]["if_subs"][perm[i][j]](comb[1][j]))

                #substitutes.append((comb[0]["function"](comb[1][j]), comb[0]["if_subs"][perm[i][j]](comb[1][j])))

                if (j==0):
                    if (perm[i][j] != len(sub_function["if_states"])):
                        #print("(perm:",perm[i][j], "arg:", j, ")",end = '')
                        print("(", comb[1][j].subs(sub_args), comb[0]["if_states"][perm[i][j]], comb[0]["if_values"][perm[i][j]], ")", end = '')
                        substitutes.append((comb[0]["function"](comb[1][j]), comb[0]["if_subs"][perm[i][j]](comb[1][j])))
                        stateSet=1
                    else:
                        substitutes.append((comb[0]["function"](comb[1][j]), comb[0]["else_sub"](comb[1][j])))
                        
                else:
                    if (perm[i][j] != len(sub_function["if_states"])):
                        substitutes.append((comb[0]["function"](comb[1][j]), comb[0]["if_subs"][perm[i][j]](comb[1][j])))
                        if (stateSet==1):
                            #print(" and ", "(perm:", perm[i][j], "arg:", j, ")",end = '')
                            print(" and (", comb[1][j].subs(sub_args), comb[0]["if_states"][perm[i][j]], comb[0]["if_values"][perm[i][j]], ")", end = '')
                            
                        else:
                           #print("(perm:", perm[i][j], "arg:", j, ")",end = '') 
                           print("(", comb[1][j].subs(sub_args), comb[0]["if_states"][perm[i][j]], comb[0]["if_values"][perm[i][j]], ")", end = '')
                           stateSet = 1;
                    else:
                       substitutes.append((comb[0]["function"](comb[1][j]), comb[0]["else_sub"](comb[1][j]))) 
                


            if(i<(len(perm)-1)):
                print("):\n", end = '')
            else:
                print(":\n", end = '')

            for ii in range(tabs):
                print("\t", end = '')

            print("\t" , end = '')
            print(left_side, "= ", end = '')

            if  partial_derivative is not None:
                
                part_der = diff(function.subs(substitutes), partial_derivative).subs(sub_args)

                if (do_simplify):
                    print(simplify(part_der))
                else:
                    print(part_der)
            else:

                if (do_simplify):
                    print(simplify(function).subs(substitutes).subs(sub_args))
                else:
                    print(function.subs(substitutes).subs(sub_args))


            print()


def makeUpdate_b(name):

    """
    Generates the function vector.
    """

    print("################################")
    print("########### {name} ###########".format(name=name))
    print("################################")

    print("def {name}(Ua, Ub):".format(name=name)) 
    print()
    print("\tfor i in range(0, parameters.n):")


    for s in ["left", "right", "center"]:

        if (s =="left"):
            print("\t\tif (i==0) :")
        elif (s=="right"):
            print("\t\telif(i==parameters.n-1):")
        else:
            print("\t\telse:")

        print("\t\t\t#################")
        print("\t\t\t### ",s, "###")
        print("\t\t\t#################")
        for function in functions:

             substituteFunctions(function[1],
                                 search_sub_function,
                                 left_side = "parameters.b["+function[0]+"]",
                                 sub_args = substitutes[s],
                                 tabs = 3,
                                 do_simplify = 1
                )

    print() 
    print("\treturn None")
    print()
    print()
    print()

    
def makeJacobi(name):
    
    print("######################################")
    print("###########  {name} ##################".format(name=name))
    print("######################################")

    print("def {name}(Ua, Ub):".format(name=name))
    print()
    print("\tfor i in range(0, parameters.n):")

    for s in ["left", "right", "center"]:

        if (s =="left"):
            print("\t\tif (i==0) :")
        elif (s=="right"):
            print("\t\telif(i==parameters.n-1):")
        else:
            print("\t\telse:")

        print()
        print("\t\t\t#################")
        print("\t\t\t### ",s, "###")
        print("\t\t\t#################")

        #print("# ",substitutes[s])

        for function in functions:
            print
            print("\t\t\t#######################")
            print("\t\t\t### ",function[2]," ###")
            print("\t\t\t#######################")
            for partial_derivative in partial_derivatives:
                if ((s == "left"  and (partial_derivative[1] in [Psi_m1, Phi_p_m1, Phi_n_m1])) or
                    (s == "right" and (partial_derivative[1] in [Psi_p1, Phi_p_p1, Phi_n_p1]))):
                    print("\t\t\t###"+"parameters.A["
                          +function[0]
                          +","
                          +partial_derivative[0]
                          +"]",
                          " = ..."
                    )
                else:
                    substituteFunctions(-function[1],
                                        search_sub_function, 
                                        "parameters.A["+function[0]+","+partial_derivative[0]+"]",
                                        sub_args = substitutes[s],
                                        partial_derivative = partial_derivative[1],
                                        tabs=4,
                                        do_simplify = 1)

    print()
    print("\treturn ")
    print()
    print()

    
    
def codeGenerator():
    """
    This function generates the python code. 
    """
    # ******************************************************************
    #  functions is a global variable, being modified in this function
    # ******************************************************************
    global functions
    
   
    print("####################################")
    print("### This code was automatically  ###")
    print("###        generated             ###")
    print("###    on",time.strftime("%d.%m.%Y at %H:%M"), "   ###")
    print("####################################")
   
    print()
    
    print("#################################")
    print("###########  Import   ###########")
    print("#################################")
    print("import numpy as np")
    print()
    print("import synumses.one_dimension.parameters as parameters")
    print("from   synumses.one_dimension.functions import ohm_potential")

    print()
    print()

    print("#################################")
    print("########### Bernoulli ###########")
    print("#################################")
    print("def bernoulli(x):")

    substituteFunctions(bernoulli(x),
                        search_sub_function,
                        "x",
                        sub_args = {
                            exp: np_exp},
                        tabs = 1,
                        do_simplify = 1
    )
    print("\treturn(x)")
    
    print("############################################")
    print("########### hole_current_density ###########")
    print("############################################")
    print("def hole_current_density():")
    print()
    print("\tj_p = np.zeros(parameters.n)")
    print()
    print("\tfor i in range(0,parameters.n-1):")

    substituteFunctions(j_p,
                        search_sub_function,
                        "j_p[i]",
                        sub_args = {
                            Psi_k:   Psi_00, 
                            Psi_l:   Psi_p1,
                            Phi_p_k: Phi_p_00,
                            Phi_p_l: Phi_p_p1,
                            Chi_k:   Chi_00,
                            Chi_l:   Chi_p1,
                            Eg_k:    Eg_00,
                            Eg_l:    Eg_p1,
                            Nv_k:    Nv_00,
                            Nv_l:    Nv_p1,
                            mu_p_k:  mu_p_00,
                            mu_p_l:  mu_p_p1,
                            mu_n_k:  mu_n_00,
                            mu_n_l:  mu_n_p1,
                            exp:     np_exp,
                            Abs:     np_abs
                        },
                        tabs = 2,
                        do_simplify = 1
    )

    print()
    print("\ti = parameters.n-1")
    print("\tj_p[i] =  j_p[i-1]")
    print()
    print("\treturn j_p")
    print()
    print()

    print("################################################")
    print("########### electron_current_density ###########")
    print("################################################")
    print("def electron_current_density():")
    print()
    print("\tj_n = np.zeros(parameters.n)")
    print()
    print("\tfor i in range(0,parameters.n-1):")

    substituteFunctions(j_n,
                        search_sub_function,
                        "j_n[i]",
                        sub_args = {
                            Psi_k:   Psi_00, 
                            Psi_l:   Psi_p1,
                            Phi_n_k: Phi_n_00,
                            Phi_n_l: Phi_n_p1,
                            Chi_k:   Chi_00,
                            Chi_l:   Chi_p1,
                            Nc_k:    Nc_00,
                            Nc_l:    Nc_p1,
                            mu_p_k:  mu_p_00,
                            mu_p_l:  mu_p_p1,
                            mu_n_k:  mu_n_00,
                            mu_n_l:  mu_n_p1,
                            exp:     np_exp,
                            Abs:     np_abs
                        },
                        tabs = 2,
                        do_simplify = 1
    )



    print()
    print("\ti = parameters.n-1")
    print("\tj_n[i] =  j_n[i-1]")
    print()
    print("\treturn j_n")
    print()
    print()

    # *****************************************************
    #
    # Generating the Jacobian matrix and b with biasing
    #
    # *****************************************************

    functions = [
        ["3*i+0",poisson, "poisson"],
        ["3*i+1",div_j_p, "div_j_p"],
        ["3*i+2",div_j_n, "div_j_n"]
    ]
    makeUpdate_b("update_b")
    makeJacobi("jacobian")

    # *****************************************************
    #
    # Generating the Jacobian matrix and b without biasing
    # for constant Fermi level 
    #
    # *****************************************************

    functions = [
        ["3*i+0",poisson, "poisson"],
        ["3*i+1",Phi_p_00 - Phi_p_m1, "div_j_p"], #Difference to the not first equations, results in a constant quasi Fermi level
        ["3*i+2",Phi_n_00 - Phi_n_m1, "div_j_n"]  #Difference to the not first equations, results in a constant quasi Fermi level
    ]
    makeUpdate_b("first_update_b")
    makeJacobi("first_jacobian")

    
    # *****************************************************
    #
    # Generating the Jacobian matrix and b for transient
    # for constant Fermi level 
    #
    # *****************************************************


    #
    # As div_j_p and div_j_n have changed functions must be updated
    #
    functions = [
        ["3*i+0",poisson, "poisson"],
        ["3*i+1",div_j_p_t, "div_j_p"],
        ["3*i+2",div_j_n_t, "div_j_n"]
    ]

    makeUpdate_b("transient_update_b")
    makeJacobi("transient_jacobian")
    

if __name__ == '__main__':

   codeGenerator()
