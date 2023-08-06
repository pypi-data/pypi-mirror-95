import pytest
from pytest import approx

from numerous.engine.model import Model
from numerous.engine.simulation import Simulation

from numerous.engine.system import Subsystem, ConnectorItem, Item, ConnectorTwoWay
from numerous import EquationBase, OutputFilter, Equation
from tests.test_equations import TestEq_ground, Test_Eq, TestEq_input


@pytest.fixture
def test_eq1():
    class TestEq1(EquationBase):
        def __init__(self, P=10):
            super().__init__(tag='example_1')
            self.add_parameter('P', P)
            self.add_state('T1', 0)
            self.add_state('T2', 0)
            self.add_state('T3', 0)
            self.add_state('T4', 0)
            self.add_parameter('T_4', 0)
            self.add_constant('TG', 10)
            self.add_constant('R1', 10)
            self.add_constant('R2', 5)
            self.add_constant('R3', 3)
            self.add_constant('RG', 2)

        @Equation()
        def eval(self,scope):
            scope.T1_dot = scope.P - (scope.T1 - scope.T2) / scope.R1
            scope.T2_dot = (scope.T1 - scope.T2) / scope.R1 - (scope.T2 - scope.T3) / scope.R2
            scope.T3_dot = (scope.T2 - scope.T3) / scope.R2 - (scope.T3 - scope.T4) / scope.R3
            scope.T4_dot = (scope.T3 - scope.T4) / scope.R3 - (scope.T4 - scope.TG) / scope.RG


    return TestEq1(P=100)


@pytest.fixture
def simple_item(test_eq1):
    class T1(Item):
        def __init__(self, tag):
            super().__init__(tag)

            t1 = self.create_namespace('t1')

            t1.add_equations([test_eq1])

    return T1('test_item')


@pytest.fixture
def ms1(simple_item):
    class S1(Subsystem):
        def __init__(self, tag):
            super().__init__(tag)
            self.register_items([simple_item])

    return S1('S1_nm')


@pytest.fixture
def ms2():
    class I(Item, EquationBase):
        def __init__(self, tag, P, T, R):
            super().__init__(tag)
            self.t1 = self.create_namespace('t1')
            self.add_parameter('P', P)
            self.add_parameter('T_o', 0)
            self.add_state('T', T)
            self.add_constant('R', R)
            self.t1.add_equations([self])


        @Equation()
        def eval(self, scope):
            scope.T_dot = scope.P - (scope.T - scope.T_o) / scope.R

    class T(Item):
        def __init__(self, tag, T, R):
            super().__init__(tag)

            t1 = self.create_namespace('t1')
            t1.add_equations([Test_Eq(T=T, R=R)])

    class G(Item):
        def __init__(self, tag, TG, RG):
            super().__init__(tag)

            t1 = self.create_namespace('t1')
            t1.add_equations([TestEq_ground(TG=TG, RG=RG)])

    class S2(Subsystem):
        def __init__(self, tag):
            super().__init__(tag)

            input = I('1', P=100, T=0, R=10)
            item1 = T('2', T=0, R=5)
            item2 = T('3', T=0, R=3)
            item3 = T('4', T=0, R=2)
            ## RG is redundant we use item3.R as a last value of R in a chain
            ground = G('5', TG=10, RG=2)

            input.t1.T_o.add_mapping(item1.t1.T)

            # item1.bind(input=input, output=item2)

            item1.t1.R_i.add_mapping(input.t1.R)
            item1.t1.T_i.add_mapping(input.t1.T)
            item1.t1.T_o.add_mapping(item2.t1.T)
            #  t_0 = item1.t1.T_o
            # item1.t1.T_o = item2.t1.T

            item2.t1.R_i.add_mapping(item1.t1.R)
            item2.t1.T_i.add_mapping(item1.t1.T)
            item2.t1.T_o.add_mapping(item3.t1.T)

            item3.t1.R_i.add_mapping(item2.t1.R)
            item3.t1.T_i.add_mapping(item2.t1.T)
            item3.t1.T_o.add_mapping(ground.t1.T)

            self.register_items([input, item1, item2, item3, ground])

    return S2('S2_nm')

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    import shutil
    shutil.rmtree('./tmp', ignore_errors=True)
    yield



@pytest.fixture
def ms3():
    class I(ConnectorItem):
        def __init__(self, tag, P, T, R):
            super(I, self).__init__(tag)

            self.create_binding('output')

            t1 = self.create_namespace('t1')

            t1.add_equations([TestEq_input(P=P, T=T, R=R)])
            ##this line has to be after t1.add_equations since t1 inside output is created there
            self.output.t1.create_variable(name='T')
            t1.T_o = self.output.t1.T

    class T(ConnectorTwoWay):
        def __init__(self, tag, T, R):
            super().__init__(tag, side1_name='input', side2_name='output')

            t1 = self.create_namespace('t1')
            t1.add_equations([Test_Eq(T=T, R=R)])

            t1.R_i = self.input.t1.R
            t1.T_i = self.input.t1.T

            ##we ask for variable T
            t1.T_o = self.output.t1.T

    class G(Item):
        def __init__(self, tag, TG, RG):
            super().__init__(tag)

            t1 = self.create_namespace('t1')
            t1.add_equations([TestEq_ground(TG=TG, RG=RG)])


    class S3(Subsystem):
        def __init__(self, tag):
            super().__init__(tag)

            input = I('1', P=100, T=0, R=10)
            item1 = T('2', T=0, R=5)
            item2 = T('3', T=0, R=3)
            item3 = T('4', T=0, R=2)
            ground = G('5', TG=10, RG=2)

            input.bind(output=item1)

            item1.bind(input=input, output=item2)

            item2.bind(input=item1, output=item3)
            item3.bind(input=item2, output=ground)

            self.register_items([input, item1, item2, item3, ground])

    return S3('S3_nm')


def test_model_without_update(ms3):
    m1 = Model(ms3)
    n_m = m1.generate_compiled_model(0, 1)
    assert n_m.path_variables["S3_nm.1.t1.R"] == 10
    assert n_m.path_variables["S3_nm.2.t1.R"] == 5
    assert n_m.path_variables["S3_nm.3.t1.R"] == 3
    assert n_m.path_variables["S3_nm.4.t1.R"] == 2

@pytest.mark.skip(reason="Functionality not implemented in current version")
def test_model_with_update(ms3):
    m1 = Model(ms3)
    n_m = m1.generate_numba_model(0, 1)
    n_m.run_callbacks_with_updates(0.1)
    assert n_m.path_variables["S3_nm.1.t1.R"] == 10
    assert n_m.path_variables["S3_nm.2.t1.R"] == 5
    assert n_m.path_variables["S3_nm.3.t1.R"] == 3
    assert n_m.path_variables["S3_nm.4.t1.R"] == 2


