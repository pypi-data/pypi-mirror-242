import numpy as np
from . import statistic as s
from . import distributions as ds
from . import hypothesis_testing as ht
from . import bayesian_statistics as bs
from . import regression as reg
from array import array
from .pca import PCA

class Data:
    """
    Instantiate a Data object.
    Acts as an array with multiple methods for operating on data.

    :param Xs: Data.
    :type Xs: np.ndarray
    """

    def __init__(self, Xs: list):

        self.Xs = np.array(Xs) if isinstance(Xs, (list, array)) else Xs
        self.model = None

        self.gaussian: ds.Gaussian = ds.Gaussian(self.Xs)
        self.bernoulli: ds.Bernoulli = ds.Bernoulli(self.Xs)
        self.exponential: ds.Exponential = ds.Exponential(self.Xs)
        self.poisson: ds.Poisson = ds.Poisson(self.Xs)
        self.binomial: ds.Binomial = ds.Binomial(self.Xs)
        self.uniform: ds.Uniform = ds.Uniform(self.Xs)
        self.geometric: ds.Geometric = ds.Geometric(self.Xs)

    def set_model(self, model: str):
        """
        Sets the probability model that will be used in our analysis.

        :param model: Model name.
        :type model: str

        :return: Instance of Distribution model.
        :rtype: ds.Distribution
        """

        self.model = ds.Distribution(self.Xs).distribution(model)
        return self

    def mean(self) -> float:
        """
        Calculates the mean of the data set.

        :return: Mean of the data set.
        :rtype: float
        """

        if self.model is None:
            return s.mean(self.Xs)
        
        else:
            return self.model.mean()
        
    def var(self) -> float:
        """
        Calculates the variance of the data set.

        :return: Variance of the data set.
        :rtype: float
        """

        if self.model is None:
            return s.variance(self.Xs)
        
        else:
            return self.model.var()
        
    def skewness(self, p: float = None) -> float:
        """
        Calculates the skewness of the given data set.

        :param p: Parameter for skewness calculation if required.
        :type p: float

        :return: Skewness of the data set
        :rtype: float
        """

        if self.model is None:
            return print("You must define a model")
        
        elif hasattr(self.model, "skewness"):

            if repr(self.model) == "Bernoulli":

                return self.model.skewness(p)
            
            else:

                return self.model.skewness()
        
        else:
            return print("The model you defined does not have the method skewness")
        
    def kurtosis(self, p: float = None) -> float:
        """
        Calculates the kurtosis of the given data set.

        :param p: Parameter for kurtosis calculation if required.
        :type p: float

        :return: Kurtosis of the data set
        :rtype: float
        """

        if self.model is None:
            return print("You must define a model")
        
        elif hasattr(self.model, "kurtosis"):

            if repr(self.model) == "Bernoulli":

                return self.model.kurtosis(p)
            
            else:

                return self.model.kurtosis()
        
        else:
            return print("The model you defined does not have the method kurtosis")
        
    def p_hat(self) -> float:
        """
        Calculates the parameter p_hat from our given data set if it fits the correct distribution.

        :return: P hat parameter.
        :rtype: float
        """

        if self.model is None:
            return print("You must define a model")
        
        elif hasattr(self.model, "p_hat"):
            return self.model.p_hat()
        
        else:
            return print("The model you defined does not have parameter p hat")
        
    def lamb_hat(self) -> float:
        """
        Calculates the parameter lambda from our given data set if it fits the correct distribution.

        :return: lambda parameter.
        :rtype: float
        """

        if self.model is None:
            return print("You must define a model")
        
        elif hasattr(self.model, "lamb_hat"):
            return self.model.lamb_hat()
        
        else:
            return print("The model you defined does not have parameter lambda hat")
        
    def pdf(self, value: float, parameter1: float = None, parameter2: float = None) -> float:
        """
        Calculates the probability of a certain value for the model specified.

        :param value: Value we want to find the probability of.
        :type value: float

        :param parameter1: Optional expected value parameter.
        :type parameter1: float

        :param parameter2: Optional variance parameter.
        :type parameter2: float

        :return: Probability of achieving a certain result.
        :rtype: float
        """

        if self.model is None:
            return print("You must define a model")
        
        elif hasattr(self.model, "pdf"):

            if repr(self.model) == "Gaussian":

                return self.model.pdf(value, parameter1, parameter2)
            
            elif repr(self.model) == "Binomial":

                return self.model.pdf(value, parameter1, parameter2)
            
            else:

                return self.model.pdf(value, parameter1)
        
        else:
            return print("The model you defined does not have the method pdf")
        
    def cdf(self, value: float, parameter1: float = None, parameter2: float = None) -> float:
        """
        Calculates the cumulative probability of a certain value for the model specified.

        :param value: Value we want to find the probability of.
        :type value: float

        :param parameter1: Optional expected value parameter.
        :type parameter1: float

        :param parameter2: Optional variance parameter.
        :type parameter2: float

        :return: Probabilty of achieving up to a certain result.
        :rtype: float
        """

        if self.model is None:
            return print("You must define a model")
        
        elif hasattr(self.model, "cdf"):
            
            if repr(self.model) == "Gaussian":

                return self.model.cdf(value)
            
            elif repr(self.model) == "Binomial":

                return self.model.cdf(value, parameter1, parameter2)
            
            else:

                return self.model.cdf(value, parameter1)
        
        else:
            return print("The model you defined does not have the method pdf")

    def hypothesis_test(self, model: str = None) -> ht.HypothesisTesting:
        """
        Method used to perfrom multiple statistical hypothesis testing functions.
        Once called you can use any method from the Hypothesis test class.

        :param model: If instance attribute model has not been set you may pass it in hear.
        :type model: str

        :return: Instance of HypothesisTesting object.
        :rtype: ht.HypothesisTesting
        """

        if self.model is None and model is None:
            raise TypeError("You must define a model, the type is set to string which is not a correct model type")
        
        if self.model is None and model is not None:
            self.set_model(model)
            
        return ht.HypothesisTesting(self.Xs, repr(self.model))

    def bayesian_statistic(self, likelihood: str = None, prior: str = None) -> bs.Bayesian:
        """
        Method used to perform Bayesian statistical analysis.

        :param likelihood: The Model used to compute the likelihood function that encorporates new data in bayesian statistics.
        :type likelihood: str

        :param prior: The Model used to base an assumption of what the data/probability already is. Usually Gamma or Beta.
        :tyoe prior: str

        :return: Instance of Bayesian object used for Bayesian statistics. 
        :rtype: bs.Bayesian
        """
        
        if self.model is None and likelihood is not None:
            self.set_model(likelihood)
            
        return bs.Bayesian(self.Xs, likelihood, prior)
    
    def linear_regression(self, data: np.ndarray = None):
        """
        Method used to perform a linear regression on Our data and another variable.
        The data originally passed into the Data class is our response variable.

        :param data: Data used as explanatory variable.
        :type data: np.ndarray

        :return: A linear regression object that has multiple methods for performing a linear regression.
        :rtype: reg.LinearRegression
        """

        return reg.LinearRegression(data, self.Xs)
    
    def multiple_linear_regression(self, *args):
        """
        Method used to perform a multiple linear regression on Our data and multiple other variables.
        The data originally passed into the Data class is our response variable.

        :param args: arguments are multiple arrays of data.
        :type args: np.ndarray

        :return: A multiple linear regression object that has multiple methods for performing and plotting a multiple linear regression.
        :rtype: reg.MultipleLinearRegression
        """

        return reg.MultipleLinearRegression(self.Xs, *args)
    
    def pca(self, *args):
        """
        Method used to conduct Principle Component Analysis on a variable amount of data.

        :param args: arguments are multiple arrays of data.
        :type args: np.ndarray

        :return: An instance of a PCA object.
        :rtype: PCA
        """

        return PCA(*args)