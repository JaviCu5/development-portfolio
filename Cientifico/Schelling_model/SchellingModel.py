lateral_size = 50
size = lateral_size*lateral_size

occupancy = 0.8

satisfaction = 0.3

white_ratio = 0.5
black_ratio = 1.-white_ratio

def sum_eight_neighbors(matrix, row, col):
      rows, cols = len(matrix), len(matrix[0])
      total = []
      
      for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                  if (0 <= i < rows and 0 <= j < cols) and (i != row or j != col):
                        total.append(matrix[i][j])
      return total

# Example of use:
matrix = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9]
]
row = 2
column = 2

neighbors = sum_eight_neighbors(matrix, row, column)
print(neighbors)
