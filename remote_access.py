# DEPRECATED FILE. WILL BE REMOVED SOON
# Load venv from kubernetes package

from kubernetes import client, config


def main():
    auth_token = "<kubectl describe secret -n api-slicing api-slicing-secret>"
    client_config = client.Configuration()
    client_config.host = "https://10.10.225.91:6443"
    # no ssl security for now
    client_config.verify_ssl = False
    client_config.api_key = {"authorization": "Bearer " + auth_token}

    api_client = client.ApiClient(client_config)

    api_v1 = client.CoreV1Api(api_client)
    print("Listing pods and their IPs:")
    ret = api_v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")


if __name__ == "__main__":
    main()


# follow :
# Principal --> https://stackoverflow.com/questions/62589073/kubernetes-api-cannot-list-resource-pods-in-api-group?rq=3
# criar namespace (talvez), ServiceAccount, Role, and RoleBinding para API
# https://stackoverflow.com/questions/55742540/kubernetes-python-client-connection-issue
#
