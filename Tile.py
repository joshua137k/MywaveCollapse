import pygame

class Tile:
    def __init__(self,img,edges):
        super().__init__()
        self.img = img
        self.edges = edges

        self.up = []
        self.right = []
        self.down = []
        self.left = []

    
    def rotate(self,angle):
        newImg=None
        if self.img!=None:
            newImg = pygame.transform.rotate(self.img, -90*angle)
        numEdges = len(self.edges)
        newEdges=[0 for i in range(numEdges)]
        for i in range(numEdges):
            newEdges[i] = self.edges[(i - angle + numEdges) % numEdges]
        return Tile(newImg,newEdges)

    def analyze(self,tiles):
        for i in range(len(tiles)):
            tile = tiles[i]
            #UP
            if (tile.edges[2]==self.edges[0]):
                self.up.append(i)
            #RIGHT
            if (tile.edges[3]==self.edges[1]):
                self.right.append(i)
            #DOWN
            if (tile.edges[0]==self.edges[2]):
                self.down.append(i)
            #LEFT
            if (tile.edges[1]==self.edges[3]):
                self.left.append(i)
            

