import numpy as np
import math

def mean(data: np.ndarray, unbiased: bool = False) -> float:
    """
    Function used to calculate the mean of our data.

    :param data: Array of data.
    :type data: np.ndarray

    :param unbiased: If true calculates an unbiased mean.
    :type unbiased: bool

    :return: Average of our data.
    :rtype: float
    """
    data = np.array(data)
    if unbiased is True:
        N: float = len(data) - 1
    else:
        N: float = len(data)
        
    return data.sum() / N

def variance(data:np.ndarray, unbiasedMu: bool = False, unbiasedVar: bool = False) -> float:
        """
        Function used to calculate the variance of our data.

        :param data: Array of data.
        :type data: np.ndarray

        :param unbiasedMu: If true calculates an unbiased mean.
        :type unbiasedMu: bool

        :param unbiasedVar: If true calculates an unbiased variance.
        :type unbiasedVar: bool

        :return: Variance of our data.
        :rtype: float
        """
        
        if unbiasedVar is True:
            N: float = len(data) - 1
        else:
            N: float = len(data)

        mu = mean(data, unbiasedMu)
        sumOfSq: float = 0
        for n in data:
            sumOfSq += (n - mu) ** 2
        sX: float = sumOfSq / (N)
        return sX

def covariance(Xs: np.ndarray = None, Ys: np.ndarray = None, unbiased: bool = False) -> float:
        """
        Function used to calculate the covariance between two arrays.

        :param Xs: Array of data.
        :type Xs: np.ndarray

        :param Ys: Array of data.
        :type Ys: np.ndarray

        :param unbiased: If true calculates a unbiased covariance.
        :type unbiased: bool

        :return: covariance
        :rtype: float
        """
        if len(Xs) != len(Ys):
            return print('X and Y are not the same length')

        N: float = len(Xs) - 1

        uX: float = mean(Xs, unbiased)
        uY: float = mean(Ys, unbiased)

        return sum((Xs - uX) * (Ys - uY)) / N

def correlation(Xs: np.ndarray = None, Ys: np.ndarray = None) -> float:
    """
    Function used to calculate the correlation between two arrays.

    :param Xs: Array of data.
    :type Xs: np.ndarray

    :param Ys: Array of data.
    :type Ys: np.ndarray

    :return: correlation.
    :rtype: float
    """
    Xs = np.array(Xs)
    Ys = np.array(Ys)
    cov: float = covariance(Xs, Ys)
    sigmaX: float = np.sqrt(variance(Xs, unbiasedVar=True))
    sigmaY: float = np.sqrt(variance(Ys, unbiasedVar=True))
    return cov / (sigmaX * sigmaY)

def z_score(Xs: np.ndarray = None) -> float:
    """
    Function that standardizes our data so it fits a standard normal distribution.

    :param Xs: Array of data.
    :type Xs: np.ndarray

    :return: Standardize array of data.
    :rtype: np.ndarray
    """
    uX: float = mean(Xs)
    varX = variance(Xs)
    return [(i - uX) / np.sqrt(varX) for i in Xs]

def phi(x):
    """
    Standard normal PDF (probability density function).

    :param x: value.
    :type x: float

    :return: Probability of standardized value.
    :rtype: float
    """
    return math.exp(-x**2 / 2.0) / math.sqrt(2.0 * math.pi)

def Phi(x):
    """
    Standard normal CDF (cumulative distribution function) using error function.

    :param x: value.
    :type x: float

    :return: cdf of passed value.
    :rtype: float
    """
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def percentile(p, mu=0, sigma=1, tol=1e-5, max_iter=100):
    """
    Function used to calculate the percentile of a value from a Gaussian distribution.

    :param p: Part of distribution we want to find the percentile of.
    :type p: float

    :param mu: Optional mean parameter.
    :type mu: float

    :param sigma: Optional variance parameter.
    :type sigma: float

    :param tol: Tolerance to stop algorithm.
    :type tol: float

    :param max_iter: Parameter used to stop iteration.
    :type max_iter: float

    :return: Percentile of Gaussian distribution.
    :rtype: float
    """

    if p > 1:
        p *= .01
        
    if p < 0 or p > 1:
        raise ValueError("Probability p must be in range [0, 1].")

    x = 0.0

    for _ in range(max_iter):
        x_old = x
        x = x_old - (Phi(x_old) - p) / phi(x_old)
        if abs(x - x_old) < tol:
            break

    return mu + sigma * x

def get_parameter(**null):
    """
    Function used to get a certain parameter.

    :param null: Variable amount of parameters to find.
    :type null: List

    :return: List of parameters.
    :rtype List:
    """

    if any(key in null for key in ("mean", "avg", "mu", "average")):
        matching_keys = [key for key in ("mean", "avg", "mu", "average") if key in null]
        return ["mean", null[matching_keys[0]]]

    if any(key in null for key in ("lambda_hat", "lambda", "lamb", "lamb_hat")):
        matching_keys = [key for key in ("lambda_hat", "lambda", "lamb", "lamb_hat") if key in null]
        return ["lamb_hat", null[matching_keys[0]]]

    if any(key in null for key in ("variance", "var")):
        matching_keys = [key for key in ("variance", "var") if key in null]
        return ["var", null[matching_keys[0]]]

    if "p_hat" in null:

        return ["p_hat", null["p_hat"]]
    
    else:
        return False