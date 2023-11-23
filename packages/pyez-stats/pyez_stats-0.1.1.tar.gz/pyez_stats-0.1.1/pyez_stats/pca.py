from . import statistic as s

import numpy as np

class PCA:
    """
    Instantiate principle component analysis object for statistical analysis.

    :param args: Variable amount of arrays of data that represent our design matrix.
    :type args: np.ndarray
    """

    def __init__(self, *args):

        self.args: list = args
        self.X = np.column_stack(args)
        self.N: int = len(args[0])
        self.k: int = len(args)

    def covariance_matrix(self):
        """
        Method used to turn our design matrix into a covariance matrix.

        :return: Matrix of array.
        :rtype: np.ndarray
        """

        ones = np.ones_like(self.args[0])
        I = np.identity(self.N)
        H = I - (1 / self.N) * (ones * ones.T)
        S = (1 / (self.N - 1)) * self.X.T @ H @ self.X
        return S
    
    def spectral_decomposition(self):
        """
        Method used for calculating the eigenvalues and eigenvectors of our design matrix.

        :return: Eigenvalues and eigenvectors of our covariance matrix.
        :rtype: np.ndarray
        """

        cov_mat = self.covariance_matrix()

        eigenvalues, eigenvectors = np.linalg.eigh(cov_mat)

        return eigenvalues, eigenvectors
    
    def explaines_variance_ratio(self) -> list:
        """
        Method that uses eigenvalues to calculate what percent of the variance in our data is caused by a certain variable.

        :return: Array of eigenvalues represented as a percent of the total eigenvalue.
        :rtype: np.ndarray
        """

        eigenvalues: list = self.spectral_decomposition()[0]

        weights: list = eigenvalues / sum(eigenvalues)

        return weights
    
    def largest_influence(self):
        """
        Method that used eigenvectors to calculate which variable causes the largest variance in our design matrix.

        :return: List of manipulated eigenvectors.
        :rtype: np.ndarray
        """

        eigenvectors = abs(self.spectral_decomposition()[1][:,::-1].T)

        inf_vars: list = []

        for i in range(len(eigenvectors)):
            
            col_max: float = max(eigenvectors[i])

            inf_var: int = list(eigenvectors[i]).index(col_max) + 1

            inf_vars.append(inf_var)

        return inf_vars
    
    def __call__(self):

        inf_vars: list = self.largest_influence()

        exp_var_ratio: list = self.explaines_variance_ratio()[::-1]

        for i in range(len(inf_vars)):

            if i is 0:
                print(f"variable {inf_vars[i]} has the lagest influence on the data")
                print(f"About {round(exp_var_ratio[i] * 100, 2)}% of the variance in the data is explained by this variable\n")

            else:
                print(f"variable {inf_vars[i]} has the next lagest influence on the data")
                print(f"About {round(exp_var_ratio[i] * 100, 2)}% of the variance in the data is explained by this variable\n")        

        return 0