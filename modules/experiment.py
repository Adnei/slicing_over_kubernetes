from modules.kubernetes_cluster import KubernetesCluster
import abc


class Experiment:
    __metaclass__ = abc.ABCMeta

    def __init__(
        self,
        cluster: KubernetesCluster,
        name,
        namespace,
    ):
        self.cluster = cluster
        self.name = name
        self.namespace = namespace
        self.start_time = None
        self.end_time = None

    @abc.abstractmethod
    def start(self):
        return
