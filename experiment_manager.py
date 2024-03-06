from modules.kubernetes_cluster import KubernetesCluster
from modules.workload_experiment import WorkloadExperiment
from time import time

def main():
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFabnJBcXBxcngyTVFmOFVZVGdyOURRSzQ1a3d0TFpuTkdMRGZmelpxT3cifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcGktc2xpY2luZyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhcGktc2xpY2luZy1zZWNyZXQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYXBpLXNsaWNpbmctc3ZjIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNzQ3Y2U3NTYtNzIwNC00YTY4LWIzNmEtZWYxYjA4YTFkYmRkIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFwaS1zbGljaW5nOmFwaS1zbGljaW5nLXN2YyJ9.uG9bWigz0mRotO_zSvFzdA7b_Whyj2x9wwBC3CUYjzKD8aXOcdDO1XE4pF-w4TzTSWAGvbM-x_n3kX5zC1UQvvvZOJlbIywKo8yLy8VX9E3f7GaiD_MAxhIsSif9ckzPWBNVGcOWf7SZq6LDRJ_kBL8LBU2KwgjwopOmQtgEErcu7VUyB9S-ElAp5opXl83BUkhc9r2_q3rj-j-jMrVEHTM6qKIXY_U6cDd3ZeCp2DRLZj2WxzECd7gBNzKxpRvkl5SwOZ7nSUPmAGhV1UXqZ4grFEgSLmXiHworbcJtJtQ0EQtsC1_DGuz0vwdwGD6WCvtT4jPsJejZ0yvS8GKgdw"
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
