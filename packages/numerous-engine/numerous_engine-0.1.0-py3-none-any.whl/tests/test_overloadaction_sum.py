from numerous.engine.system import Item, Subsystem
from numerous.multiphysics import EquationBase, Equation
from numerous.engine.model import Model
from numerous.engine.simulation import Simulation
import numpy as np
import pytest
from pytest import approx

from numerous.engine.simulation.solvers.base_solver import solver_types

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    import shutil
    shutil.rmtree('./tmp', ignore_errors=True)
    yield



class Item1(Item, EquationBase):
    def __init__(self, tag='item1'):
        super(Item1, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_state('x', 1)
        self.add_state('t', 0)
        self.t1.add_equations([self])

    @Equation()
    def eval(self, scope):
        scope.t_dot = 1
        scope.x_dot = -1 * np.exp(-1 * scope.t)



class Subsystem1(Subsystem, EquationBase):
    def __init__(self, tag='subsystem1', item1=object):
        super(Subsystem1, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_parameter('x_dot_mod', 0)
        self.add_parameter('x_2_dot_mod', 0)
        self.t1.add_equations([self])
        self.register_items([item1])

        item1.t1.x_dot += self.t1.x_dot_mod

    @Equation()
    def eval(self, scope):
        scope.x_dot_mod = -1


class Item2(Item, EquationBase):
    def __init__(self, tag='item1'):
        super(Item2, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_state('x', 1)
        self.add_state('x_2', 1)
        self.add_state('t', 0)
        self.t1.add_equations([self])

    @Equation()
    def eval(self, scope):
        scope.t_dot = 1
        scope.x_dot = -1 * np.exp(-1 * scope.t)
        scope.x_2_dot = -1 * np.exp(-1 * scope.t)


class Subsystem2(Subsystem, EquationBase):
    def __init__(self, tag='subsystem1', item1=object):
        super(Subsystem2, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_parameter('x_dot_mod', 0)
        self.add_parameter('x_2_dot_mod', 0)
        self.t1.add_equations([self])
        self.register_items([item1])

        item1.t1.x_dot += self.t1.x_dot_mod

        item1.t1.x_dot += self.t1.x_2_dot_mod

    @Equation()
    def eval(self, scope):
        scope.x_dot_mod = 0
        scope.x_2_dot_mod = -1

class System(Subsystem, EquationBase):
    def __init__(self, tag='system_overload', subsystem=object):
        super(System, self).__init__(tag)

        self.register_items([subsystem])

@pytest.fixture
def system1():
    return System(tag='system1_overload',subsystem=Subsystem1(item1=Item1()))

@pytest.fixture
def system2():
    return System(tag='system2_overload',subsystem=Subsystem2(item1=Item2()))

def expected_sol(t):
    return -1*(t*np.exp(t) -1)*np.exp(-t)

@pytest.mark.parametrize("solver", solver_types)
@pytest.mark.parametrize("use_llvm", [True,False])
def test_overloadaction_sum(system1, solver, use_llvm):
    model = Model(system1,use_llvm=use_llvm)
    sim = Simulation(model, t_start=0, t_stop=10, num=100, solver_type = solver)
    sim.solve()
    df = sim.model.historian_df
    assert approx(np.array(df['system1_overload.subsystem1.item1.t1.x'])) == expected_sol(np.linspace(0, 10, 101))

@pytest.mark.parametrize("solver", solver_types)
@pytest.mark.parametrize("use_llvm", [True, False])
def test_overloadaction_sum_multiple(system2, solver, use_llvm):
    model = Model(system2, use_llvm=use_llvm)
    sim = Simulation(model, t_start=0, t_stop=10, num=100, solver_type = solver)
    sim.solve()
    df = sim.model.historian_df
    assert approx(np.array(df['system2_overload.subsystem1.item1.t1.x'])) == expected_sol(np.linspace(0, 10, 101))