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
    ):
        super().__init__(cluster, name, namespace)
        self.node = node
        self.image = image
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

        # saving start and end time of the experiment
        start = self.start_time
        end = self.end_time
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        # converting start and end time to unix
        date_obj_start = datetime.datetime.strptime(start, date_format)
        date_obj_end = datetime.datetime.strptime(end, date_format)
        # converting datetime object to integer
        unix_start = int(date_obj_start.timestamp())
        unix_end = int(date_obj_end.timestamp())
    
        metrics = ['scaph_host_power_microwatts{instance="192.168.189.100:8080"}/1000000&start='+str(unix_start)+'&end='+str(unix_end)+'&step=5s' , 
                    'sum(scaph_process_cpu_usage_percentage{instance="192.168.189.100:8080"})&start='+str(unix_start)+'&end='+str(unix_end)+'&step=5s',
                    'sum(scaph_process_memory_bytes{instance="192.168.189.100:8080"})&start='+str(unix_start)+'&end='+str(unix_end)+'&step=5s'
                ]
        data = []

        # getting responses for each metric and appending them
        for x in metrics:
            response = requests.get('http://10.10.225.91:30000/api/v1/query_range?query='+x)
            data.append(response) 

        # creating different json objects for each metric
        powerJson = data[0].json()
        cpuJson = data[1].json()
        memJson = data[2].json()
        
        timeStamps = []
        power = []
        cpu = []
        mem = []

        # creates list of timestamps from the CPU json and a list of CPU values in the same order as the timestamps
        for values in cpuJson['data']['result'][0]['values']:
            timeStamps.append(values[0])
            cpu.append(values[1])

        # creates list of Power values in the same order as the timestamps
        for values in powerJson['data']['result'][0]['values']:
            power.append(values)

        # creates list of memory (RAM) values in the same order as the timestamps
        for values in memJson['data']['result'][0]['values']:
            mem.append(values)

        # creates dataframe with timestamps as index and a column with CPU values
        df = pd.DataFrame( {'CPU %': cpu}, 
                        index = timeStamps)

        # adds column with POWER values (verifies if the timestamps match)
        dfPower = []
        for index in range(len(df.index)):
            if df.index[index] == power[index][0]:
                dfPower.append(power[index][1]) 
            else:
                dfPower.append(np.nan) # if the timestamps dont match, fill element with None
        df['Power'] = dfPower

        # adds column with memory (RAM) values (verifies if the timestamps match)
        dfMem = []
        for index in range(len(df.index)):
            if df.index[index] == mem[index][0]:
                dfMem.append(mem[index][1]) 
            else:
                dfMem.append(np.nan) # if the timestamps dont match, fill with None
        df['Mem'] = dfMem

        exec = iteration + 1 # execution number
       
        # creates columns for part ID and execution ID
        df['Part ID'] = self.name
        df['Exec ID'] = exec

        # returns dataframe that will be saved to csv file in main
        return df 
