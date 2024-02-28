from kubernetes import client, config


def main():
    auth_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFabnJBcXBxcngyTVFmOFVZVGdyOURRSzQ1a3d0TFpuTkdMRGZmelpxT3cifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjRlMzkwYzE2LWFhZGQtNDRmNi05YWYyLWFmYzIwZDY3NTJiYiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.W_HnTmeOxwv1iMClo0lRSWecPSANVU6FayKT9yFOzq5rVW-wCtV-jOIUIjvH2Vi8lxJ1DE-mjBi6_oUmw_1tTFz1Usd0D3CedicnhJ6aQTFftwPzdtAKBFgqvYxnH54YUloWhz4wAkNNQQEIAtLLDUXAfTr7eURCvV6zZvH3pDR8DGf-RQwNbRwEi2XOsb7HVCQY5kGxm1rXnmF82k20-EPNOudljKEzbMb6U4cwNIpnNlR5aebHJd7OulDv5RGbVC8_fYgKFtWC7GhQ2OqRtSAyldT-mE_E_SrNFPGmyDk6LY9DkPHTqUbSGIhYu0YppX93hZUkrsYuIVBynFOwjg"
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
