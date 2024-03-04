from modules.kubernetes_cluster import KubernetesCluster
from modules.workload_experiment import WorkloadExperiment


def main():
    auth_token "<>"
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
