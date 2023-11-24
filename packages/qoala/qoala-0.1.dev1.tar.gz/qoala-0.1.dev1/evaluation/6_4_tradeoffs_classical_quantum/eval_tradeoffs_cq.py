from __future__ import annotations

import json
import math
import os
import time
from argparse import ArgumentParser
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import netsquid as ns

from qoala.lang.parse import QoalaParser
from qoala.lang.program import QoalaProgram
from qoala.runtime.config import (
    ClassicalConnectionConfig,
    LatenciesConfig,
    NtfConfig,
    ProcNodeConfig,
    ProcNodeNetworkConfig,
    TopologyConfig,
)
from qoala.runtime.program import BatchResult, ProgramInput
from qoala.util.logging import LogManager
from qoala.util.runner import (
    SchedulerType,
    run_single_node_app,
    run_two_node_app_separate_inputs,
    run_two_node_app_separate_inputs_plus_constant_tasks,
)


def create_procnode_cfg(
    name: str, id: int, t1: float, t2: float, determ: bool, deadlines: bool, fcfs: bool
) -> ProcNodeConfig:
    return ProcNodeConfig(
        node_name=name,
        node_id=id,
        topology=TopologyConfig.uniform_t1t2_qubits_perfect_gates_default_params(
            5, t1, t2
        ),
        latencies=LatenciesConfig(qnos_instr_time=1000, host_instr_time=1000),
        ntf=NtfConfig.from_cls_name("GenericNtf"),
        determ_sched=determ,
        use_deadlines=deadlines,
        fcfs=fcfs,
    )


def load_program(path: str) -> QoalaProgram:
    path = os.path.join(os.path.dirname(__file__), path)
    with open(path) as file:
        text = file.read()
    return QoalaParser(text).parse()


@dataclass
class ProgResult:
    alice_results: BatchResult
    bob_results: BatchResult
    qpu_waits: List[float]
    total_duration: float


def run_apps(
    state: int,
    t1: float,
    t2: float,
    cc_latency: float,
    num_const_tasks: int,
    busy_duration: float,
    const_period: float,
    const_start: float,
    sched_typ: SchedulerType,
) -> ProgResult:
    ns.sim_reset()

    alice_id = 1
    bob_id = 0

    fcfs = sched_typ == SchedulerType.FCFS

    # Alice never uses FCFS!
    alice_node_cfg = create_procnode_cfg(
        "alice", alice_id, t1, t2, determ=True, deadlines=True, fcfs=False
    )
    bob_node_cfg = create_procnode_cfg(
        "bob", bob_id, t1, t2, determ=True, deadlines=True, fcfs=fcfs
    )

    cconn = ClassicalConnectionConfig.from_nodes(alice_id, bob_id, cc_latency)
    network_cfg = ProcNodeNetworkConfig.from_nodes_perfect_links(
        nodes=[alice_node_cfg, bob_node_cfg], link_duration=1000
    )
    network_cfg.cconns = [cconn]

    alice_program = load_program("programs/controller.iqoala")
    bob_program = load_program("programs/interactive_quantum.iqoala")
    busy_program = load_program("programs/cpu_busy.iqoala")

    alice_inputs = [ProgramInput({"bob_id": bob_id})]

    def measure_state(prepare_state: int) -> int:
        return {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}[prepare_state]

    bob_inputs = [
        ProgramInput(
            {
                "alice_id": alice_id,
                "prepare_state": state,
                "measure_state": measure_state(state),
            },
        )
    ]

    busy_inputs = [
        ProgramInput({"duration": busy_duration}) for _ in range(num_const_tasks)
    ]

    if sched_typ == SchedulerType.QOALA or sched_typ == SchedulerType.FCFS:
        app_result = run_two_node_app_separate_inputs_plus_constant_tasks(
            num_iterations=1,
            num_const_tasks=num_const_tasks,
            node1="alice",
            node2="bob",
            prog_node1=alice_program,
            prog_node1_inputs=alice_inputs,
            prog_node2=bob_program,
            prog_node2_inputs=bob_inputs,
            const_prog_node2=busy_program,
            const_prog_node2_inputs=busy_inputs,
            const_period=int(const_period),
            const_start=int(const_start),
            network_cfg=network_cfg,
            sched_typ=sched_typ,
            linear=True,
        )
        alice_result = app_result.batch_results["alice"]
        bob_result = app_result.batch_results["bob"]

        return ProgResult(alice_result, bob_result, [], app_result.total_duration)
    else:
        app_result_quantum = run_two_node_app_separate_inputs(
            num_iterations=1,
            programs={"alice": alice_program, "bob": bob_program},
            program_inputs={"alice": alice_inputs, "bob": bob_inputs},
            network_cfg=network_cfg,
            linear=True,
        )
        app_result_classical = run_single_node_app(
            num_iterations=num_const_tasks,
            program_name="bob",
            program=busy_program,
            program_input=ProgramInput({"duration": busy_duration}),
            network_cfg=network_cfg,
            linear=True,
        )
        alice_result = app_result_quantum.batch_results["alice"]
        bob_result = app_result_quantum.batch_results["bob"]

        total_duration = (
            app_result_classical.total_duration + app_result_quantum.total_duration
        )

        return ProgResult(alice_result, bob_result, [], total_duration)


@dataclass
class DataPoint:
    sched_typ: str
    busy_factor: float
    busy_duration: float
    succ_prob: float
    succ_prob_lower: float
    succ_prob_upper: float
    makespan: float


@dataclass
class DataMeta:
    timestamp: str
    sim_duration: float
    num_iterations: int
    t1: float
    t2: float
    latency_factor: float
    num_const_tasks: int
    const_rate_factor: float
    cc_latency: float
    const_period: float
    const_start: float
    busy_factors: List[float]


@dataclass
class Data:
    meta: DataMeta
    data_points: List[DataPoint]


def relative_to_cwd(file: str) -> str:
    return os.path.join(os.path.dirname(__file__), file)


def wilson_score_interval(p_hat, n, z):
    denominator = 1 + z**2 / n
    centre_adjusted_probability = p_hat + z**2 / (2 * n)
    adjusted_standard_deviation = z * math.sqrt(
        (p_hat * (1 - p_hat) + z**2 / (4 * n)) / n
    )

    lower_bound = (
        centre_adjusted_probability - adjusted_standard_deviation
    ) / denominator
    upper_bound = (
        centre_adjusted_probability + adjusted_standard_deviation
    ) / denominator

    return (lower_bound, upper_bound)


def get_datapoint(
    num_iterations: int,
    t1: float,
    t2: float,
    cc_latency: float,
    num_const_tasks: int,
    const_period: float,
    const_start: float,
    sched_typ: SchedulerType,
    busy_factor: float,
) -> DataPoint:
    successes: List[bool] = []
    makespans: List[float] = []

    busy_duration = busy_factor * cc_latency

    for i in range(num_iterations):
        result = run_apps(
            state=i % 6,
            t1=t1,
            t2=t2,
            cc_latency=cc_latency,
            num_const_tasks=num_const_tasks,
            busy_duration=busy_duration,
            const_period=const_period,
            const_start=const_start,
            sched_typ=sched_typ,
        )
        program_results = result.bob_results.results
        outcomes = [result.values["outcome"] for result in program_results]
        assert len(outcomes) == 1
        successes.append(outcomes[0] == 1)
        makespans.append(result.total_duration)

    avg_succ_prob = sum([s for s in successes if s]) / len(successes)
    succ_prob_lower, succ_prob_upper = wilson_score_interval(
        p_hat=avg_succ_prob, n=len(successes), z=1.96
    )

    total_makespan = sum(makespans)

    return DataPoint(
        sched_typ=sched_typ.name,
        busy_factor=busy_factor,
        busy_duration=busy_duration,
        succ_prob=avg_succ_prob,
        succ_prob_lower=succ_prob_lower,
        succ_prob_upper=succ_prob_upper,
        makespan=total_makespan,
    )


def run(
    output_dir: str,
    sched_typ: SchedulerType,
    num_iterations: int,
    dump: bool = True,
    log: bool = False,
):
    if log:
        LogManager.set_log_level("DEBUG")
        LogManager.log_to_file("classical_multitasking_2.log")
        LogManager.set_task_log_level("DEBUG")
        LogManager.log_tasks_to_file("classical_multitasking_tasks_2.log")

    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # print(timestamp)

    data_points: List[DataPoint] = []

    # Constants
    t1 = 1e10
    t2 = 1e8
    latency_factor = 0.1
    num_const_tasks = 100
    const_rate_factor = 10

    cc_latency = latency_factor * t2
    const_period = cc_latency / const_rate_factor
    const_start = cc_latency

    # Variables
    busy_factors = [
        # 0.05,
        0.1,
        0.15,
        0.2,
        0.3,
        0.5,
        1,
        2,
        5,
        10,
    ]  # fraction of cc_latency
    # busy_factors = [0.5]
    # busy_factors = [0.1]

    for i, busy_factor in enumerate(busy_factors):
        print(
            f"{sched_typ:30}: data point {i}/{len(busy_factors)}", end="\r", flush=True
        )
        data_point = get_datapoint(
            num_iterations=num_iterations,
            t1=t1,
            t2=t2,
            cc_latency=cc_latency,
            num_const_tasks=num_const_tasks,
            const_period=const_period,
            const_start=const_start,
            sched_typ=sched_typ,
            busy_factor=busy_factor,
        )

        data_points.append(data_point)

    end_time = time.time()
    sim_duration = end_time - start_time

    meta = DataMeta(
        timestamp=timestamp,
        sim_duration=sim_duration,
        num_iterations=num_iterations,
        t1=t1,
        t2=t2,
        latency_factor=latency_factor,
        num_const_tasks=num_const_tasks,
        const_rate_factor=const_rate_factor,
        cc_latency=cc_latency,
        const_period=const_period,
        const_start=const_start,
        busy_factors=busy_factors,
    )

    if dump:
        data = Data(meta=meta, data_points=data_points)

        json_data = asdict(data)

        abs_dir = relative_to_cwd(f"data/{output_dir}")
        Path(abs_dir).mkdir(parents=True, exist_ok=True)
        last_path = os.path.join(abs_dir, "LAST.json")
        timestamp_path = os.path.join(abs_dir, f"{timestamp}.json")
        with open(last_path, "w") as datafile:
            json.dump(json_data, datafile)
        with open(timestamp_path, "w") as datafile:
            json.dump(json_data, datafile)

        print(f"data written to {timestamp_path} and {last_path}", end="\r", flush=True)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--scheduler",
        "-s",
        type=str,
        choices=["no_sched", "fcfs", "qoala"],
        required=True,
    )
    parser.add_argument("--num_iterations", "-n", type=int, required=True)
    parser.add_argument("--dump", "-d", action="store_true")
    parser.add_argument("--log", "-l", action="store_true")

    args = parser.parse_args()

    num_iterations = args.num_iterations
    dump = args.dump
    log = args.log

    if args.scheduler == "no_sched":
        run(
            output_dir="no_sched",
            sched_typ=SchedulerType.NO_SCHED,
            num_iterations=num_iterations,
            dump=dump,
            log=log,
        )
    elif args.scheduler == "fcfs":
        run(
            output_dir="fcfs",
            sched_typ=SchedulerType.FCFS,
            num_iterations=num_iterations,
            dump=dump,
            log=log,
        )
    elif args.scheduler == "qoala":
        run(
            output_dir="qoala",
            sched_typ=SchedulerType.QOALA,
            num_iterations=num_iterations,
            dump=dump,
            log=log,
        )
