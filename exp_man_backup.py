from modules.kubernetes_cluster import KubernetesCluster
from modules.workload_experiment import WorkloadExperiment
from time import time

def main():
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFabnJBcXBxcngyTVFmOFVZVGdyOURRSzQ1a3d0TFpuTkdMRGZmelpxT3cifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcGktc2xpY2luZyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhcGktc2xpY2luZy1zZWNyZXQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYXBpLXNsaWNpbmctc3ZjIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNzQ3Y2U3NTYtNzIwNC00YTY4LWIzNmEtZWYxYjA4YTFkYmRkIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFwaS1zbGljaW5nOmFwaS1zbGljaW5nLXN2YyJ9.uG9bWigz0mRotO_zSvFzdA7b_Whyj2x9wwBC3CUYjzKD8aXOcdDO1XE4pF-w4TzTSWAGvbM-x_n3kX5zC1UQvvvZOJlbIywKo8yLy8VX9E3f7GaiD_MAxhIsSif9ckzPWBNVGcOWf7SZq6LDRJ_kBL8LBU2KwgjwopOmQtgEErcu7VUyB9S-ElAp5opXl83BUkhc9r2_q3rj-j-jMrVEHTM6qKIXY_U6cDd3ZeCp2DRLZj2WxzECd7gBNzKxpRvkl5SwOZ7nSUPmAGhV1UXqZ4grFEgSLmXiHworbcJtJtQ0EQtsC1_DGuz0vwdwGD6WCvtT4jPsJejZ0yvS8GKgdw"
    sfi2_cluster = KubernetesCluster(auth_token)
    constant_load = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="constant-load-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/test1_hamperer:1.1.5",
    )
    vnfsim1 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim1-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim2 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim2-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim3 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim3-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim4 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim4-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim5 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim5-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim6 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim6-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim7 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim7-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim8 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim8-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim9 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim9-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim10 = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim10-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim11= WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim11-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim12= WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim12-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim13= WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim13-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim14= WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim14-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )
    vnfsim15= WorkloadExperiment(
        cluster=sfi2_cluster,
        name="vnfsim15-w1",
        namespace="api-slicing",
        node="worker1",
        image="eduardogomescampos/load_test:1.1.5",
    )

    experiment_list = [[constant_load],[constant_load, vnfsim1],[constant_load,vnfsim1,vnfsim2],[constant_load,vnfsim1,vnfsim2,vnfsim3],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim7],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim7,vnfsim8],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim7,vnfsim8,vnfsim9],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim8,vnfsim7,vnfsim9,vnfsim10],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim8,vnfsim7,vnfsim9,vnfsim10,vnfsim11],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim8,vnfsim7,vnfsim9,vnfsim10,vnfsim11,vnfsim12],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim8,vnfsim7,vnfsim9,vnfsim10,vnfsim11,vnfsim12,vnfsim13],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim8,vnfsim7,vnfsim9,vnfsim10,vnfsim11,vnfsim12,vnfsim13,vnfsim14],[constant_load,vnfsim1,vnfsim2,vnfsim3,vnfsim4,vnfsim5,vnfsim6,vnfsim8,vnfsim7,vnfsim9,vnfsim10,vnfsim11,vnfsim12,vnfsim13,vnfsim14,vnfsim15]]
    print("Starting experiment")
    for i in range(10):
        for experiment_part in experiment_list:
            for experiment in experiment_part:
                experiment.start()
            for experiment in experiment_part:
                experiment.get_results()
        print(f"Finished execution number {i + 1}")
    print("Finishing experiment")
if __name__ == "__main__":
    main()
