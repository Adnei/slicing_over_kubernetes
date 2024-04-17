from modules.kubernetes_cluster import KubernetesCluster
from modules.workload_experiment import WorkloadExperiment
from time import time

def part_setup(cluster):
    experiment_part = []
    print("Instatiating a part\n")
    option = -1
    last_option = -1
    while (option != 1 or last_option != 2):
        last_option = option
        print("\n1- Quit")
        print("2- Add a job")
        option = int(input("Select an option: "))
        if (option == 1 and last_option != 2):
            print("\nPlease add a job before quitting")
        if option == 2:
            print("\nPAY ATTENTION NOW!!! ANY IMPROPER CONFIGURATIONS ***WILL*** CAUSE THE TEST TO MALFUNCTION\n")
            name = input("Enter a job name: ")
            node = input("Enter a node for the job to be run on: ")
            print("\nDo not forget to especify the tag you're using for the image\n")
            image = input("Enter the image name: ")
            experiment_part.append(WorkloadExperiment(cluster=cluster,
                name=name,
                namespace='api-slicing',
                node=node,
                image=image,)
                )
    return experiment_part
    
def main():
    ############# Descrição das imagens #############
    ## test1_regular (https://hub.docker.com/r/eduardogomescampos/test1_regular)
    # 1.0.0: não funciona
    # 1.1.0: dura 6 minutos e oferece uma carga periódica de 3 instâncias executando sqrt() que atua por 10 segundos em cada um dos 18 ciclos de 20 segundos
    # 1.2.0: dura 6 minutos e oferece uma carga periódica de 3 instâncias executando sqrt() que atua por 1 min em cada um dos 3 ciclos de 2 min
    # 1.3.0: dura 16 minutos e oferece uma carga periódica de 15 instâncias executando sync() que atua por 1 min em cada um dos 8 ciclos de 2 min
    # 1.3.1: dura 16 minutos e oferece uma carga periódica de 10 instâncias executando sync() que atua por 1 min em cada um dos 8 ciclos de 2 min
    # 1.4.0: dura 6 minutos e oferece uma carga periódica de 15 instâncias executando sync() que atua por 1 min em cada um dos 3 ciclos de 2 min
    # 1.4.1: dura 6 minutos e oferece uma carga periódica de 10 instâncias executando sync() que atua por 1 min em cada um dos 3 ciclos de 2 min
    # 1.4.2: dura 6 minutos e oferece uma carga periódica de 5 instâncias executando sync() que atua por 1 min em cada um dos 3 ciclos de 2 min
    # 1.4.3: dura 6 minutos e oferece uma carga periódica de 2 instâncias executando sync() que atua por 1 min em cada um dos 3 ciclos de 2 min
    # 1.4.4: dura 6 minutos e oferece uma carga periódica de 7 instâncias executando sync() que atua por 1 min em cada um dos 3 ciclos de 2 min
    # 1.4.5: dura 6 minutos e oferece uma carga periódica de 12 instâncias executando sync() que atua por 1 min em cada um dos 3 ciclos de 2 min
    ## test1_hamperer (https://hub.docker.com/r/eduardogomescampos/test1_hamperer)
    # 1.0.0: não funciona
    # 1.1.0: dura 6 minutos e oferece uma carga constante de 3 instâncias executando sqrt()
    # 1.1.1: dura 30 minutos e oferece uma carga constante de 3 instâncias executando sqrt()
    # 1.1.2: dura 30 minutos e oferece uma carga constante de 2 instâncias executando sqrt()
    # 1.1.3: dura 36 minutos e oferece uma carga constante de 2 instâncias executando sqrt()
    # 1.1.4: dura 6 minutos e oferece uma carga constante de 2 instâncias executando sqrt()
    ## empty_test (https://hub.docker.com/repository/docker/eduardogomescampos/empty_test)
    # 1.0.0: dura 5 segundos e não executa nada após subir
    auth_token ""
    sfi2_cluster = KubernetesCluster(auth_token)
    experiment_list = []
    print("Welcome to the experiment manager interface\n")
    option = -1
    last_option = -1
    parts = 0 
    while option != '3':
        last_option = option
        print("1 - Create new experiment")
        print("2 - Run created experiment")
        print("3 - Quit")
        option = input("Please select an option: ")
        print("\n")
        if (option == '2' and last_option != '1'):
            print("Test is not ready, please create it first\n\n")
        if option == '1':
            if (len(experiment_list) > 0):
                print("This will override the previous test!\n")
            experiment_list = []
            parts = int(input("How many parts will the test have? "))
            for i in range(parts):
                print(f"\n***Regarding the part {i+1}***\n")
                experiment_list.append(part_setup(sfi2_cluster))
        if (option == '2' and last_option == '1'):
            cycles = int(input("How many cycles should the test have: "))
            print("Starting experiment\n")
            for i in range(cycles):
                for experiment_part in experiment_list:
                    for experiment in experiment_part:
                        experiment.start()
                    for experiment in experiment_part:
                        experiment.get_results()
                iteration = i + 1
                print(f"Finished execution number {iteration}")
            print("Finishing experiment\n")
if __name__ == "__main__":
    main()
