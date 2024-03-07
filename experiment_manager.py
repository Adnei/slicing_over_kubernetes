from modules.kubernetes_cluster import KubernetesCluster
from modules.workload_experiment import WorkloadExperiment
from time import time

def main():
    auth_token "<>"
    sfi2_cluster = KubernetesCluster(auth_token)
    constant_load = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="constant-load",
        namespace="api-slicing",
        node="worker2",
        image="eduardogomescampos/test1_hamperer:1.1.4",
    )
    first_load = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="first-load",
        namespace="api-slicing",
        node="worker2",
        image="eduardogomescampos/test1_regular:1.4.0",
    )
    second_load = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="second-load",
        namespace="api-slicing",
        node="worker2",
        image="eduardogomescampos/test1_regular:1.4.1",
    )
    third_load = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="third-load",
        namespace="api-slicing",
        node="worker2",
        image="eduardogomescampos/test1_regular:1.4.2",
    )
    experiment_list = [[constant_load, first_load],[constant_load],[constant_load, third_load]]
    print("Starting experiment")
    for i in range(10):
        for experiment_part in experiment_list:
            for experiment in experiment_part:
                experiment.start()
            for experiment in experiment_part:
                experiment.get_results()
        print(f"Finished execution number {i}")
    print("Finishing experiment")
if __name__ == "__main__":
    main()
