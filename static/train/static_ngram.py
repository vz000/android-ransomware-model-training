import pandas as pd

'''
# param dataset_file - Name of the file where the list of permissions are included. Must be a csv.
                       Naming format: permissions-{type}.csv
# param out_file - output from static_stats module
# param n - N-gram size
'''
class permissions_ngram():
    def __init__(self, dataset_file : str, out_file, n : int) -> None:
        self.dataset_file = dataset_file
        self.out_file = out_file
        self.n = n
        self.final_list = []
        self.chunks = []
        self.__generate_stats()
        self.__draft_detectors()
    
    # Recupera el archivo donde se almacenaron la lista de permisos a utilizar
    def __generate_stats(self) -> None:
        file_permissions = self.out_file
        with open(file_permissions,'r') as list:
            for row in list:
                if "\n" in row:
                    row = row.rstrip()
                self.final_list.append(row)

    # Genera el primer borrador de detectores
    # Lee el archivo permissions.csv en la carpeta out/ransomware/static/train
    def __draft_detectors(self) -> None:
        with open(self.dataset_file,'r') as permissions:
            for row in permissions:
                permissions = row.split(",")
                end = len(permissions) - 1 # amount of permissions and end of list
                start = 0
                while start < end:
                    n_gram = permissions[start:start+self.n] # recorrido de 3
                    first_match = 0
                    clean_list = []
                    if len(n_gram) >= self.n:
                        for word in n_gram:
                            if word in self.final_list:
                                exp = self.final_list.index(word.rstrip())
                                clean_list.append(2**exp) # obtiene el valor para el permiso segun su lugar en la lista
                                first_match += 1
                            else:
                                clean_list.append(0) # añade 0
                        n_gram = sum(clean_list) # suma los 3 elementos
                    # Almacena en la lista la suma solo si esta no se ha añadido con anterioridad
                    # y si hubo almenos una coincidencia con la lista
                    if first_match > 0:
                        if n_gram not in self.chunks:
                            self.chunks.append(n_gram)
                    start += 1

# funciones para recuperar las listas: detectores y permisos de la lista static.csv
    def get_draft_detectors(self) -> list:
        return self.chunks
    
    def get_permission_list(self) -> list:
        return self.final_list
