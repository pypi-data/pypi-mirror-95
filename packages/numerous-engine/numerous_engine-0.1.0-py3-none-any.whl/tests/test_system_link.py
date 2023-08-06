import pytest
from pytest import approx

from numerous.engine.system import Subsystem, Item
from numerous.multiphysics import EquationBase, Equation
from numerous.engine.model import Model
from numerous.engine.simulation import Simulation
import numpy as np

from numerous.engine.simulation.solvers.base_solver import solver_types

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    import shutil
    shutil.rmtree('./tmp', ignore_errors=True)
    yield


class InitialValue(Item, EquationBase):
    def __init__(self, tag='initialvalue', x0=1):
        super(InitialValue, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_constant('x', x0)
        self.t1.add_equations([self])


class Root(Subsystem):
    def __init__(self, tag='root_linktest', N_outer=2, N_inner=5, k=0.9):
        super().__init__(tag)
        inlet_item = InitialValue(x0=1)
        for i in range(N_outer):
            system = Level1(tag='linkersubsystem_' + str(i), inlet_item=inlet_item, N=N_inner, k=k)
            self.register_item(system)
            inlet_item = system.ports['outlet']  # Set next inlet item to outlet item from Level1 - this does not work


class Level1(Subsystem):
    def __init__(self, tag='level1', N=2, k=0.9, inlet_item=object):
        super(Level1, self).__init__(tag)

        items = []

        for i in range(N):
            item = Base(tag='item_' + str(i), inlet=inlet_item, k=k)
            self.register_item(item)
            inlet_item = item  # This works

        self.add_port("outlet", item)
        # self.outlet = item  # Add outlet item as last item in Level1 subsystem


class Base(Subsystem, EquationBase):
    def __init__(self, tag='level2', inlet=object, k=0.9):
        super(Base, self).__init__(tag)
        self.t1 = self.create_namespace('t1')
        self.add_parameter('x', 0)
        self.add_parameter('x0', 0)
        self.add_constant('k', k)
        self.t1.add_equations([self])
        self.register_items([inlet])

        # Bind

        self.t1.x0 = inlet.t1.x

    @Equation()
    def eval(self, scope):
        scope.x = scope.x0 * scope.k


def expected(length, N, k):
    return (k ** N) * np.ones(length)


@pytest.fixture
def system15():
    return Root(N_outer=5, N_inner=1)


@pytest.fixture
def system51():
    return Root(N_outer=1, N_inner=5)

@pytest.mark.parametrize("solver", solver_types)
@pytest.mark.parametrize("use_llvm", [True, False])
def test_system_link_1_5(system15, solver,use_llvm):
    model = Model(system15,use_llvm=use_llvm)

    sim = Simulation(model, t_start=0, t_stop=100, num=200, solver_type=solver)

    sim.solve()
    df = sim.model.historian_df

    assert approx(np.array(df['root_linktest.linkersubsystem_4.item_0.t1.x'])[1:]) == \
           expected(len(df.index[:-1]), 5, 0.9)

@pytest.mark.parametrize("solver", solver_types)
@pytest.mark.parametrize("use_llvm", [True, False])
def test_system_link_5_1(system51, solver,use_llvm):
    model = Model(system51,use_llvm=use_llvm)

    sim = Simulation(model, t_start=0, t_stop=100, num=200, solver_type=solver)

    sim.solve()
    df = sim.model.historian_df

    assert approx(np.array(df['root_linktest.linkersubsystem_0.item_4.t1.x'])[1:]) == \
           expected(len(df.index[:-1]), 5, 0.9)
