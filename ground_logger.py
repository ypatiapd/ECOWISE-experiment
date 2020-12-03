import logging
class ground_logger:
    __instance=None
    def __init__(self,loggername,filename):
        self.logger=logging.getLogger(filename)
        self.logger.setLevel(logging.INFO)
        self.formatter=logging.Formatter('%(message)s')
        self.file_handler=logging.FileHandler(filename)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        #logging.basicConfig(filename='data.log', level=logging.INFO,format='%(asctime)s:%(name)s:%(message)s')
    def write_info(self,str):
        self.logger.info(str)
