from GA import Gen

if __name__ == '__main__':
    n = int(input("Please enter number of rows (or columns) in your table:"))
    n_queen = Gen(n, no_population=50)
    n_queen.evolution()

