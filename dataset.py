import numpy as np

class Dataset:
    def __init__ (self):
        self.dataset=[[0,0,0,0,0,0,0,0,0,0],0,0,0,0,0]
        
    def get_peaks(self,grid):
        gridWidth=len(grid[0])
        gridHeight=len(grid)
        peaks=[0]*gridWidth
        for i in range(gridWidth):
            j=0
            while j<gridHeight and grid[j][i]==0:        
                j+=1
            peaks[i]=gridHeight-j
        return peaks
                 
    def get_bumpiness(self,grid):
        gridWidth=len(grid[0])
        gridHeight=len(grid)
        bumpiness=0
        previousHeight=0
        for i in range(gridWidth):
            j=0
            while j<gridHeight and grid[j][i]==0:
                j+=1
            if i>0:
                bumpiness+=abs(previousHeight+j-gridHeight)
            previousHeight=gridHeight-j
        return bumpiness

    def get_number_holes(self,peaks,grid): #this method will count the number of cells that are under a filled cell (this does not litterally count holes, bus rather counts the number of cells that are hard and impossible to fill)
        holes_count=0
        gridWidth=len(grid[0])
        for i in range(gridWidth):
            j=0
            test=False
            while j<len(grid):
                if(grid[j][i]==1):
                    test=True
                if(grid[j][i]==0 and test==True):
                    holes_count+=1
                j+=1
        return holes_count
 
    def get_data(self,grid):
        
        #peak data
        peaks=self.get_peaks(grid)
        max_peak=np.max(peaks)
        min_peak=np.min(peaks)
        average_peak=sum(peaks)/len(peaks)
             
        #bumpiness
        bumpiness=self.get_bumpiness(grid)
             
        #holes
        number_holes=self.get_number_holes(peaks,grid)
             
        #clearable lines
        #clearable_lines=self.get_clearable_lines(peaks,max_peak,min_peak)
        
        return peaks,max_peak,min_peak,average_peak,bumpiness,number_holes