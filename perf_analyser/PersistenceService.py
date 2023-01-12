from abc import ABC,abstractmethod 
  
class PersistenceService():
    #TODO: Idee der abstrakten Klasse erstmal verworfen, bei zweiter Persistenz-Möglichkeit nochmal anbinden
    @abstractmethod
    def __init__(db_name: str):
        pass

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def store_testrun(self, testcase):
        pass

    @abstractmethod
    def get_last_n_runs(self, testname: str, n: int):
        pass

    @abstractmethod
    def get_avg_of_last_runs(self, testname: str, n: int):
        pass 
