import numpy as np
import math

from . import statistic as s
from . import confidence_interval as ci
from . import likelihoods as ll
            
class Gaussian(ll.GaussianLikelihood):
    """
    Instantiate an object that represents a Gaussian distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        super().__init__(Xs)
        self.Xs: np.ndarray = np.array(Xs)
        self.muX: float = sum(Xs) / len(Xs)
        self.N: int = len(Xs)
        self.var_theta_hat: float = self.var_mu_hat

    def __repr__(self) -> str:
        return f"Gaussian"
    
    def mean(self) -> float:
        """
        Method used to calculate the mean of our provided data.

        :return: Mean of the data.
        :rtype: float 
        """
        return self.muX

    def var(self, unbiasedVar: bool = False) -> float:
        """
        Method for calculating the variance of a distribution.

        :param unbiasedVar: Used to specify if we want our variance to be biased or unbiased.
        :type unbiasedVar: bool

        :return: Variance of our data.
        :rtype: float
        """
        if unbiasedVar is True:
            N: float = len(self.Xs) - 1
        else:
            N: float = len(self.Xs)

        mu = self.muX
        sumOfSq: float = 0
        for n in self.Xs:
            sumOfSq += (n - mu) ** 2
        sX: float = sumOfSq / (N)
        return sX
    
    def skewness(self) -> float:
        """
        Method that calculates the skewness of our distribution.

        :return: The skewness of our distribution.
        :rtype: float
        """

        std_dev: float = np.sqrt(self.var(unbiasedVar=True))

        return (self.N / ((self.N - 1) * (self.N - 2))) * np.sum(((self.Xs - self.muX) / std_dev) ** 3)
    
    def kurtosis(self) -> float:
        """
        Method that calculates the kurtosis of our distribution.

        :return: Kurtosis of our data.
        :rtype: float
        """

        std_dev: float = np.sqrt(self.var(unbiasedVar=True))

        return ((self.N * (self.N + 1)) / ((self.N - 1) * (self.N - 2) * (self.N - 3))) * \
                     np.sum(((self.Xs - self.muX) / std_dev) ** 4) - \
                     (3 * (self.N - 1) ** 2) / ((self.N - 2) * (self.N - 3))        
    
    def var_mu_hat(self) -> float:
        """
        Helper function used to calculate the variance hat of our data.

        :return: Variance hat used for calculations in other methods.
        :rtype: float
        """
        return self.var() / self.N
    
    def fisher_information(self) -> float:
        """
        Method that calculates the mean fisher information of our data.

        :return: Mean fisher information.
        :rtype: float
        """
        return 1 / self.var()
    
    def var_fisher_information(self) -> float:
        """
        Method that calculates the variance fisher information for our data.

        :return: Variance of the fisher information.
        :rtype: float
        """
        return 1 / 2 * (self.var() ** 2) 
    
    def _gaussian_pdf(self, value: float, mu: float = None, var: float = None) -> float:
        """
        Abstract method used to hold the formula for our pdf.

        :param value: Value we want to calculate the probability of occurring.
        :type value: float

        :param mu: Optional mean parameter.
        :type mu: float

        :param var: Optional var parameter.
        :type var: float

        :return: Probability calculation for our passed value.
        :rtype: float
        """

        if mu is None and var is None:

            return ( 1 / np.sqrt(2 * self.var() * np.pi)) * np.exp(-((value - self.muX)**2) / (2 * self.var()))
        
        if mu is not None and var is None:

            return ( 1 / np.sqrt(2 * self.var() * np.pi)) * np.exp(-((value - mu)**2) / (2 * self.var()))
        
        if mu is None and var is not None:

            return ( 1 / np.sqrt(2 * var * np.pi)) * np.exp(-((value - self.muX)**2) / (2 * var))
        
        if mu is not None and var is not None:

            return ( 1 / np.sqrt(2 * var * np.pi)) * np.exp(-((value - mu)**2) / (2 * var))
    
    def _gaussian_cdf(self, value, test_statistic: bool = False) -> float:
        """
        Abstract method used to hold the formula for our cdf.

        :param value: Value we want to calculate the probability of events occurring up to.
        :type value: float

        :param test_statistic: Used to signify if this function is being called from the Hypothesis Testion class.
        :type test_statistic: bool

        :return: Probability calculation for our passed value.
        :rtype: float
        """
        if test_statistic is False:
            z = (value - self.muX) / np.sqrt(self.var() * 2)
            return 0.5 * (1.0 + math.erf(z))
        
        else:
            
            return 0.5 * (1.0 + math.erf(value / np.sqrt(2)))
    
    def _gaussian_percentile(self, percent: int, tol: float = 1e-5, max_iter: int = 100) -> float:
        """Approximate the quantile function using the Newton-Raphson method.
        
        :param percent: used to specify where on the distribution we want to calculate the distribution of.
        :type percent: float

        :param tol: Tolerance used stop iteration.
        :type tol: float

        :param max_iter: Max amount of iterations possible.
        :type max_iter: int

        :return: Percentile of our Gaussian Distribution.
        :rtype: float
        """
        percent = percent * .01
        if percent < 0 or percent > 1:
            raise ValueError("Probability p must be in range [0, 1].")

        x = self.mean()

        for _ in range(max_iter):
            x_old = x
            x = x_old - (self._gaussian_cdf(x_old) - percent) / self._gaussian_pdf(x_old)
            
            if abs(x - x_old) < tol:
                break

        return x
        
    def pdf(self, value: float = None, mu: float = None, var: float = None) -> float:
        """
        Method used to calculate the probability density function for Gaussian data.

        :param value: Value we want to find the probability of.
        :type value: float

        :param mu: Optional parameter if the population mean is known.
        :type mu: float

        :param var: Optional parameter if the population variance is known.
        :type var: float

        :return: Probability of passed value.
        :rtype: float
        """

        if isinstance(value, (int, float)):
            return self._gaussian_pdf(value, mu, var)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            return [self._gaussian_pdf(i, mu, var) for i in value]
        
        else:
            return [self._gaussian_pdf(i, mu, var) for i in self.Xs]

        
    def cdf(self, value = None) -> float:
        """
        Method used to calculate the cdf of passed values.

        :param value: Value we want to find the cumulative probability of.
        :type value: float

        :return: Cdf of a Gaussian distribution.
        :rtype: float
        """
        
        if isinstance(value, (int, float)):
            return self._gaussian_cdf(value)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            return [self._gaussian_cdf(i) for i in value]
        
        else:
            return [self._gaussian_cdf(i) for i in self.Xs]
        
    def percentile(self, percent: float = None, standardize: bool = False) -> float:
        """
        Calculate the percentile of a Gaussian distribution.

        :param percent: Specify the percentile of the distribution we want to find the value of.
        :type percent: float

        :param standardize: If True calculates the percentile of the standard normal distribution.
        :type standardize: bool

        :return: Percent of the Gaussian distribution.
        :rtype: float
        """
        mu: float = self.mean()
        std: float = np.sqrt(self.var())

        if isinstance(percent, (int, float)):

            if standardize is False:
                return self._gaussian_percentile(percent)
            
            else:
                return (self._gaussian_percentile(percent) - mu) / std
        
        elif isinstance(percent, (list, tuple, np.ndarray)):

            if standardize is False:
                return [self._gaussian_percentile(i) for i in percent]
            
            else:
                return [(self._gaussian_percentile(i) - mu) / std for i in percent]
        
        else:

            if standardize is False:
                return self._gaussian_percentile(95)
            
            else:

                return (self._gaussian_percentile(95) - mu) / std
        
    def confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        Uses ConfidenceInterval class to calculate the confidence interval of Gaussian data.

        :param percent: Defines the percent of the distribution we want to calculate the confidence interval for.
        :type percent: float

        :param parameter: Optional used to define a specific parameter or not.
        :type parameter: str

        :return: Confidence interval for Gaussian distributed data.
        :rtype: ConfidenceInterval
        """
        return ci.ConfidenceInterval(self.Xs, self.muX, self.var()).gaussian_confidence_interval(percent, parameter)
    
class Exponential(ll.ExponentialLikelihood):
    """
    Instantiate an object that represents a Exponential distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        super().__init__(Xs)
        self.Xs: np.ndarray = np.array(Xs)
        self.N: int = len(Xs)
        self.var_theta_hat: float = self.var_lamb_hat

    def __repr__(self) -> str:
        return f"Exponential"
    
    def lamb_hat(self) -> float:
        """
        Calculates the lambda parameter (which usually represents the arrival rate) for the distribution.

        :return: Lambda parameter.
        :rtype: float
        """
        return self.N / sum(self.Xs)
    
    def mean(self, lamb: float = None) -> float:
        """
        Calculates the average of our exponential data.
        Optional parameter lambda id we know the parameter of our distribution.

        :param lamb: Parameter of our distribution.
        :type lamb: float

        :return: Average of our random exponential data
        :rtype: float
        """
        if lamb is None:
            return 1 / self.lamb_hat()
        else:
            return 1 / lamb
        
    def median(self, lamb: float = None) -> float:
        """
        Calculates the median of our random exponential data.

        :param lamb: Optional parameter used if the population lambda is known.
        :type lamb: float

        :return: Median of random exponential data.
        :rtype: float
        """
        if lamb is None:
            return np.log(2) / self.lamb_hat()
        else:
            return np.log(2) / self.lamb
    
    def var(self, lamb: float = None) -> float:
        """
        Calculates the variance of random exponential data.

        :param lamb: Optional parameter used if the population lamb is known.
        :type lamb: float

        :return: Variance of random exponential data.
        :rtype: float
        """
        if lamb is None:
            return 1 / (self.lamb_hat() ** 2)
        else:
            return 1 / (lamb ** 2)
        
    def skewness(self) -> int:
        """
        Skewness of our exponential distribution.

        :return: Skewness of our exponential distribution.
        :rtype: int
        """
        return 2
    
    def kurtosis(self) -> int:
        """
        kurtosis of our exponential distribution.

        :return: kurtosis of our exponential distribution.
        :rtype: int
        """

        return 6
        
    def var_lamb_hat(self) -> float:
        """
        Calculates the variance in our estimator parameter.

        :return: Variance in our parameter lambda hat.
        :rtype: float
        """

        return self.lamb_hat() ** 2 / self.N
    
    def fisher_information(self) -> float:
        """
        Returns fisher information to be used in other calculations in this library.

        :return: Fisher information of our data.
        :rtype: float
        """
        return self.N / self.lamb_hat() ** 2
    
    def _exponential_pdf(self, value: float, lamb: float = None) -> float:
        """
        A abstract method used to hold the formula for an exponential pdf.

        :param value: Value we want to find the probability of.
        :type value: float

        :param lamb: Optional parameter if lambda parameter is known.
        :type lamb: float

        :return: Probability of value passed.
        :rtype: float
        """
        if lamb is None:
            return self.lamb_hat() * np.exp(-self.lamb_hat() * value)
        else:
            return lamb * np.exp(-lamb * value)
    
    def _exponential_cdf(self, value: float, lamb: float = None) -> float:
        """
        A abstract method used to hold the formula for an exponential cdf.

        :param value: Value we want to find the cumulative probability of.
        :type value: float

        :param lamb: Optional parameter if lambda parameter is known.
        :type lamb: float

        :return: Cumulative probability of value passed.
        :rtype: float
        """
        if lamb is None:
            return 1 - np.exp(-self.lamb_hat() * value)
        else:
            return 1 - np.exp(-lamb * value)
        
    def _exponential_percentile(self, percent: float, lamb: float = None) -> float:
        """
        Calculates value at the passed percent of our distribution.

        :param percent: percentage point on our distribution we want to find the percentage of.
        :type percent: float

        :param lamb: Optional if population parameter is known.
        :type lamb: float

        :return: Percentile of exponential distribution.
        :rtype: float
        """

        if lamb is None:
            return -np.log(1 - percent) / self.lamb_hat()
        
        else:
            return -np.log(1 - percent) / lamb
    
    def pdf(self, value: float = None, lamb: float = None) -> float:
        """
        Method used to call abstract pdf formula.

        :param value: Value we want to find the probability of.
        :type value: float

        :param lamb: Optional parameter if population lambda is known.
        :type lamb: float

        :return: Probability of certain value.
        :rtype: float 
        """

        if isinstance(value, (int, float)):
            return self._exponential_pdf(value, lamb)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            return [self._exponential_pdf(i, lamb) for i in value]
        
        else:
            return [self._exponential_pdf(i, lamb) for i in self.Xs]

        
    def cdf(self, value: float = None, lamb: float = None) -> float:
        """
        Method used to call abstract cdf formula.

        :param value: Value we want to find the cumulative probability of.
        :type value: float

        :param lamb: Optional lambda parameter if population lambda is known.
        :type lamb: float

        :return: Cumulative probability of certain value.
        :rtype: float
        """
        if isinstance(value, (int, float)):
            return self._exponential_cdf(value, lamb)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            return [self._exponential_cdf(i, lamb) for i in value]
        
        else:
            return [self._exponential_cdf(i, lamb) for i in self.Xs]

    def percentile(self, percent: float, lamb: float = None) -> float:
        """
        Method used to call other abstract method for calculating the percentile of our distribution.

        :param percent: Where on our distribution we want to find the percentile of.
        :type percent: float

        :param lamb: Optional lambda parameter if population lambda hat is known.
        :type lamb: float

        :return: Percentile of the distribution.
        :rtype: float
        """
        if isinstance(percent, (int, float)):
            return self._exponential_percentile(percent, lamb)
        
        elif isinstance(percent, (list, tuple, np.ndarray)):
            return [self._exponential_percentile(i, lamb) for i in percent]
        
        else:
            return f"you must enter a percent that is a int, float, list or tuple"
        
    def confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        Uses exponential confidence interval from our confidence interval class to calculate the confidence interval of our distribution.

        :param percent: Defines the percent of the distribution we want to calculate the confidence interval for.
        :type percent: float

        :param parameter: Optional used to define a specific parameter or not.
        :type parameter: str

        :return: Confidence interval for Exponentially distributed data.
        :rtype: ConfidenceInterval
        """
        return ci.ConfidenceInterval(self.Xs, self.lamb_hat(), self.var()).exponential_confidence_interval(percent, parameter)
    
class Bernoulli(ll.BernoulliLikelihood):
    """
    Instantiate an object that represents a Bernoulli distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        super().__init__(Xs)
        self.Xs: np.ndarray = np.array(Xs)
        self.N: int = len(Xs)
        self.var_theta_hat: float = self.var_p_hat

    def __repr__(self) -> str:
        return f"Bernoulli"

    def p_hat(self) -> float:
        """
        Method used to calculate the p parameter for our bernoulli data.

        :return: p parameter.
        :rtype: float
        """
        return sum(self.Xs) / self.N
    
    def mean(self, p: float = None) -> float:
        """
        Calculate the mean for our bernoulli data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Mean of our Bernoulli distribution.
        :rtype: float
        """
        if p is None:
            return self.p_hat()
        
        else:
            return p
    
    def var(self, p: float = None) -> float:
        """
        Calculates the variance of our bernoulli data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Variance of our data.
        :rtype: float
        """
        if p is None:
            return self.p_hat() * (1 - self.p_hat())
        
        else:
            return p * (1 - p)
        
    def skewness(self, p: float = None) -> float:
        """
        Calculates the skewness of our data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Skewness of our data.
        :rtype: float
        """

        if p is None:

            p: float = self.p_hat()
            q: float = 1 - p

            return (q - p) / np.sqrt(p * q)
        
        else:

            q: float = 1 - p

            return (q - p) / np.sqrt(p * q)
        
    def kurtosis(self, p: float = None) -> float:
        """
        Calculates the kurtosis of our data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Kurtosis of our data.
        :rtype: float
        """

        if p is None:

            p: float = self.p_hat()
            q: float = 1 - p

            return (1 - 6*p*q) / p*q
        
        else:

            q: float = 1 - p

            return (1 - 6*p*q) / p*q   
        
    def var_p_hat(self) -> float:
        """
        Variance of our parameter p.

        :return: Variance of our parameter.
        :rtype: float
        """
        return (self.p_hat() * (1 - self.p_hat())) / self.N
    
    def fisher_information(self, p: float = None) -> float:
        """
        Calculates the fisher information of our data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Returns the fisher information.
        :rtype: float
        """
        if p is None:
            return 1 / (self.p_hat() * (1 - self.p_hat()))
        
        else:
            return 1 / (p * (1 - p))
    
    def _bernoulli_pmf(self, value: float, p: float = None) -> float:
        """
        Abstract method used to hold the formula for our pmf.

        :param value: Value we want to find the probability of occuring.
        :type value: float

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Probability of certain value.
        :rtype: float
        """
        if p == None:
            return (self.p_hat() ** value) * (1 - self.p_hat()) ** (1 - value)
        
        else:
            return (p ** value) * (1 - p) ** (1 - value)
        
    def pmf(self, value: float = None, p: float = None) -> float:
        """
        Method used to call abstract method of pmf formula.

        :param value: Value we want to find the probability of occuring.
        :type value: float

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Probability of certain value.
        :rtype: float
        """
        if isinstance(value, (int, float)):
            return self._bernoulli_pmf(value, p)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            ber_list = [self._bernoulli_pmf(i, p) for i in value]
            ber_array = np.array(ber_list)
            return np.prod(ber_array)
        
        else:
            ber_list = [self._bernoulli_pmf(i, p) for i in self.Xs]
            ber_array = np.array(ber_list)
            return np.prod(ber_array)
        
    def confidence_interval(self, percent: float = 95, **null) -> list:
        """
        Uses Bernoulli confidence interval from our confidence interval class to calculate the confidence interval of our distribution.

        :param percent: Defines the percent of the distribution we want to calculate the confidence interval for.
        :type percent: float

        :param null: Optional used to define a specific parameter or not.
        :type null: Dictionary

        :return: Confidence interval for Exponentially distributed data.
        :rtype: ConfidenceInterval
        """
        return ci.ConfidenceInterval(self.Xs, self.p_hat(), self.var()).bernoulli_confidence_interval(percent, **null)
    
class Poisson(ll.PoissonLikelihood):
    """
    Instantiate an object that represents a Poisson distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        super().__init__(Xs)
        self.Xs: np.ndarray = np.array(Xs)
        self.N: int = len(Xs)
        self.var_theta_hat: float = self.var_lamb_hat

    def __repr__(self) -> str:
        return f"Poisson"

    def lamb_hat(self) -> float:
        """
        Calculates the lambda parameter for the distribution.

        :return: Lambda parameter.
        :rtype: float
        """
        return s.mean(self.Xs)
    
    def mean(self, lamb: float = None) -> float:
        """
        Calculates the average of our Poisson data.
        Optional parameter lambda if we know the parameter of our distribution.

        :param lamb: Parameter of our distribution.
        :type lamb: float

        :return: Average of our random Poisson data
        :rtype: float
        """
        if lamb is None:
            return self.lamb_hat()
        
        else:
            return lamb
    
    def var(self, lamb: float = None) -> float:
        """
        Calculates the variance of random Poisson data.

        :param lamb: Optional parameter used if the population lamb is known.
        :type lamb: float

        :return: Variance of random Poisson data.
        :rtype: float
        """
        if lamb is None:
            return self.lamb_hat()
        
        else:
            return lamb
        
    def var_lamb_hat(self) -> float:
        """
        Calculates the variance in our estimator parameter.

        :return: Variance in our parameter lambda hat.
        :rtype: float
        """
        return self.lamb_hat() / self.N
    
    def fisher_information(self, lamb: float = None) -> float:
        """
        Returns fisher information to be used in other calculations in this library.

        :param lamb: Optional parameter used if the population lamb is known.
        :type lamb: float

        :return: Fisher information of our data.
        :rtype: float
        """
        if lamb is None:
            return 1 / self.lamb_hat()
        
        else:
            return 1 / lamb
    
    def skewness(self) -> float:
        """
        Method that calculates the skewness of our distribution.

        :return: The skewness of our distribution.
        :rtype: float
        """
        return 1 / np.sqrt(self.lamb_hat())
    
    def kurtosis(self) -> float:
        """
        kurtosis of our exponential distribution.

        :return: kurtosis of our exponential distribution.
        :rtype: int
        """
        return 1 / self.lamb_hat()

    def _poisson_pmf(self, value: float = None, lamb: float = None) -> float:
        """
        A abstract method used to hold the formula for an Poisson pmf.

        :param value: Value we want to find the probability of.
        :type value: float

        :param lamb: Optional parameter if lambda parameter is known.
        :type lamb: float

        :return: Probability of value passed.
        :rtype: float
        """
        if lamb is None:
            return ((self.lamb_hat() ** value) * np.exp(-self.lamb_hat())) / math.factorial(value)
        
        else:
            return ((lamb ** value) * np.exp(-lamb)) / math.factorial(value)
        
    def _poisson_cdf(self, value: float = None, lamb: float = None) -> float:
        """
        A abstract method used to hold the formula for an poisson cdf.

        :param value: Value we want to find the cumulative probability of.
        :type value: float

        :param lamb: Optional parameter if lambda parameter is known.
        :type lamb: float

        :return: Cumulative probability of value passed.
        :rtype: float
        """
        if lamb is None:
            cdf = 0
            for k in range(value + 1):
                cdf += np.exp(-self.lamb_hat()) * self.lamb_hat() ** k / math.factorial(k)
            return cdf

        else:
            cdf = 0
            for k in range(value + 1):
                cdf += np.exp(-lamb) * lamb ** k / math.factorial(k)
            return cdf
        
    def pmf(self, value: float = None, lamb: float = None) -> float:
        """
        Method used to call abstract pmf formula.

        :param value: Value we want to find the probability of.
        :type value: float

        :param lamb: Optional parameter if population lambda is known.
        :type lamb: float

        :return: Probability of certain value.
        :rtype: float 
        """

        if isinstance(value, (int, float)):
            return self._poisson_pmf(value, lamb)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            return [self._poisson_pmf(i, lamb) for i in value]
        
        else:
            return [self._poisson_pmf(i, lamb) for i in self.Xs]
        
    def cdf(self, value: float = None, lamb: float = None) -> float:
        """
        Method used to call abstract cdf formula.

        :param value: Value we want to find the cumulative probability of.
        :type value: float

        :param lamb: Optional lambda parameter if population lambda is known.
        :type lamb: float

        :return: Cumulative probability of certain value.
        :rtype: float
        """
        if isinstance(value, (int, float)):
            return self._poisson_cdf(value, lamb)
        
        elif isinstance(value, (list, tuple, np.ndarray)):
            return [self._poisson_cdf(i, lamb) for i in value]
        
        else:
            return [self._poisson_cdf(i, lamb) for i in self.Xs]
        
    def confidence_interval(self, percent: float = 95, **null) -> list:
        """
        Uses poisson confidence interval from our confidence interval class to calculate the confidence interval of our distribution.

        :param percent: Defines the percent of the distribution we want to calculate the confidence interval for.
        :type percent: float

        :param null: Optional used to define a specific parameter or not.
        :type null: Dictionary

        :return: Confidence interval for Exponentially distributed data.
        :rtype: ConfidenceInterval
        """
        return ci.ConfidenceInterval(self.Xs, self.lamb_hat(), self.lamb_hat()).poisson_confidence_interval(percent, **null)
    
class Binomial(ll.BinomialLikelihood):
    """
    Instantiate an object that represents a Binomial distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.
    Note we us np.random.binomial(1, p, size) to get random data for this, it is important that the first parameter is 1 or else the calculations will be wrong

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.N: float = None if Xs is None else len(self.Xs)
        self.var_theta_hat: float = self.var_p_hat

    def __repr__(self) -> str:
        return f"Binomial"

    def p_hat(self) -> float:
        """
        Method used to calculate the p parameter for our binomial data.

        :return: p parameter.
        :rtype: float
        """
        return sum(self.Xs) / len(self.Xs)
    
    def mean(self, p: float = None) -> float:
        """
        Calculate the mean for our Binomial data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Mean of our Binomial distribution.
        :rtype: float
        """
        if p is None:
            return self.N * self.p_hat()
        
        else:
            return self.N * p
    
    def var(self, p: float = None) -> float:
        """
        Calculates the variance of our Binomial data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Variance of our data.
        :rtype: float
        """
        if p is None:
            q: float = 1 - self.p_hat()
            return self.N * self.p_hat() * q
        
        else:
            q: float = 1 - p
            return self.N * p * q
        
    def var_p_hat(self) -> float:
        """
        Variance of our parameter p.

        :return: Variance of our parameter.
        :rtype: float
        """
        return (self.p_hat() * (1 - self.p_hat())) / self.N
    
    def fisher_information(self, p: float = None) -> None:
        """
        Calculates the fisher information of our data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Returns the fisher information.
        :rtype: float
        """
        if p is None:
            return 1 / (self.p_hat() * (1 - self.p_hat()))
        
        else:
            return 1 / (p * (1 - p))
        
    def skewness(self) -> float:
        """
        Calculates the skewness of our data.

        :return: Skewness of our data.
        :rtype: float
        """
        q: float = 1 - self.p_hat()
        return (q - self.p_hat()) / np.sqrt(self.var())
    
    def kurtosis(self) -> float:
        """
        Calculates the kurtosis of our data.

        :return: Kurtosis of our data.
        :rtype: float
        """
        q: float = 1 - self.p_hat()
        return (1 - 6 * self.p_hat * q) / self.var()
    
    def _binomial_pmf(self, k: int = None, p: float = None, n: int = None) -> float:
        """
        Abstract method used to represent our formula for the pmf.

        :param k: number of successes in n trials.
        :type k: int

        :param p: Optional parameter if population p is known.
        :type p: float

        :param n: Number of trials ran in the experiment.
        :type n: int

        :return: Probability of value.
        :rtype: float 
        """

        if n is None:
            
            if p is None:
                return math.comb(self.N, k) * (self.p_hat() ** k) * (1 - self.p_hat()) ** (self.N - k)
            
            else:
                return math.comb(self.N, k) * (p ** k) * (1 - p) ** (self.N - k)
        
        else:

            if p is None:
                return math.comb(n, k) * (self.p_hat() ** k) * (1 - self.p_hat()) ** (n - k)
            
            else:
                return math.comb(n, k) * (p ** k) * (1 - p) ** (n - k)

        
    def pmf(self, k: int = None, p: float = None, n: float = None) -> float:
        """
        Method used to call abstract method that calculates the pmf.

        :param k: number of successes in n trials.
        :type k: int

        :param p: Optional parameter if population p is known.
        :type p: float

        :param n: Number of trials ran in the experiment.
        :type n: int

        :return: Probability of value.
        :rtype: float 
        """

        if isinstance(k, (int, float)):
            return self._binomial_pmf(k, p, n)
        
        elif isinstance(k, (list, tuple, np.ndarray)):
            return [self._binomial_pmf(i, p, n) for i in k]
        
        else:
            return [self._binomial_pmf(i, p, n) for i in range(len(self.Xs))]
        
    def cdf(self, x: int = None, p: float = None, n: float = None) -> float:
        """
        Method used to calculate the cdf of our distribution.

        :param x: number of successes we calculate the cdf of.
        :type x: int

        :param p: Optional parameter if population p is known.
        :type p: float

        :param n: Number of trials ran in the experiment.
        :type n: int

        :return: Cumulative probability of value.
        :rtype: float 
        """

        probability = sum(self.pmf(k, p, n) for k in range(x + 1))
        return probability

    def confidence_interval(self, percent: float = 95, **null) -> list:
        """
        Uses binomial confidence interval from our confidence interval class to calculate the confidence interval of our distribution.

        :param percent: Defines the percent of the distribution we want to calculate the confidence interval for.
        :type percent: float

        :param null: Optional used to define a specific parameter or not.
        :type null: Dictionary

        :return: Confidence interval for Exponentially distributed data.
        :rtype: ConfidenceInterval
        """
        return ci.ConfidenceInterval(self.Xs, self.p_hat(), self.var()).binomial_confidence_interval(percent, **null)
    
class Uniform(ll.UniformLikelihood):
    """
    Instantiate an object that represents a Uniform distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.a: float = sorted(np.array(Xs))[0]
        self.b: float = sorted(np.array(Xs))[-1]
        self.n = sorted(np.array(Xs))[-1] - sorted(np.array(Xs))[0]

    def __repr__(self) -> str:
        return f"Uniform"

    def mean(self) -> float:
        """
        Calculate the mean for our Uniform data.

        :return: Mean of our Uniform distribution.
        :rtype: float
        """
        return (self.a + self.b) / 2
    
    def var(self) -> float:
        """
        Calculate the variance for our Uniform data.

        :return: variance of our uniform distribution.
        :rtype: float
        """
        return self.n * (self.n + 2) / 12
    
    def pdf(self) -> float:
        """
        Calculate the pdf for our Uniform data.

        :return: pdf of our uniform distribution.
        :rtype: float
        """
        return 1 / (self.b - self.a)
    
    def cdf(self, x: float = None):
        """
        Calculate the cdf for our Uniform data.

        :param x: Stopping value of where we want out cdf to be calculated up to.
        :type x: float

        :return: cdf of our uniform distribution.
        :rtype: float
        """
    
        if isinstance(x, (int, float)):
            return (x - self.a) / self.n
        
        elif isinstance(x, (list, tuple, np.ndarray)):
            return [(i - self.a) / self.n for i in x]
        
        else:
            return [(i - self.a) / self.n for i in self.Xs]
        
    def probability_range(self, d: float, c: float):
        """
        Calculate The probability of falling between to values.

        :param d: upper value range.
        :type d: float

        :param c: lower value range.
        :type c: float

        :return: Probability
        :rtype: float
        """
        return (d - c) / self.n
    
class Geometric(ll.GeometricLikelihood):
    """
    Instantiate an object that represents a Geometric distribution.
    Inherits A likelihhod class used for calculations involving maximum likelihood estimation.

    :param Xs: Array used to hold data.
    :type Xs: np.ndarray 
    """

    def __init__(self, Xs: np.ndarray = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.N: int = len(Xs)
        self.var_theta_hat: float = self.var_p_hat

    def __repr__(self) -> str:
        return "Geometric"

    def p_hat(self) -> float:
        """
        Method used to calculate the p parameter for our geometric data.

        :return: p parameter.
        :rtype: float
        """
        return 1 / (sum(self.Xs) / self.N)
    
    def mean(self, p: float = None) -> float:
        """
        Calculate the mean for our geometric data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Mean of our geometric distribution.
        :rtype: float
        """
        if p is None:
            return 1 / self.p_hat()
        
        else:
            return 1 / p
    
    def var(self, p: float = None) -> float:
        """
        Calculates the variance of our geometric data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Variance of our data.
        :rtype: float
        """
        if p is None:
            return (1 - self.p_hat()) / self.p_hat() ** 2
        
        else:
            return (1 - p) / p ** 2
        
    def var_p_hat(self) -> float:
        """
        Variance of our parameter p.

        :return: Variance of our parameter.
        :rtype: float
        """
        return (1 - self.p_hat()) * self.p_hat() **2 / self.N
    
    def fisher_information(self, p: float = None):
        """
        Calculates the fisher information of our data.

        :param p: Optional p parameter if the population parameter is known.
        :type p: float

        :return: Returns the fisher information.
        :rtype: float
        """
        if p is None:
            return 1 / ((self.p_hat() ** 2) * (1 - self.p_hat()) ** 2)
        
        else:
            return 1 / ((p ** 2) * (1 - p) ** 2)
    
    def skewness(self) -> float:
        """
        Calculates the skewness of our data.

        :return: Skewness of our data.
        :rtype: float
        """
        return (2 - self.p_hat()) / (np.sqrt(1 - self.p_hat()))
    
    def kurtosis(self) -> float:
        """
        Calculates the kurtosis of our data.

        :return: Kurtosis of our data.
        :rtype: float
        """
        return 6 + (self.p_hat() ** 2) / (1 - self.p_hat())
    
    def _geometric_pmf(self, k: float = None, p: float = None) -> float:
        """
        Calculates the probability of having a success at trial k.

        :param k: Trial number where there is the first success.
        :type k: int

        :param p: probability of success.
        :type p: float

        :return: Probability of success at kth trial
        :rtype: float
        """
        
        if p is None:
            return self.p_hat() * (1 - self.p_hat()) ** (k - 1)
        
        else:
            return p * (1 - p) ** (k - 1)
            
    def _geometric_cdf(self, k: float = None, p: float = None) -> float:
        """
        Calculates the cumulative probability of up to k trials.

        :param k: Number when there is a success.
        :type k: int

        :param p: probability of success.
        :type p: float

        :return: probability.
        :rtype: float
        """
    
        if p is None:
            return 1 - (1 - self.p_hat()) ** k
        
        else:
            return 1 - (1 - p) ** k
            
    def pmf(self, k: int = None, p: float = None) -> float:
        """
        Method used to call abstract pmf method.

        :param k: Trial number where there is the first success.
        :type k: int

        :param p: probability of success.
        :type p: float

        :return: Probability of success at kth trial
        :rtype: float
        """

        if isinstance(k, (int, float)):
            return self._geometric_pmf(k, p)
        
        elif isinstance(k, (list, tuple, np.ndarray)):
            return [self._geometric_pmf(i, p) for i in k]
        
        else:
            return [self._geometric_pmf(i, p) for i in range(len(self.Xs))]
        
    def cdf(self, k: int = None, p: float = None) -> float:
        """
        Calls abstract method for calculating a cdf.

        :param k: Number when there is a success.
        :type k: int

        :param p: probability of success.
        :type p: float

        :return: probability.
        :rtype: float
        """

        if isinstance(k, (int, float)):
            return self._geometric_cdf(k, p)
        
        elif isinstance(k, (list, tuple, np.ndarray)):
            return [self._geometric_cdf(i, p) for i in k]
        
        else:
            return [self._geometric_cdf(i, p) for i in range(len(self.Xs))]
        
    def confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        Uses geometric confidence interval from our confidence interval class to calculate the confidence interval of our distribution.

        :param percent: Defines the percent of the distribution we want to calculate the confidence interval for.
        :type percent: float

        :param parameter: Optional used to define a specific parameter or not.
        :type parameter: str

        :return: Confidence interval for geometriclly distributed data.
        :rtype: ConfidenceInterval
        """
        return ci.ConfidenceInterval(self.Xs, self.p_hat(), self.var()).geometric_confidence_interval(percent, parameter)
    
class Beta:
    """
    Beta distribution used primarily used as a posterior distribution in our Bayesian statistical model.
    a and b allow us to scale the distribution.

    :param Xs: Array of Data.
    :type: np.ndarray

    :param a: a parameter in Beta distribution.
    :type a: float

    :param b: b parameter in Beta distribution
    :type b: float
    """

    def __init__(self, Xs: np.ndarray, a: float = None, b: float = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.a: float = a
        self.b: float = b

    def __repr__(self) -> str:
        return f"Beta"

    def mean(self, a: float = None, b: float = None) -> float:
        """
        Mean of our Beta distribution.

        :param a: a parameter in Beta distribution.
        :type a: float

        :param b: b parameter in Beta distribution
        :type b: float

        :return: Mean of our distribution.
        :rtype: float
        """

        if a is None and b is None:

            return self.a / (self.a + self.b)
        
        elif a is not None and b is not None:
    
            return a / (a + b)
        
        else:
            raise ValueError("You must define a and b")
        
    def median(self, a: float = None, b: float = None) -> float:
        """
        median of our Beta distribution.

        :param a: a parameter in Beta distribution.
        :type a: float

        :param b: b parameter in Beta distribution
        :type b: float

        :return: median of our distribution.
        :rtype: float
        """

        if a is None and b is None:

            return (self.a - (1/3)) / (self.a + self.b - (2/3))
        
        elif a is not None and b is not None:
    
            return (a - (1/3)) / (a + b - (2/3))
        
        else:
            raise ValueError("You must define a and b")  

    def mode(self, a: float = None, b: float = None) -> float:
        """
        mode of our Beta distribution.

        :param a: a parameter in Beta distribution.
        :type a: float

        :param b: b parameter in Beta distribution
        :type b: float

        :return: mode of our distribution.
        :rtype: float
        """

        if a is None and b is None:

            return (self.a - 1) / (self.a + self.b - 2)
        
        elif a is not None and b is not None:
    
            return (a - 1) / (a + b - 2)
        
        else:
            raise ValueError("You must define a and b")

    def var(self, a: float = None, b: float = None) -> float:
        """
        variance of our Beta distribution.

        :param a: a parameter in Beta distribution.
        :type a: float

        :param b: b parameter in Beta distribution
        :type b: float

        :return: variance of our distribution.
        :rtype: float
        """

        if a is None and b is None:

            return (self.a * self.b) / (self.a + self.b) ** 2 * (self.a + self.b + 1)
        
        elif a is not None and b is not None:
    
            return (a * b) / (a + b) ** 2 * (a + b + 1)
        
        else:
            raise ValueError("You must define a and b")

    def _beta_pdf(self, x: float, a: float = None, b: float = None) -> float:
        """
        abstract method to calculate the pdf of our Beta distribution.
        x is our prior belief about the parameter p, a and b allow us to scale the distribution.

        :param x: Prior belief.
        :type x: float

        :param a: a parameter in Beta distribution.
        :type a: float

        :param b: b parameter in Beta distribution
        :type b: float

        :return: pdf of our distribution.
        :rtype: float
        """
        if a is None and b is None:

            B = (math.gamma(self.a) * math.gamma(self.b)) / math.gamma(self.a + self.b)
            return (x ** (self.a - 1) * (1 - x) ** (self.b - 1)) / B
        
        elif a is not None and b is not None:
    
            B = (math.gamma(a) * math.gamma(b)) / math.gamma(a + b)
            return (x ** (a - 1) * (1 - x) ** (b - 1)) / B
        
        else:
            raise ValueError("You must define a and b")
        
    def pdf(self, x: float = None, a: float = None, b: float = None) -> float:
        """
        Method used to call our abstract method for our pdf.
        x is our prior belief about the parameter p, a and b allow us to scale the distribution.

        :param x: Prior belief.
        :type x: float

        :param a: a parameter in Beta distribution.
        :type a: float

        :param b: b parameter in Beta distribution
        :type b: float

        :return: pdf of our distribution.
        :rtype: float
        """

        if isinstance(x, (int, float)):
            return self._beta_pdf(x, a, b)
        
        elif isinstance(x, (list, tuple, np.ndarray)):
            return [self._beta_pdf(i, a, b) for i in x]
        
        else:
            return [self._beta_pdf(i, a, b) for i in range(len(self.Xs))]
        
class Gamma:
    """
    Gamma distribution used primarily used as a posterior distribution in our Bayesian statistical model.
    a and b allow us to scale the distribution.

    :param Xs: Array of Data.
    :type: np.ndarray

    :param a: a parameter in Beta distribution.
    :type a: float

    :param b: b parameter in Beta distribution
    :type b: float
    """

    def __init__(self, Xs: np.ndarray, a: float = None, b: float = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.a: float = a
        self.b: float = b
        self.theta: float = 1 / b if b is not None else 0
        self.N: int = len(Xs)

    def __repr__(self) -> str:
        return f"Gamma"

    def mean(self, a: float = None, b: float = None) -> float:
        """
        Mean of our Gamma distribution.

        :param a: a parameter in Gamma distribution.
        :type a: float

        :param b: b parameter in Gamma distribution
        :type b: float

        :return: Mean of our distribution.
        :rtype: float
        """
        if a is None and b is None:

            return self.a * self.theta
        
        elif a is not None and b is not None:
    
            return a * (1 / b)
        
        else:
            raise ValueError("You must define a and b")
    
    def var(self, a: float = None, b: float = None) -> float:
        """
        variance of our Gamma distribution.

        :param a: a parameter in Gamma distribution.
        :type a: float

        :param b: b parameter in Gamma distribution
        :type b: float

        :return: variance of our distribution.
        :rtype: float
        """
        if a is None and b is None:

            return self.a * self.theta ** 2
        
        elif a is not None and b is not None:
    
            return a * (1 / b) ** 2
        
        else:
            raise ValueError("You must define a and b")
        
    def _gamma_pdf(self, x: float, a: float = None, b: float = None) -> float:
        """
        abstract method to calculate the pdf of our Gamma distribution.
        x is our prior belief about the parameter p, a and b allow us to scale the distribution.

        :param x: Prior belief.
        :type x: float

        :param a: a parameter in Gamma distribution.
        :type a: float

        :param b: b parameter in Gamma distribution
        :type b: float

        :return: pdf of our distribution.
        :rtype: float
        """

        if a is None and b is None:

            return (x ** (self.a - 1) * np.exp(-self.b * x) * self.b ** self.a) / math.gamma(self.a)
        
        elif a is not None and b is not None:

            return (x ** (a - 1) * np.exp(-b * x) * b ** a) / math.gamma(a)
        
    def pdf(self, x: float = None, a: float = None, b: float = None) -> float:
        """
        Method used to call our abstract method for our pdf.
        x is our prior belief about the parameter p, a and b allow us to scale the distribution.

        :param x: Prior belief.
        :type x: float

        :param a: a parameter in Gamma distribution.
        :type a: float

        :param b: b parameter in Gamma distribution
        :type b: float

        :return: pdf of our distribution.
        :rtype: float
        """

        if isinstance(x, (int, float)):
            return self._gamma_pdf(x, a, b)
        
        elif isinstance(x, (list, tuple, np.ndarray)):
            return [self._gamma_pdf(i, a, b) for i in x]
        
        else:
            return [self._gamma_pdf(i, a, b) for i in range(len(self.Xs))]
        
class Distribution:
    """
    Instatiate object to define and set a defined distribution for analysis on our data.

    :param Xs: Array of our data.
    :type Xs: np.ndarray

    :param model: Model our data fits.
    :type model: str
    """

    def __init__(self, Xs: np.ndarray, model: str = None):

        self.Xs: np.ndarray = Xs
        self.model: str = model

    def distribution(self, dist: str = None):
        """
        Main function used to set our distribution for our data.
        Used match case to find the model we pass in.

        :param dist: Distribution we think our data fits.
        :type dist: str

        :return: Speciefic distribution.
        :rtype: Distribution
        """

        if self.model is None and dist is None:
            return f"You must set a model"
        
        elif self.model is None and dist is not None:
            self.model = dist

        match self.model.lower():

            case "gaussian" | "gauss" | "normal" | "norm" | "gaus":
                return Gaussian(self.Xs)
            
            case "exponential" | "exp":
                return Exponential(self.Xs)
            
            case "bernoulli" | "ber":
                return Bernoulli(self.Xs)
            
            case "poisson" | "poiss" | "pois":
                return Poisson(self.Xs)
            
            case "binomial" | "binom" | "bin":
                return Binomial(self.Xs)
            
            case "uniform" | "uni":
                return Uniform(self.Xs)
            
            case "geometric" | "geom" | "geo":
                return Geometric(self.Xs)