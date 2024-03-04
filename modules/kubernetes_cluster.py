from kubernetes import client, config


REQUEST_TIMEOUT = 600


class KubernetesCluster:
    """
    Class for authenticating and using the Kubernetes Python API
    """

    def __init__(self, token=None, host="https://10.10.225.91:6443"):
        if not token:
            raise ValueError("Token not provided")
        self.client_config = client.Configuration()
        self.client_config.host = host

        # TODO: Verifying SSL is not priority for now
        self.client_config.verify_ssl = False
        self.token = token
        self.client_config.api_key = {"authorization": "Bearer " + self.token}
        self.api_client = client.ApiClient(self.client_config)
        self.core_v1_api = client.api.core_v1_api.CoreV1Api(self.api_client)
        self.batch_v1_api = client.api.batch_v1_api.BatchV1Api(self.api_client)
