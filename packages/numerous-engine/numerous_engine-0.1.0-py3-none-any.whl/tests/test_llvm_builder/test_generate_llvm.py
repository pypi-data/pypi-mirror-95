import pytest
from numba import carray
from pytest import approx

from numerous.engine.model.lowering.llvm_builder import LLVMBuilder
import numpy as np
import os

initial_values = np.arange(1, 10)
filename = 'llvm_IR_code.txt'


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    if os.path.exists(filename):
        os.remove(filename)


eval_llvm_signature = 'void(float64, float64, CPointer(float64), CPointer(float64))'


def eval_llvm(s_x1, s_x2, s_x2_dot, s_x3_dot):
    carray(s_x2_dot, (1,))[0] = -100 if s_x1 > s_x2 else 50
    carray(s_x3_dot, (1,))[0] = -carray(s_x2_dot, (1,))[0]


eval_llvm_mix_signature = 'void(float64, CPointer(float64),float64, CPointer(float64))'


def eval_llvm_mix(s_x1, s_x2_dot, s_x2, s_x3_dot):
    carray(s_x2_dot, (1,))[0] = -100 if s_x1 > s_x2 else 50
    carray(s_x3_dot, (1,))[0] = -carray(s_x2_dot, (1,))[0]


number_of_derivatives = 3
number_of_states = 3

variable_names = {
    "oscillator1.mechanics.x": 0,
    "oscillator1.mechanics.y": 1,
    "oscillator1.mechanics.z": 2,
    "oscillator1.mechanics.a": 3,
    "oscillator1.mechanics.b": 4,
    "oscillator1.mechanics.c": 5,
    "oscillator1.mechanics.x_dot": 6,
    "oscillator1.mechanics.y_dot": 7,
    "oscillator1.mechanics.z_dot": 8,
}

variable_distributed = {
    "oscillator1.mechanics.a": 0,
    "oscillator1.mechanics.x_dot": 1,
    "oscillator1.mechanics.y_dot": 2,
    "oscillator1.mechanics.z_dot": 3,
    "oscillator1.mechanics.x": 4,
    "oscillator1.mechanics.b": 5,
    "oscillator1.mechanics.c": 6,
    "oscillator1.mechanics.y": 7,
    "oscillator1.mechanics.z": 8,
}
DERIVATIVES = ["oscillator1.mechanics.x_dot", "oscillator1.mechanics.y_dot", "oscillator1.mechanics.z_dot"]
STATES = ["oscillator1.mechanics.x", "oscillator1.mechanics.y", "oscillator1.mechanics.z"]


def test_llvm_1_to_1_mapping_state():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)

    llvm_program.add_mapping(["oscillator1.mechanics.x"], ["oscillator1.mechanics.x_dot"])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([2.1, 8, 9.])


def test_llvm_1_to_1_mapping_parameter():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)

    llvm_program.add_mapping(["oscillator1.mechanics.b"], ["oscillator1.mechanics.x_dot"])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([5, 8, 9.])


def test_llvm_n_to_1_sum_mapping():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)

    llvm_program.add_mapping(["oscillator1.mechanics.x", "oscillator1.mechanics.y", "oscillator1.mechanics.b"],
                             ["oscillator1.mechanics.x_dot"])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([9.3, 8, 9.])


def test_llvm_1_to_n_mapping():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)

    llvm_program.add_mapping(["oscillator1.mechanics.x"],
                             ["oscillator1.mechanics.x_dot", "oscillator1.mechanics.y_dot"])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([2.1, 2.1, 9.])


def test_llvm_1_function():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])

    llvm_program.add_call(eval_llvm.__qualname__,
                          ["oscillator1.mechanics.x", "oscillator1.mechanics.y", "oscillator1.mechanics.x_dot",
                           "oscillator1.mechanics.y_dot"],
                          target_ids=[2, 3])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([50, -50, 9.])
    assert approx(diff(np.array([2.3, 2.2, 2.1]))) == np.array([-100, 100, 9.])


def test_llvm_1_function_and_mapping():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])

    llvm_program.add_call(eval_llvm.__qualname__,
                          ["oscillator1.mechanics.x", "oscillator1.mechanics.y",
                           "oscillator1.mechanics.a", "oscillator1.mechanics.y_dot"], target_ids=[2, 3])

    llvm_program.add_mapping(args=["oscillator1.mechanics.a"],
                             targets=["oscillator1.mechanics.x_dot"])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([50, -50, 9.])
    assert approx(diff(np.array([2.3, 2.2, 2.1]))) == np.array([-100, 100, 9.])

def test_llvm_unordered_vars():
    llvm_program = LLVMBuilder(initial_values, variable_distributed, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])
    diff, var_func, _ = llvm_program.generate(filename)
    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([2., 3., 4.])
    assert approx(var_func()) == np.array([1., 2., 3., 4., 2.1, 6., 7., 2.2, 2.3])


def test_llvm_1_function_and_mapping_unordered_vars():
    llvm_program = LLVMBuilder(initial_values, variable_distributed, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])

    llvm_program.add_call(eval_llvm.__qualname__,
                          ["oscillator1.mechanics.x", "oscillator1.mechanics.y",
                           "oscillator1.mechanics.a", "oscillator1.mechanics.y_dot"], target_ids=[2, 3])

    llvm_program.add_mapping(args=["oscillator1.mechanics.a"],
                             targets=["oscillator1.mechanics.x_dot"])

    diff, var_func, _ = llvm_program.generate(filename)
    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([50., -50., 4.])
    assert approx(diff(np.array([2.3, 2.2, 2.1]))) == np.array([-100, 100, 4.])


def test_llvm_1_function_and_mappings():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])

    llvm_program.add_mapping(args=["oscillator1.mechanics.x"],
                             targets=["oscillator1.mechanics.b"])

    llvm_program.add_call(eval_llvm.__qualname__, ["oscillator1.mechanics.b", "oscillator1.mechanics.y",
                                                   "oscillator1.mechanics.a", "oscillator1.mechanics.y_dot"],
                          target_ids=[2, 3])

    llvm_program.add_mapping(args=["oscillator1.mechanics.a"],
                             targets=["oscillator1.mechanics.b"])

    llvm_program.add_call(eval_llvm.__qualname__, ["oscillator1.mechanics.b", "oscillator1.mechanics.y",
                                                   "oscillator1.mechanics.a", "oscillator1.mechanics.y_dot"],
                          target_ids=[2, 3])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([7., 100., 9.])

    assert approx(var_func()) == np.array([2.1, 2.2, 2.3, -100., 50., 6., 7., 100., 9.])


def test_llvm_2_function_and_mappings():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])

    llvm_program.add_call(eval_llvm.__qualname__, ["oscillator1.mechanics.b", "oscillator1.mechanics.y",
                                                   "oscillator1.mechanics.a", "oscillator1.mechanics.y_dot"],
                          target_ids=[2, 3])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.1, 2.2, 2.3]))) == np.array([7., 100., 9.])

    assert approx(var_func()) == np.array([2.1, 2.2, 2.3, -100., 5., 6., 7., 100., 9.])


def test_llvm_loop_seq():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm, eval_llvm_signature, number_of_args=4, target_ids=[2, 3])

    llvm_program.add_set_call(eval_llvm.__qualname__, [
        ["oscillator1.mechanics.y", "oscillator1.mechanics.z", "oscillator1.mechanics.a", "oscillator1.mechanics.b"],
        ["oscillator1.mechanics.c", "oscillator1.mechanics.x_dot", "oscillator1.mechanics.y_dot",
         "oscillator1.mechanics.z_dot"]],
                              targets_ids=[2, 3])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.6, 2.2, 2.3]))) == np.array([7, 50., -50])
    ##Note that state is not changed. States can only be changed by the solver
    assert approx(var_func()) == np.array([2.6, 2.2, 2.3, 50, -50., 6., 7., 50., -50.])


def test_llvm_loop_mix():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_external_function(eval_llvm_mix, eval_llvm_mix_signature, number_of_args=4, target_ids=[1, 3])

    llvm_program.add_set_call(eval_llvm_mix.__qualname__, [
        ["oscillator1.mechanics.y", "oscillator1.mechanics.z", "oscillator1.mechanics.a", "oscillator1.mechanics.b"],
        ["oscillator1.mechanics.c", "oscillator1.mechanics.x_dot", "oscillator1.mechanics.y_dot",
         "oscillator1.mechanics.z_dot"]],
                              targets_ids=[1, 3])

    diff, var_func, _ = llvm_program.generate(filename)

    assert approx(diff(np.array([2.6, 2.2, 2.3]))) == np.array([50, 8, -50])

    assert approx(var_func()) == np.array([2.6, 2.2, 2.3, 4, -50., 6., 50, 8., -50.])


def test_llvm_idx_write():
    llvm_program = LLVMBuilder(initial_values, variable_names, STATES, DERIVATIVES)
    llvm_program.add_mapping(["oscillator1.mechanics.b"],
                             ["oscillator1.mechanics.x_dot", "oscillator1.mechanics.y_dot"])
    diff, var_func, var_write = llvm_program.generate(filename)

    var_write(100, 4)

    assert approx(var_func()) == np.array([1.0, 2.0, 3.0, 4., 100., 6., 7., 8., 9.])
    assert approx(diff(np.array([2.6, 2.2, 2.3]))) == np.array([100, 100., 9.])
