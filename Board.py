from cmu_graphics import *
from PIL import Image

def generateBoard():
    currBoard = [[] for _ in range(4)]

    for row in range(4):
        for col in range(4):
                randomLetter = chr(ord('A')+ randrange(27)%26)
                currBoard[row].append(randomLetter)
    return currBoard



def isLegalBoard(board, legalWords):
    foundWords=set()
    def searchFromSquare(board, word, r, c, seen):
        if word == '':
            return True
        else:
            directions =[(-1,-1),(-1,0),(-1,1),
                         (0,-1),(0,1),
                         (1,-1),(1,0),(1,1)]
            for dx, dy in directions:
                tr, tc = r+dx,c+dy
                if 0<=tr<4 and 0<=tc<4 and board[tr][tc]==word[0] and (tr,tc) not in seen:
                    sol = searchFromSquare(board,word[1:],tr,tc, seen|{(tr,tc)})
                    if sol == True: return sol
        return False
    #go through each square to see if the word can be formed there
    def inBoard(board, word):
        for row in range(4):
            for col in range(4):
                if board[row][col] == word[0]:
                    if searchFromSquare(board, word[1:], row, col, {(row,col)})==True:
                        return True
        return False
    for word in legalWords:
        word = word.upper()
        if 2<len(word)<11 and inBoard(board,word) and word not in foundWords:
            foundWords.add(word)
    return (board,foundWords)

def makeLegalBoard(board, legalWords):
    while True:
        board, foundWords = isLegalBoard(generateBoard(), legalWords)
        if len(foundWords) >120:
            return board, foundWords


