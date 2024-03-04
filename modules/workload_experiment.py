from modules.experiment import Experiment
from modules.kubernetes_cluster import REQUEST_TIMEOUT, KubernetesCluster
from kubernetes.client.rest import ApiException
from kubernetes import watch
from kubernetes import client


class WorkloadExperiment(Experiment):
    def __init__(
        self,
        cluster: KubernetesCluster,
        name="default_experiment",
        namespace="api-slicing",
        node=None,
        image="eduardogomescampos/test1_hamperer:1.1.0",
    ):
        super().__init__(cluster, name, namespace)
        self.node = node
        self.image = image

    def start(self):
        def _check_for_job():
            resp = None
            try:
                resp = self.cluster.batch_v1_api.read_namespaced_job(
                    name=self.name, namespace=self.namespace
                )
            except ApiException as e:
                if e.status != 404:
                    print("API error while reading namespaced job: ", e)
                    exit(1)
            return resp

        def _wait_for_job():
            watcher = watch.Watch()
            for event in watcher.stream(
                self.cluster.batch_v1_api.list_namespaced_job,
                namespace=self.namespace,
                label_selector=f"job-name={self.name}",
                timeout_seconds=0,
                _request_timeout=REQUEST_TIMEOUT,
            ):
                obj = event["object"]
                # print(obj.metadata.name)
                # print("TESTING")
                # print(obj)

                if obj.status.succeeded:
                    self.start_time = obj.status.start_time
                    self.end_time = obj.status.completion_time
                    print("Experiment ", self.name, " completed")
                    print("Start time: ", self.start_time)
                    print("End time: ", self.end_time)
                    watcher.stop()
                    return

                if not obj.status.active and obj.status.failed:
                    watcher.stop()
                    raise Exception("Job Failed")

        response = _check_for_job()
        if not response:
            print("Job: ", self.name, " does not exist. Creating it...")
            job_body = {
                "apiVersion": "batch/v1",
                "kind": "Job",
                "metadata": {"name": self.name, "namespace": self.namespace},
                "spec": {
                    "template": {
                        "spec": {
                            "restartPolicy": "Never",
                            "containers": [
                                {
                                    "name": self.name,
                                    "image": self.image,
                                }
                            ],
                            "nodeName": self.node,
                        }
                    }
                },
            }
            self.cluster.batch_v1_api.create_namespaced_job(
                namespace=self.namespace, body=job_body
            )
            print("Job created!")
            print("Waiting for the job to finish")
            delete_opt_body = client.V1DeleteOptions(propagation_policy="Background")
            _wait_for_job()
            print("Deleting job")
            self.cluster.batch_v1_api.delete_namespaced_job(
                name=self.name, body=delete_opt_body, namespace=self.namespace
            )
            # @TODO
            #    - Salvar informações do experimento
            #    - Gerar .csv do intervalo de duração do experimento (usar API Grafana ou Prometheus)
