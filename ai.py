from tetrisgame import TetrisGame
from random import random
import copy

class Ai:
    def __init__(self,screen):
        self.game=TetrisGame(screen)
        self.multipliers = {}
        self.fitness = 0
        self.movementPlan=[]
        
    def fixMultiplier(self):
        self.multipliers={
            "holeCountMultiplier": 100,
            "bumpinessMultiplier":5,
            "lineClearMultiplier":20,
            "blocksRightLaneMultiplier":10,
            "averagePeakMultiplier":1
            }
        
    def randomizeMultipliers(self):
         self.multipliers={
             "holeCountMultiplier": 100 * random(0, 2),
             "bumpinessMultiplier":5 * random(0, 2),
             "lineClearMultiplier":20 * random(0, 2),
             "blocksRightLaneMultiplier":10 * random(0, 2),
             "averagePeakMultiplier":1 * random(0, 2)
             }
    
    def calculateFitness(self):
        self.fitness = self.game.score
    
    def nextMove(self):
        if(self.movementPlan[0]=="right"):
            self.game.move_piece_right()
        elif(self.movementPlan[0]=="left"):
            self.game.move_piece_left()
        elif(self.movementPlan[0]=="rotate"):
            self.game.rotate_piece()
        else:
            self.game.drop()   
        self.movementPlan.pop(0)
    
    def costOfMove(self,board,piece,position):
        boardCopy = copy.deepcopy(board)
        pieceCopy = copy.deepcopy(piece)
        
        pieceCopy.x = position[0]
        pieceCopy.y = position[1]
        for i in range(position[2]):
            pieceCopy.rotate()
            
        boardCopy.place_piece(pieceCopy)
        
        lineClear = boardCopy.clear_lines()
        holes = boardCopy.get_number_holes()
        bumpiness = boardCopy.get_bumpiness()
        blocksRightmostLane = boardCopy.count_blocks_in_rightmost_lane()
        averagePeaks = boardCopy.get_average_peaks()
        
        costLineClear=0
        if(lineClear!=4):
            costLineClear = self.multipliers["lineClearMultiplier"]*lineClear
        else:
            costLineClear = -self.multipliers["lineClearMultiplier"]*lineClear
        
        return (self.multipliers["holeCountMultiplier"]*holes + 
                self.multipliers["bumpinessMultiplier"]*bumpiness +
                costLineClear +
                self.multipliers["blocksRightLaneMultiplier"]*blocksRightmostLane +
                self.multipliers["averagePeakMultiplier"]*averagePeaks )
    
    def getBestMove(self):
        positions = self.game.board.get_all_position(self.game.current_piece)
        costPositions =[]
        for i in range(len(positions)):
            costPositions.append(self.costOfMove(self.game.board,self.game.current_piece,positions[i]))
        indexMinCost = costPositions.index(min(costPositions))
        return self.game.current_piece.get_path_to_position(positions[indexMinCost])
    
    def addMoves(self,path):
        self.movementPlan.append(path)
        
        
        
        