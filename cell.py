class Cell:
    def __init__(self,num,arr=[]):
        super().__init__()
        self.collapsed = False  
        self.options=[]
        if arr==[]:
            self.options = [i for i in range(num)]
        else:
            self.options=arr
        