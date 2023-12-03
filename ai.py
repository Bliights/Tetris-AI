from tetrisgame import TetrisGame
from random import random, uniform, randint
import copy


class Ai:
    def __init__(self, screen):
        self.game = TetrisGame(screen)
        self.game.status.set_solo()
        self.multipliers = {}
        self.fitness = 0
        self.movementPlan = []
        self.screen = screen

    def fixMultiplier(self):       
        self.multipliers = {
            "holeCountMultiplier": 100,
            "bumpinessMultiplier": 10,
            "lineClearMultiplier": 60,
            "blocksRightLaneMultiplier": 30,
            "averagePeakMultiplier": 30,
            "maximumLineHeightMultiplier": 60,
            "openHoleCountMultiplier": 40
        }
        '''
        self.multipliers = {
            'holeCountMultiplier': 42.68264153847743, 
            'bumpinessMultiplier': 13.587323081008062, 
            'lineClearMultiplier': 78.37682266274075, 
            'blocksRightLaneMultiplier': 31.411371718826906, 
            'averagePeakMultiplier': 65.86099291324257, 
            'maximumLineHeightMultiplier': 22.520383663033915, 
            'openHoleCountMultiplier': 29.52488638146715
            }
        '''
        
    def randomizeMultipliers(self):
        self.multipliers = {
            "holeCountMultiplier": uniform(0, 100),
            "bumpinessMultiplier": uniform(0, 100),
            "lineClearMultiplier": uniform(0, 100),
            "blocksRightLaneMultiplier": uniform(0, 100),
            "averagePeakMultiplier": uniform(0, 100),
            "maximumLineHeightMultiplier": uniform(0, 100),
            "openHoleCountMultiplier": uniform(0, 100)
        }

    def calculateFitness(self):
        if self.game.totaLinesClear != 0:
            self.fitness = self.game.score / self.game.totaLinesClear
        else:
            self.fitness = 0

    def nextMove(self):
        if self.movementPlan[0] == "right":
            self.game.move_piece_right()
        elif self.movementPlan[0] == "left":
            self.game.move_piece_left()
        elif self.movementPlan[0] == "rotate":
            self.game.rotate_piece()
        else:
            self.game.drop()
        self.movementPlan.pop(0)

    def placePieceInBoardAtPosition(self, board, piece, position):
        piece.x = position[0]
        piece.y = position[1]
        for i in range(position[2]):
            piece.rotate()
        if board.is_valid_move(piece.shape, piece.x, piece.y):
            board.place_piece(piece)

    def costOfMove(self, board, piece, position):
        boardCopy = copy.deepcopy(board)
        pieceCopy = copy.deepcopy(piece)

        self.placePieceInBoardAtPosition(boardCopy, pieceCopy, position)

        lineClear = boardCopy.clear_lines()
        holes = boardCopy.get_number_holes()
        bumpiness = boardCopy.get_bumpiness()
        blocksRightmostLane = boardCopy.count_blocks_in_rightmost_lane()
        averagePeaks = boardCopy.get_average_peaks()
        maximumLineHeight = boardCopy.get_maximum_line_height()
        openHoles = boardCopy.get_number_open_holes()

        costLineClear = 0
        if lineClear != 4:
            costLineClear = self.multipliers["lineClearMultiplier"] * lineClear
        else:
            costLineClear = -self.multipliers["lineClearMultiplier"] * lineClear

        return (
            self.multipliers["holeCountMultiplier"] * holes
            + self.multipliers["bumpinessMultiplier"] * bumpiness
            + costLineClear
            + self.multipliers["blocksRightLaneMultiplier"] * blocksRightmostLane
            + self.multipliers["averagePeakMultiplier"] * averagePeaks
            + self.multipliers["maximumLineHeightMultiplier"] * maximumLineHeight
            +self.multipliers["openHoleCountMultiplier"] * openHoles
        )

    def getBestMove(self):
        positionsCurrent = self.game.board.get_all_position(self.game.current_piece)
        costPositions = []
        BestPositionsNext = []
        for i in range(len(positionsCurrent)):
            costPositions.append(
                self.costOfMove(
                    self.game.board, self.game.current_piece, positionsCurrent[i]
                )
            )

            boardCopy = copy.deepcopy(self.game.board)
            pieceCopy = copy.deepcopy(self.game.current_piece)
            self.placePieceInBoardAtPosition(boardCopy, pieceCopy, positionsCurrent[i])

            positionsNext = boardCopy.get_all_position(self.game.next_piece)
            costNext = []
            for j in range(len(positionsNext)):
                costNext.append(
                    self.costOfMove(boardCopy, self.game.next_piece, positionsNext[j])
                )

            indexBestNextMove = costNext.index(min(costNext))
            BestPositionsNext.append(positionsNext[indexBestNextMove])
            costPositions[i] += costNext[indexBestNextMove]

        indexBestMoves = costPositions.index(min(costPositions))
        return self.game.current_piece.get_path_to_position(
            positionsCurrent[indexBestMoves]
        )

    def addMoves(self, path):
        for i in range(len(path)):
            self.movementPlan.append(path[i])

    def mutate(self, mutationRate):
        if random() < mutationRate:
            num = randint(0, len(self.multipliers)-1)
            count=0
            for key, value in self.multipliers.items():
                if num == count:
                    self.multipliers[key] = uniform(0, 100)
                    break
                count+=1
            
    def clone(self):
        clone = Ai(self.screen)
        clone.multipliers = self.multipliers
        return clone

    def reset(self):
        self.game.reset()
        self.game.status.set_solo()
        self.fitness = 0
        self.movementPlan = []
