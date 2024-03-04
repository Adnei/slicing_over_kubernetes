from modules.kubernetes_cluster import KubernetesCluster
from modules.workload_experiment import WorkloadExperiment


def main():
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFabnJBcXBxcngyTVFmOFVZVGdyOURRSzQ1a3d0TFpuTkdMRGZmelpxT3cifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcGktc2xpY2luZyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhcGktc2xpY2luZy1zZWNyZXQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYXBpLXNsaWNpbmctc3ZjIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNzQ3Y2U3NTYtNzIwNC00YTY4LWIzNmEtZWYxYjA4YTFkYmRkIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFwaS1zbGljaW5nOmFwaS1zbGljaW5nLXN2YyJ9.uG9bWigz0mRotO_zSvFzdA7b_Whyj2x9wwBC3CUYjzKD8aXOcdDO1XE4pF-w4TzTSWAGvbM-x_n3kX5zC1UQvvvZOJlbIywKo8yLy8VX9E3f7GaiD_MAxhIsSif9ckzPWBNVGcOWf7SZq6LDRJ_kBL8LBU2KwgjwopOmQtgEErcu7VUyB9S-ElAp5opXl83BUkhc9r2_q3rj-j-jMrVEHTM6qKIXY_U6cDd3ZeCp2DRLZj2WxzECd7gBNzKxpRvkl5SwOZ7nSUPmAGhV1UXqZ4grFEgSLmXiHworbcJtJtQ0EQtsC1_DGuz0vwdwGD6WCvtT4jPsJejZ0yvS8GKgdw"

    sfi2_cluster = KubernetesCluster(auth_token)
    sample_constant_exp = WorkloadExperiment(
        cluster=sfi2_cluster,
        name="constant-test-2",
        namespace="api-slicing",
        node="worker1",
    )
    # É possível executar N experimentos ao mesmo tempo, criando uma lista de Experiments com parâmetros diferentes
    # O tempo de execução do experimento deveria ser um parâmetro. No entanto, esse tempo é definido na imagem do job
    # A imagem usada no job do experimento também é parametrizável. @param image="<nome da imagem>"
    sample_constant_exp.start()


if __name__ == "__main__":
    main()
