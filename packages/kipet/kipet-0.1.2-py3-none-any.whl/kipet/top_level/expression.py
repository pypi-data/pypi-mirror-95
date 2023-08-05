"""
Expression Classes
"""
# Standad library imports

# Third party imports
from pyomo.core.expr.numeric_expr import DivisionExpression
from pyomo.environ import (
    ConcreteModel,
    Objective,
    Var, 
    )
from pyomo.environ import units as u

# KIPET library imports
from kipet.common.VisitorClasses import ReplacementVisitor
from kipet.post_model_build.replacement import _update_expression


class ExpressionBlock():
    
    """Class for general expression block classes"""
    
    def __init__(self,
                 exprs=None,
                 ):
        
        self.exprs = exprs
        self._title = 'EXPR'
        
    def display(self):
        
        if self.exprs is not None:
            print(f'{self._title} expressions:')
            for key, expr in self.exprs.items():
                print(f'{key}: {expr.expression.to_string()}')


    def display_units(self):

        if self.exprs is not None:
            print(f'{self._title} units:')
            for key, expr in self.exprs.items():
                print(f'{key}: {expr.units}')
    

class ODEExpressions(ExpressionBlock):
    
    """Class for ODE expressions"""
    
    def __init__(self,
                 ode_exprs=None,
                 ):
        
        super().__init__(ode_exprs)
        self._title = 'ODE'
        
        
class AEExpressions(ExpressionBlock):
    
    """Class for AE expressions"""
    
    def __init__(self,
                 alg_exprs=None,
                 ):
        
        super().__init__(alg_exprs)
        self._title = 'ALG'

class Expression():
    
    """Class for individual expressions"""
    
    def __init__(self,
                 name,
                 expression):
        
        self.name = name
        self.expression = expression
        self.units = None
        self.expression_orig = None
        
    def __str__(self):
        
        return self.expression.to_string()
    
    @property
    def show_units(self):
        return self.units.to_string()
    
    def _change_to_unit(self, c_mod, c_mod_new):
        """Method to remove the fixed parameters from the ConcreteModel
        TODO: move to a new expression class
        """
        var_dict = c_mod_new.var_dict
        expr_new = self.expression
        if self.expression_orig is not None:
            expr_new = self.expression_orig
        for model_var, var_obj in var_dict.items():
            old_var = getattr(c_mod, model_var)
            new_var = getattr(c_mod_new, model_var)         
            expr_new = _update_expression(expr_new, old_var, new_var)
            
        return expr_new
    
    def _change_to_unit2(self, c_mod, c_mod_new):
        """Method to remove the fixed parameters from the ConcreteModel
        TODO: move to a new expression class
        """
        var_dict = c_mod_new.var_dict
        expr_new = self.expression
        if self.expression_orig is not None:
            expr_new = self.expression_orig    
        for model_var, var_obj in var_dict.items():
            old_var = c_mod[model_var]
            new_var = var_dict[model_var]         
            expr_new = _update_expression(expr_new, old_var, new_var)
            
        return expr_new

    """
    def change_time(self, expr_orig, c_mod, new_time, current_model):
           
            expr_new_time = expr_orig
            var_dict = c_mod
            
            for model_var, obj_list in var_dict.items():
                
                if not isinstance(obj_list[1].index(), int):
                    old_var = obj_list[1]
                    new_var = getattr(current_model, obj_list[0])[new_time, model_var]
            
                else:
                    old_var = obj_list[1]
                    new_var = getattr(current_model, obj_list[0])[model_var]
            
                expr_new_time = self._update_expression(expr_new_time, old_var, new_var)
        
            return expr_new_time
    """


    def check_units(self, c_mod, c_mod_new):
        """Check the expr units by exchanging the real model with unit model
        components
        
        Args:
            key (str): component represented in ODE
            
            expr (Expression): Expression object of ODE
            
            c_mod (Comp): original Comp object used to declare the expressions
            
            c_mod_new (Comp_Check): dummy model with unit components
            
        Returns:
            pint_units (): Returns expression with unit model components
        
        """
        expr = self._change_to_unit(c_mod, c_mod_new)
        self.units = u.get_units(expr)
        return None
    
    def check_units2(self, c_mod, c_mod_new):
        """Check the expr units by exchanging the real model with unit model
        components
        
        Args:
            key (str): component represented in ODE
            
            expr (Expression): Expression object of ODE
            
            c_mod (Comp): original Comp object used to declare the expressions
            
            c_mod_new (Comp_Check): dummy model with unit components
            
        Returns:
            pint_units (): Returns expression with unit model components
        
        """
        expr = self._change_to_unit2(c_mod, c_mod_new)
        self.units = u.get_units(expr)
        return None

    def check_division(self, eps=1e-12):
        """Add a small amount to the numerator and denominator in a
        DivisionExpression to improve the numerics
        
        """
        expr = self.expression
        
        if isinstance(expr, DivisionExpression):
        
            ex1, ex2 = expr.args
            ex1 += eps
            ex2 += eps
            expr_new = ex1/ex2
            
            self.expression = expr_new
            self.expression_orig = expr
    
        return None