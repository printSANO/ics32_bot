class GameBoard:
    """A class encapsulating tic tac toe board logic.
    """
    def __init__(self):
        """Args:
                board: tic tac toe game board iterable[list[str]]
        """
        self.board = {"1": " ","2": " ","3": " ","4": " ","5": " ","6": " ","7": " ","8": " ","9": " "}

    def userUpdateBoard(self, data):
        self.board[data] = "X"

    def aiUpdateBoard(self, data):
        self.board[data] = "O"

    def checkUserWin(self) -> bool:
        """Check if the User won the game.
        """
        winstate = False
        lst = [] #contains 8 logics
        for j in range(1,10,3):
            y1 = str(j)
            y2 = str(j+1)
            y3 = str(j+2)
            row = [self.board[y1],self.board[y2],self.board[y3]]
            num_x = row.count("X")
            lst.append(num_x)
        for i in range(1,4):
            x1 = str(i)
            x2 = str(i+3)
            x3 = str(i+6)
            column = [self.board[x1],self.board[x2],self.board[x3]]
            num_x = column.count("X")
            lst.append(num_x)
        d1 = [self.board["1"],self.board["5"],self.board["9"]]
        d2 = [self.board["3"],self.board["5"],self.board["7"]]
        d1x = d1.count("X")
        d2x = d2.count("X")
        lst.append(d1x)
        lst.append(d2x)
        for k in lst:
            if k == 3:
                winstate = True
        return winstate

    def checkAIWin(self) -> bool:
        """Check if the AI won the game.
        """
        winstate = False
        lst = [] #contains 8 logics
        for j in range(1,10,3):
            y1 = str(j)
            y2 = str(j+1)
            y3 = str(j+2)
            row = [self.board[y1],self.board[y2],self.board[y3]]
            num_x = row.count("O")
            lst.append(num_x)
        for i in range(1,4):
            x1 = str(i)
            x2 = str(i+3)
            x3 = str(i+6)
            column = [self.board[x1],self.board[x2],self.board[x3]]
            num_x = column.count("O")
            lst.append(num_x)
        d1 = [self.board["1"],self.board["5"],self.board["9"]]
        d2 = [self.board["3"],self.board["5"],self.board["7"]]
        d1x = d1.count("O")
        d2x = d2.count("O")
        lst.append(d1x)
        lst.append(d2x)
        for k in lst:
            if k == 3:
                winstate = True
        return winstate
    def checkDraw(self) -> bool:
        """Check if the game is a draw.
        """
        drawState = False
        state = self.checkEmpty()
        if len(state) == 0:
            drawState = True
        return drawState

    def aiHard(self) -> str:
        """Make move using hard version of AI.
            Returns a position of calculated move.
        """
        state = self.board
        turn = list(self.board.values()).count("X")
        if turn == 1:
            if state["2"] == "X" or state["4"] == "X" or state["5"] == "X":
                return "1"
            elif state["8"] == "X":
                return "2"
            elif state["6"] == "X":
                return "3"
            else:
                return "5"
        if turn == 2:
            val = self.findTwoUser()
            if val == None:
                val = self.findOne()
            return val
            
        if turn == 3:
            val = self.findTwoAI()
            if val == None:
                val = self.findTwoUser()
                if val == None:
                    val = self.findOne()
                    if val == None:
                        val = self.findNoWin()
            return val
            
        if turn == 4:
            val = self.findTwoAI()
            if val == None:
                val = self.findTwoUser()
                if val == None:
                    val = self.findOne()
                    if val == None:
                        val = self.findNoWin()
            return val

    def findOne(self):
        state = self.board
        row1 = ["1","2","3"]
        row2 = ["4","5","6"]
        row3 = ["7","8","9"]
        col1 = ["1","4","7"]
        col2 = ["2","5","8"]
        col3 = ["3","6","9"]
        dia1 = ["1","5","9"]
        dia2 = ["3","5","7"]
        lst = [row1,row2,row3,col1,col2,col3,dia1,dia2]
        for j in lst:
            xNum = 0
            oNum = 0
            for i in j:
                val = state[i]
                if val == "X":
                    xNum += 1
                if val == "O":
                    oNum += 1
            if xNum == 0 and oNum == 1:
                for k in j:
                    if state[k] == " ":
                        return k


    def findTwoUser(self):
        state = self.board
        row1 = ["1","2","3"]
        row2 = ["4","5","6"]
        row3 = ["7","8","9"]
        col1 = ["1","4","7"]
        col2 = ["2","5","8"]
        col3 = ["3","6","9"]
        dia1 = ["1","5","9"]
        dia2 = ["3","5","7"]
        lst = [row1,row2,row3,col1,col2,col3,dia1,dia2]
        for j in lst:
            xNum = 0
            oNum = 0
            for i in j:
                val = state[i]
                if val == "X":
                    xNum += 1
                if val == "O":
                    oNum += 1
            if xNum == 2 and oNum == 0:
                for k in j:
                    if state[k] == " ":
                        return k

    def findTwoAI(self):
        state = self.board
        row1 = ["1","2","3"]
        row2 = ["4","5","6"]
        row3 = ["7","8","9"]
        col1 = ["1","4","7"]
        col2 = ["2","5","8"]
        col3 = ["3","6","9"]
        dia1 = ["1","5","9"]
        dia2 = ["3","5","7"]
        lst = [row1,row2,row3,col1,col2,col3,dia1,dia2]
        for j in lst:
            xNum = 0
            oNum = 0
            for i in j:
                val = state[i]
                if val == "X":
                    xNum += 1
                if val == "O":
                    oNum += 1
            if xNum == 0 and oNum == 2:
                for k in j:
                    if state[k] == " ":
                        return k

    def findNoWin(self):
        state = self.board
        row1 = ["1","2","3"]
        row2 = ["4","5","6"]
        row3 = ["7","8","9"]
        col1 = ["1","4","7"]
        col2 = ["2","5","8"]
        col3 = ["3","6","9"]
        dia1 = ["1","5","9"]
        dia2 = ["3","5","7"]
        lst = [row1,row2,row3,col1,col2,col3,dia1,dia2]
        for j in lst:
            xNum = 0
            oNum = 0
            for i in j:
                val = state[i]
                if val == "X":
                    xNum += 1
                if val == "O":
                    oNum += 1
            if xNum == 1 and oNum == 1:
                for k in j:
                    if state[k] == " ":
                        return k

    def checkEmpty(self) -> list:
        """Check the board and return empty a list of string of numbers for spaces in board (1-9).
        """
        lst = []
        board = self.board
        for i in range(1,10):
            num = str(i)
            if board[num] == " ":
                lst.append(str(i))
        return lst

    def userMove(self, num):
        """Ask the user for a move and return a dictionary of board.
        """
        lst = self.checkEmpty()
        # print(self.boardGuide())
        while True:
            if num in lst:
                self.board[num] = "X"
                return True
            else:
                print("Wrong Input")
                break
