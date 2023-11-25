from tetrisgame import TetrisGame
from random import random,uniform
import copy

class Ai:
    def __init__(self,screen):
        self.game=TetrisGame(screen)
        self.game.status.set_solo()
        self.multipliers = {}
        self.fitness = 0
        self.movementPlan=[]
        self.screen = screen
        
    def fixMultiplier(self):
        self.multipliers={
            "holeCountMultiplier": 100,
            "bumpinessMultiplier":5,
            "lineClearMultiplier":20,
            "blocksRightLaneMultiplier":10,
            "averagePeakMultiplier":10,
            "maximumLineHeightMultiplier":1
            }
        
    def randomizeMultipliers(self):
         self.multipliers={
             "holeCountMultiplier": 100 * uniform(0, 2),
             "bumpinessMultiplier":5 * uniform(0, 2),
             "lineClearMultiplier":20 * uniform(0, 2),
             "blocksRightLaneMultiplier":10 * uniform(0, 2),
             "averagePeakMultiplier":10 * uniform(0, 2),
             "maximumLineHeightMultiplier":1* uniform(0, 2)
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
    
    def placePieceInBoardAtPosition(self,board,piece,position):    
        piece.x = position[0]
        piece.y = position[1]
        for i in range(position[2]):
            piece.rotate()
        if board.is_valid_move(piece.shape,piece.x, piece.y):
            board.place_piece(piece)
    
    def costOfMove(self,board,piece,position):
        boardCopy = copy.deepcopy(board)
        pieceCopy = copy.deepcopy(piece)
        
        self.placePieceInBoardAtPosition(boardCopy,pieceCopy,position)

        
        lineClear = boardCopy.clear_lines()
        holes = boardCopy.get_number_holes()
        bumpiness = boardCopy.get_bumpiness()
        blocksRightmostLane = boardCopy.count_blocks_in_rightmost_lane()
        averagePeaks = boardCopy.get_average_peaks()
        maximumLineHeight = boardCopy.get_maximum_line_height()
        
        costLineClear=0
        if(lineClear!=4):
            costLineClear = self.multipliers["lineClearMultiplier"]*lineClear
        else:
            costLineClear = -self.multipliers["lineClearMultiplier"]*lineClear
        
        return (self.multipliers["holeCountMultiplier"]*holes + 
                self.multipliers["bumpinessMultiplier"]*bumpiness +
                costLineClear +
                self.multipliers["blocksRightLaneMultiplier"]*blocksRightmostLane +
                self.multipliers["averagePeakMultiplier"]*averagePeaks +
                self.multipliers["maximumLineHeightMultiplier"]*maximumLineHeight
                )
    
    def getBestMove(self):
        positionsCurrent = self.game.board.get_all_position(self.game.current_piece)
        costPositions = []
        BestPositionsNext = []
        for i in range(len(positionsCurrent)):
            costPositions.append(self.costOfMove(self.game.board,self.game.current_piece,positionsCurrent[i]))
            
            boardCopy = copy.deepcopy(self.game.board)
            pieceCopy = copy.deepcopy(self.game.current_piece)
            self.placePieceInBoardAtPosition(boardCopy,pieceCopy,positionsCurrent[i])
            
            positionsNext = boardCopy.get_all_position(self.game.next_piece)
            costNext = []
            for j in range(len(positionsNext)):
               costNext.append(self.costOfMove(boardCopy,self.game.next_piece,positionsNext[j]))
            
            indexBestNextMove = costNext.index(min(costNext))
            BestPositionsNext.append(positionsNext[indexBestNextMove])
            costPositions[i]+=costNext[indexBestNextMove]
        
        indexBestMoves = costPositions.index(min(costPositions))
        return self.game.current_piece.get_path_to_position(positionsCurrent[indexBestMoves])
    
    def addMoves(self,path):
        for i in range(len(path)):
            self.movementPlan.append(path[i])
    
    def mutate(self,mutationRate):
        for key, value in self.multipliers.items():
            if random() < mutationRate:
                self.multipliers[key] = value * uniform(0.95, 1.05)
    
    def clone(self):
        clone = Ai(self.screen)       
        clone.multipliers = self.multipliers
        return clone

    def reset(self):
        self.game.reset()
        self.game.status.set_solo()
        self.movementPlan=[]
        