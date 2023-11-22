class OutRangeError(Exception):
    def __init__(self, path, message):
        self.message = '\nOutRangeError: '+path+'\nError massage: '+ message
    
    def __str__(self):
        return self.message