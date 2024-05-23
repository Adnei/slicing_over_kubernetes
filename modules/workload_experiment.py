from modules.experiment import Experiment
from modules.kubernetes_cluster import REQUEST_TIMEOUT, KubernetesCluster
from kubernetes.client.rest import ApiException
from kubernetes import watch
from kubernetes import client

import requests
import json
import pandas as pd
import numpy as np
import datetime 

class WorkloadExperiment(Experiment):
    def __init__(
        self,
        cluster: KubernetesCluster,
        name="default_experiment",
        namespace="api-slicing",
        node=None,
        image="eduardogomescampos/test1_hamperer:1.1.0",
        cmdline="default"
    ):
        super().__init__(cluster, name, namespace)
        self.node = node
        self.image = image
        self.cmdline = cmdline
    def get_results(self):
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

    def get_data_df(self, iteration): 
        
        start = str(self.start_time)
        end = str(self.end_time)
        date_format = "%Y-%m-%d %H:%M:%S%z"

        date_obj_start = datetime.datetime.strptime(start, date_format)
        date_obj_end = datetime.datetime.strptime(end, date_format)

        unix_start = int(date_obj_start.timestamp())
        unix_end = int(date_obj_end.timestamp())

        if self.node == "worker1":
            instance = "192.168.235.131:8080" #scaphandre IP for worker 1 and prometheus' port (8080)
        elif self.node == "worker2":
            instance = "192.168.189.73:8080"
        elif self.node == "worker3":
            instance = "192.168.182.42:8080"
        elif self.node == "worker4":
            instance = "192.168.199.185:8080"
        elif self.node == "worker5":
            instance = "192.168.42.68:8080"
        else:
            instance = "" 
            
        metrics = ['scaph_host_power_microwatts{instance="'+instance+'"}/1000000'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s',
                    'sum(scaph_process_cpu_usage_percentage{instance="'+instance+'"})'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s',
                    'sum(scaph_process_memory_bytes{instance="'+instance+'"})'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s',
                    'scaph_host_cpu_frequency{instance="'+instance+'"}'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s',
                    'sum(scaph_process_power_consumption_microwatts{instance="'+instance+'",cmdline="'+self.cmdline+'"})'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s',
                    'sum(scaph_process_cpu_usage_percentage{instance="'+instance+'",cmdline="'+self.cmdline+'"})'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s',
                    'scaph_process_memory_bytes{instance="'+instance+'",cmdline="'+self.cmdline+'"}'+'&start='+str(unix_start)+'&end='+str(unix_end)+'&step=1s']

        data = []
        for x in metrics:
            response = requests.get('http://10.10.225.91:30000/api/v1/query_range?query='+x)
            data.append(response)
            
        powerJson = data[0].json()
        cpuJson = data[1].json()
        memJson = data[2].json()
        freqJson = data[3].json()
        powerPJson = data[4].json()
        cpuPJson = data[5].json()
        memPJson = data[6].json()

        TScpu = []
        cpu = []
        TSpower = []
        power = []
        TSmem = []
        mem = []
        TSfreq = []
        freq = []
        TSpowerP = []
        powerP = []
        TScpuP =[]
        cpuP = []
        TSmemP =[]
        memP = []
        
        for values in cpuJson['data']['result'][0]['values']:
            TScpu.append(values[0])
            cpu.append(values[1])
        for values in powerJson['data']['result'][0]['values']:
            TSpower.append(values[0])
            power.append(values[1])
        for values in memJson['data']['result'][0]['values']:
            TSmem.append(values[0])
            mem.append(values[1])
        for values in freqJson['data']['result'][0]['values']:
            TSfreq.append(values[0])
            freq.append(values[1])
        for values in powerPJson['data']['result'][0]['values']:
            TSpowerP.append(values[0])
            powerP.append(values[1])
        for values in cpuPJson['data']['result'][0]['values']:
            TScpuP.append(values[0])
            cpuP.append(values[1])
        for values in memPJson['data']['result'][0]['values']:
            TSmemP.append(values[0])
            memP.append(values[1])

        DFcpu = pd.DataFrame( {'CPU % - Worker': cpu}, 
                        index = TScpu)
        DFpower = pd.DataFrame( {'PWR - Worker (W)': power}, 
                        index = TSpower)
        DFmem = pd.DataFrame( {'RAM - Worker (B)': mem}, 
                        index = TSmem)
        DFfreq = pd.DataFrame( {'CPU FREQ - Worker (MHz)': freq}, 
                        index = TSfreq)
        DFcpuP = pd.DataFrame( {'CPU % - Process': cpuP}, 
                        index = TScpuP)
        DFpowerP = pd.DataFrame( {'PWR - Process (W)': powerP}, 
                        index = TSpowerP)
        DFmemP = pd.DataFrame( {'RAM - Process (B)': memP}, 
                        index = TSmemP)
        
        dfs = [DFpower, DFmem, DFfreq, DFcpuP, DFpowerP, DFmemP]
        dataframe = DFcpu.join(dfs)

        exec = iteration + 1
        dataframe['Part ID'] = self.name
        dataframe['Exec ID'] = exec

        return dataframe
