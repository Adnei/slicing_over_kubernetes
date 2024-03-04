# @DEPRECATED FILE. WILL BE REMOVED SOON
import time

from kubernetes import config, client
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api, batch_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


def exec_commands(api_batch, api_core):
    name = "constant-test"
    resp = None
    try:
        resp = api_batch.read_namespaced_job(name=name, namespace="default")
    except ApiException as e:
        if e.status != 404:
            print("Error reading namespaced job: ", e)
            print(f"Unknown error: {e}")
            exit(1)

    if not resp:
        print(f"Test (job) {name} does not exist. Creating it...")
        job_body = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"name": name},
            "spec": {
                "template": {
                    "spec": {
                        "restartPolicy": "Never",
                        "containers": [
                            {
                                "name": "constant-test",
                                "image": "eduardogomescampos/test1_hamperer:1.1.0",
                            }
                        ],
                        "nodeName": "worker1",
                    }
                }
            },
        }
        api_batch.create_namespaced_job(namespace="api-slicing", body=job_body)
        print("Done. The test is now running :)")
        time.sleep(380)
        print("The test is now over!")
        api_batch.delete_namespaced_job(name=name, namespace="api-slicing")
        print("Cleaning leftover pods")
        pods_list = api_core.list_namespaced_pod(namespace="api-slicing")
        pods_list_items = pods_list.items
        for i in pods_list_items:
            api_core.delete_namespaced_pod(
                name=i.metadata.name, namespace="api-slicing"
            )
        print("All pods are being deleted")


def main():
    auth_token = "<kubectl describe secret -n api-slicing api-slicing-secret>"
    client_config = client.Configuration()
    client_config.host = "https://10.10.225.91:6443"
    # no ssl security for now
    client_config.verify_ssl = False
    client_config.api_key = {"authorization": "Bearer " + auth_token}

    api_client = client.ApiClient(client_config)
    api_v1 = client.api.batch_v1_api.BatchV1Api(api_client)
    api_core = core_v1_api.CoreV1Api(api_client)
    exec_commands(api_v1, api_core)


if __name__ == "__main__":
    main()
