



class chessboard(object):

    digits = range(1,9)
          
    # lines, columns and square are bitfields of length 9
    lines = columns = squares = 0

    # matrix is a 9x9 matrix of ints between 1 and 9
    matrix   = (array.array('b',[1] * 9),) * 9
    
    def check(self, i, j, val):
        return self.lines[i][val]      \
            and self.columns[j][val]   \
            and self.squares[(j/3)*3+i/3][val]

    def candidates(i,j):
        return filter(lambda val:check(i,j,val), digits)

    def set(self,i,j,val):
        self.matrix[i][j]=val

    def empty(self,i,j):
        val, self.matrix[i][j] = self.matrix[i][j], None
        self.lines[i][val] = 
        self.columns[j][val] = 

    def 
        


