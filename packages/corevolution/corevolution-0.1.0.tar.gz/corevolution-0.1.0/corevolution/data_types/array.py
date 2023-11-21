

class Array(): 
    # TODO 
    
    def __init__(self, dim:tuple(int), data:list, dtype:type): 
        
        
        self.dim = dim
        self.data = data
        self.dtype = dtype
        
    def __str__(self): 
        print(self.data)