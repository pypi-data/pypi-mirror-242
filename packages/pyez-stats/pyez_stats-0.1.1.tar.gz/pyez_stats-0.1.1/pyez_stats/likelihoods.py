import numpy as np
#import statistic as s
import math
#import ez_stats.confidence_interval as ci

class GaussianLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """

    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = Xs
        self.N: int = len(Xs)

    def maximaximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """

        mu: float = sum(self.Xs) / len(self.Xs)
        var: float = sum((self.Xs - mu) ** 2) / len(self.Xs)

        return mu, var
    
    def likelihood_function(self, mu: float = None, var: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param mu: Used to pass a population mean into the likelihood function.
        :type mu: float

        :param var: Used to pass a population variance into the likelihood function.
        :type var: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """

        if mu is None and var is None:
            mu, var = self.maximaximum_likelihood_estimator()
            return (1 / (np.sqrt(2 * np.pi * var)))**self.N * np.exp(-np.sum((self.Xs - mu)**2) / (2 * var))
        
        elif mu is None and var is not None:
            mu: float = self.maximaximum_likelihood_estimator()[0]
            return (1 / (np.sqrt(2 * np.pi * var)))**self.N * np.exp(-np.sum((self.Xs - mu)**2) / (2 * var))
        
        elif mu is not None and var is None:

            var: float = self.maximaximum_likelihood_estimator()[1]

            if isinstance(mu, (int, float)):
                return (1 / (np.sqrt(2 * np.pi * var)))**self.N * np.exp(-np.sum((self.Xs - mu)**2) / (2 * var))
            
            elif isinstance(mu, (list, tuple, np.ndarray)):

                return np.array([(1 / (np.sqrt(2 * np.pi * var)))**self.N * np.exp(-np.sum((self.Xs - i)**2) / (2 * var)) for i in mu])
        
        else:

            if isinstance(mu, (int, float)):
                return (1 / (np.sqrt(2 * np.pi * var)))**self.N * np.exp(-np.sum((self.Xs - mu)**2) / (2 * var))
            
            elif isinstance(mu, (list, tuple, np.ndarray)):
                return np.array([(1 / (np.sqrt(2 * np.pi * var)))**self.N * np.exp(-np.sum((self.Xs - i)**2) / (2 * var)) for i in mu])
        
    def likelihood_ratio(self, null: float, known_var: float = None) -> float:
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :param known_var: Used to pass our known variance into the function.
        :type known_var: float

        :return: likelihood ratio.
        :rtype: float
        """
        
        return 2 * (np.log(self.likelihood_function(var = known_var)) - np.log(self.likelihood_function(null, var = known_var)))

class BernoulliLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """

    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = np.array(Xs)
        self.N: int = len(Xs)

    def maximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """
        return sum(self.Xs) / self.N
    
    def likelihood_function(self, p: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param p: Used to pass probability p into the likelihood function.
        :type p: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """
        if p is None:
            p = self.maximum_likelihood_estimator()
            return p ** sum(self.Xs) * (1 - p) ** (self.N - sum(self.Xs))
        
        else:
            return p ** sum(self.Xs) * (1 - p) ** (self.N - sum(self.Xs))
        
    def likelihood_ratio(self, null: float):
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :return: likelihood ratio.
        :rtype: float
        """
        return 2 * (np.log(self.likelihood_function()) - np.log(self.likelihood_function(null)))

class ExponentialLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """

    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = Xs
        self.N: int = len(Xs)

    def maximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """
        return 1 / np.mean(self.Xs)

    def likelihood_function(self, lamb: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param lamb: Used to pass parameter lamb into the likelihood function.
        :type lamb: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """
        if lamb is None:
            lamb: float = self.maximum_likelihood_estimator()
            return (lamb ** self.N) * np.exp(-lamb * sum(self.Xs))
        
        else:
            return (lamb ** self.N) * np.exp(-lamb * sum(self.Xs))
        
    def likelihood_ratio(self, null: float):
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :return: likelihood ratio.
        :rtype: float
        """
        return 2 * (np.log(self.likelihood_function()) - np.log(self.likelihood_function(null)))
    
class PoissonLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """
    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = Xs
        self.N: int = len(Xs)

    def maximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """
        return np.sum(self.Xs) / self.N
    
    def likelihood_function(self, lamb: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param lamb: Used to pass parameter lamb into the likelihood function.
        :type lamb: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """
        sumX = sum(self.Xs)
        prod_fact: int = 1
        for x in self.Xs:
            prod_fact *= math.factorial(x)

        if lamb is None:
            lamb: float = self.maximum_likelihood_estimator()
            return np.prod(np.exp(-lamb) * lamb**self.Xs / np.array([np.math.factorial(x) for x in self.Xs]))
        
        else:
            return np.prod(np.exp(-lamb) * lamb**self.Xs / np.array([np.math.factorial(x) for x in self.Xs]))
        
    def likelihood_ratio(self, null: float):
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :return: likelihood ratio.
        :rtype: float
        """
        return 2 * (np.log(self.likelihood_function()) - np.log(self.likelihood_function(null)))
    
class UniformLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """
    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = Xs
        self.N: int = len(Xs)

    def maximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """
        return np.max(self.Xs)
    
    def likelihood_function(self, theta: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param theta: Used to pass parameter theta into the likelihood function.
        :type theta: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """
        if theta is None:
            theta: float = self.maximum_likelihood_estimator()
            return 1 / (theta ** self.N)
        
        else:
            return 1 / (theta ** self.N)
        
    def likelihood_ratio(self, null: float):
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :return: likelihood ratio.
        :rtype: float
        """
        return 2 * (np.log(self.likelihood_function()) - np.log(self.likelihood_function(null)))
    
class BinomialLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """
    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = Xs
        self.N: int = len(Xs)

    def maximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """
        return sum(self.Xs) / len(self.Xs)
    
    def likelihood_function(self, p: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param p: Used to pass probability p into the likelihood function.
        :type p: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """
        if p is None:
            p: float = self.maximum_likelihood_estimator()
            return p ** sum(self.Xs) * (1 - p) ** (sum(1 - self.Xs))
        
        else:
            return p ** sum(self.Xs) * (1 - p) ** (sum(1 - self.Xs))
        
    def likelihood_ratio(self, null: float):
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :return: likelihood ratio.
        :rtype: float
        """
        return 2 * (np.log(self.likelihood_function()) - np.log(self.likelihood_function(null)))
    
class GeometricLikelihood:
    """
    Instantiate object to calculate our likelihood.

    :param Xs: Array of data.
    :type Xs: np.ndarray
    """

    def __init__(self, Xs: np.ndarray):
        self.Xs: np.ndarray = Xs
        self.N = len(Xs)

    def maximum_likelihood_estimator(self) -> float:
        """
        Method for calculating out maximum likelihood.

        :return: Maximum likelihood estimator.
        :rtype: float
        """
        x_bar: float = sum(self.Xs) / self.N

        return 1 / x_bar
    
    def likelihood_function(self, p: float = None) -> float:
        """
        Method used to represent our likelihood function.

        :param p: Used to pass probability p into the likelihood function.
        :type p: float

        :return: Calculation from our likelihood function.
        :rtype: float  
        """
        
        if p is None:
            
            p: float = self.maximum_likelihood_estimator()
            return np.prod([p * (1-p)**(x - 1) for x in self.Xs])
        
        elif self.N == 1:

            return p * (1-p)**(self.Xs - 1)
        
        else:
            
            return np.prod([p * (1-p)**(x - 1) for x in self.Xs])
        
    def likelihood_ratio(self, null: float):
        """
        Method for calculating the likelihood ratio between our null and alternative hypothesis.

        :param null: null hypothesis value.
        :type null: float

        :return: likelihood ratio.
        :rtype: float
        """
        return 2 * (np.log(self.likelihood_function()) - np.log(self.likelihood_function(null)))