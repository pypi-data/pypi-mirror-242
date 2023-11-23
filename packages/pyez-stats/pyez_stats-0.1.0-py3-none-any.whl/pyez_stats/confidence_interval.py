import numpy as np
from . import statistic as s
from scipy.stats import chi2

def confidence_interval(Xs: np.ndarray = None, percent = 95, unbiased: bool = False) -> list:
    """
    A function used to calculate a basic confidence region for Gaussian distributed data.

    :param Xs: Gaussian distributed data.
    :type Xs: np.ndarray

    :param percent: Defines on what percent of the distribution do we want our parameter to fall within.
    :type percent: int

    :param unbiased: Used to define if we use an unbiased or biased estimator.
    :type unbiased: bool

    :return: A list representing a confidence interval.
    :rtype: List
    """
    uX: float = s.mean(Xs)
    varX: float = s.variance(Xs, unbiasedVar=unbiased)
    N = len(Xs)

    z: float = s.percentile(percent)
     
    return [uX - z * (np.sqrt(varX/N)), uX + z * (np.sqrt(varX/N))]
    
class ConfidenceInterval:
    """
    Instantiate an object that represents a confidence interval.
    A helper class used in other classes and py files.

    :param Xs: Instance attribute for our data.
    :type Xs: np.ndarray

    :param uX: Optional instance attribute used specify the mean of the distribution.
    :type uX: float

    :param varX: Optional instance attribute used specify the variance of the distribution.
    :type varX: float
    """
     
    def __init__(self, Xs: np.ndarray, uX: float = None, varX: float = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.uX: float = uX
        self.varX: float = varX
        
    def gaussian_confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        A method used to calculate the confidence interval for Gaussian data.

        :param percent: Defines the percentile of the ditribution for where our confidence interval will lie within.
        :type percent: float

        :param parameter: Variable used to define what parameter we want to find the confidence interval for.
        :type parameter: str

        :return: List that has the lower and upper bounds for our confidence interval.
        :rtype: List 
        """
        p = percent * .01
        p = 1 - (1 - p) / 2
        N: int = len(self.Xs)
        z: float = s.percentile(p)

        low: float = self.uX - z * (np.sqrt(self.varX/N))

        high: float = self.uX + z * (np.sqrt(self.varX/N))

        if parameter is None: return f"mean: {[low, high]}"

        if parameter in ("mean", "avg", "mu", "average"): return [low, high]

        if parameter in ("variance", "var"):

            alpha: float = 1 - p

            chi2_lower = chi2.ppf(alpha / 2, N - 1)
            chi2_upper = chi2.ppf(1 - alpha / 2, N - 1)

            ci_lower = ((N - 1) * self.varX) / chi2_upper
            ci_upper = ((N - 1) * self.varX) / chi2_lower
            
            return f"variance: {[ci_lower, ci_upper]}"
        
    def exponential_confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        A method used to calculate the confidence interval for Exponential data.

        :param percent: Defines the percentile of the ditribution for where our confidence interval will lie within.
        :type percent: float

        :param parameter: Variable used to define what parameter we want to find the confidence interval for.
        :type parameter: str

        :return: List that has the lower and upper bounds for our confidence interval.
        :rtype: List 
        """
        p = percent * .01
        p = 1 - (1 - p) / 2
        lamb: float = len(self.Xs) / sum(self.Xs)
        z: float = s.percentile(p)
        N: int = len(self.Xs)
        low: float = lamb / (1 + (z / np.sqrt(N)))
        high: float = lamb / (1 - (z / np.sqrt(N)))
    
        if parameter is None: return f"lambda_hat: {[low, high]}\nmean: {[1 / high, 1 / low]}\nvariance: {[1 / high ** 2, 1 / low ** 2]}"

        if parameter in ("lambda_hat", "theta", "lambda", "lamb", "lamb_hat"): return [low, high]

        if parameter in ("mean", "avg", "mu", "average"): return [1 / high, 1 / low]

        if parameter in ("variance", "var"): return [1 / high ** 2, 1 / low ** 2]
    
    def bernoulli_confidence_interval(self, percent: float = 95, **null) -> list:
        """
        A method used to calculate the confidence interval for Bernoulli data.

        :param percent: Defines the percentile of the ditribution for where our confidence interval will lie within.
        :type percent: float

        :param null: Keyword argument to define multiple parameters.
        :type null: Dictionary

        :return: List that has the lower and upper bounds for our confidence interval.
        :rtype: List 
        """
        p = percent * .01
        p = 1 - (1 - p) / 2
        holder: dict = null
        N: int = len(self.Xs)
        z: float = s.percentile(p)

        low: float = self.uX - z * (np.sqrt(self.varX/N))
        high: float = self.uX + z * (np.sqrt(self.varX/N))

        return [self.uX - z * (np.sqrt(self.varX/N)), self.uX + z * (np.sqrt(self.varX/N))]
    
    def poisson_confidence_interval(self, percent: float = 95, **null) -> list:
        """
        A method used to calculate the confidence interval for Poisson data.

        :param percent: Defines the percentile of the ditribution for where our confidence interval will lie within.
        :type percent: float

        :param null: Keyword argument to define multiple parameters.
        :type null: Dictionary

        :return: List that has the lower and upper bounds for our confidence interval.
        :rtype: List 
        """
        p = percent * .01
        p = 1 - (1 - p) / 2
        N: int = len(self.Xs)
        z: float = s.percentile(p)

        return [self.uX - z * (np.sqrt(self.uX/N)), self.uX + z * (np.sqrt(self.uX/N))]
    
    def binomial_confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        A method used to calculate the confidence interval for Binomial data.

        :param percent: Defines the percentile of the ditribution for where our confidence interval will lie within.
        :type percent: float

        :param null: Variable used to define the parameter we want to find the confidence interval for.
        :type null: str

        :return: List that has the lower and upper bounds for our confidence interval.
        :rtype: List 
        """
        per = percent * .01
        per = 1 - (1 - per) / 2

        p: float = sum(self.Xs) / len(self.Xs)
        N: int = len(self.Xs)
        z: float = s.percentile(per)

        low: float = p - z * (np.sqrt(p*(1-p)/N)) 
        high: float = p + z * (np.sqrt(p*(1-p)/N))

        low = low if low > 0 else 0
        high = high if high < 1 else 1

        low_q: float = 1 - low
        high_q: float = 1 - high

        if parameter is None: return f"p_hat: {[low, high]}\nmean: {[low * N, high * N]}\nvariance: {[low * N * low_q, high * N * high_q]}"

        if parameter in ("p_hat", "theta", "p"): return [low, high]

        if parameter in ("mean", "avg", "mu", "average"): return [low * N, high * N]

        if parameter in ("variance", "var"): return [low * N * low_q, high * N * high_q]
    
    def geometric_confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        A method used to calculate the confidence interval for Geometric data.

        :param percent: Defines the percentile of the ditribution for where our confidence interval will lie within.
        :type percent: float

        :param null: Variable used to define the parameter we want to find the confidence interval for.
        :type null: str

        :return: List that has the lower and upper bounds for our confidence interval.
        :rtype: List 
        """
        per = percent * .01
        per = 1 - (1 - per) / 2

        p: float = 1 / (sum(self.Xs) / len(self.Xs))
        N: int = len(self.Xs)
        z: float = s.percentile(per)

        low: float = p - z * (np.sqrt(p*(1-p)/N))
        high: float = p + z * (np.sqrt(p*(1-p)/N))

        if parameter is None: return f"p_hat: {[low if low > 0 else 0, high]}\nmean: {[1 / high, 1 / low]}\nvariance: {[(1 - high) / high**2, (1 - low) / low**2 ]}"
        
        if parameter in ("p_hat", "theta", "p"): return [low if low > 0 else 0, high]
        
        if parameter in ("mean", "avg", "mu", "average"): return [1 / high, 1 / low]
        
        if parameter in ("variance", "var"): return [(1 - high) / high**2, (1 - low) / low**2]