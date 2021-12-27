import numpy as np
def LCSubStr(X, Y, m, n):

	# Create a table to store lengths of
	# longest common suffixes of substrings.
	# Note that LCSuff[i][j] contains the
	# length of longest common suffix of
	# X[0...i-1] and Y[0...j-1]. The first
	# row and first column entries have no
	# logical meaning, they are used only
	# for simplicity of the program.

	# LCSuff is the table with zero
	# value initially in each cell
	LCSuff = [[0 for k in range(n+1)] for l in range(m+1)]

	# To store the length of
	# longest common substring
	result = 0

	# Following steps to build
	# LCSuff[m+1][n+1] in bottom up fashion
	for i in range(m + 1):
		for j in range(n + 1):
			if (i == 0 or j == 0):
				LCSuff[i][j] = 0
			elif (X[i-1] == Y[j-1]):
				LCSuff[i][j] = LCSuff[i-1][j-1] + 1
				result = max(result, LCSuff[i][j])
			else:
				LCSuff[i][j] = 0
	return result

def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])

if __name__ == "__main__":
    X = 'OldSite:GeeksforGeeks.org'
    Y = 'NewSite:GeeksQuiz.com'

    m = len(X)
    n = len(Y)

    print('Length of Longest Common Substring is',	LCSubStr(X, Y, m, n))


