from .distributions import Gaussian
from .distributions import Gamma
from .distributions import Beta
from .distributions import Uniform
from .distributions import Bernoulli
from .distributions import Exponential
from .distributions import Distribution
from . import statistic as s
from . import likelihoods as ll

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

class ConjugatePrior:
    """
    Instantiate a conjugate prior object to be used in other class's for defining prior distributions.
    This is a helper class that is used in other class's for easy access to other distributions.

    :param Xs: Array object of our data.
    :type Xs: np.ndarray

    :param model: Instance attribute used to define the distribution to be used as the conjugate prior.
    :type model: str 
    """

    def __init__(self, Xs: np.ndarray, model: str = None):

        self.Xs: np.ndarray = np.array(Xs)
        self.model: str = model

    def distribution(self, dist: str = None, value: float = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1):
        """
        A helper method used for filtering out and returning a pdf of a passed distribution.

        :param dist: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type dist: str

        :param value: The value of the probablity we want to calculate.
        :type value: float

        :param mu: Optional parameter used to calculate the pdf if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used to calculate the pdf if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: Distribution from distribution.py file.
        :rtype: Distribution 
        """
        if self.model is None and dist is None:
            return f"You must set a model"
        
        elif self.model is None and dist is not None:
            self.model = dist

        match self.model.lower():

            case "gaussian" | "gauss" | "normal" | "norm" | "gaus":

                if value is None:

                    raise TypeError("When using a Gaussian as a conjugate prior you must define a value")
                
                return Gaussian(self.Xs).pdf(value, mu, var)
            
            case "gamma":
                if value is None:

                    raise TypeError("When using a Gamma distribution as a conjugate prior you must define a value")
                
                return Gamma(self.Xs).pdf(theta, a, b)
            
            case "beta":

                if value is None:

                    raise TypeError("When using a Beta distribution as a conjugate prior you must define a value")

                return Beta(self.Xs).pdf(theta, a, b)
            
            case "bernoulli" | "ber":

                if value is None:

                    raise TypeError("When using a Bernoulli distribution as a conjugate prior you must define a value")

                return Bernoulli(self.Xs).pmf(value, theta)
            
            case "exponential" | "exp":

                return Exponential(self.Xs).pdf(value, theta)
            
            case "uniform" | "uni":

                return Uniform(self.Xs).pdf()
            
class Bayesian:
    """
    Instantiate a Bayesian object for Bayesian statistical analysis.

    :param Xs: Data used for Bayesian statistical analysis.
    :type Xs: np.ndarray

    :param likelihood: Parameter used to specify the model we will use as a likelihood.
    :type likelihood: str

    :param prior: Parameter used to specify the model we will use as a prior distribution.
    :type prior: str
    """

    def __init__(self, Xs: np.ndarray, likelihood: str = None, prior: str = None):
        self.Xs: np.ndarray = np.array(Xs)
        self.likelihood: str = likelihood
        self.prior: str = prior
        self.theta_range: np.ndarray = None
        self.posterior_distributions: dict = None
        self.N: int = len(self.Xs)

    def set_prior(self, model: str):
        """
        A method used to set a prior distribution if it has not yet been set while instantiating the Bayesian object.

        :param model: Used to define a model for out prior distribution.
        :type model: str 
        """
        self.prior: str = model

    def set_likelihood(self, model: str):
        """
        A method used to set a likelihood distribution if it has not yet been set while instantiating the Bayesian object.

        :param model: Used to define a model for out likelihood distribution.
        :type model: str 
        """
        self.likelihood: str = model

    def set_theta_range(self, parameter_range: np.ndarray = None, start: float = None, end: float = None):
        """
        Method used to set the range of our parameter which will be passed into a maximum likelihood function in order to get a range of parameters.

        :param parameter_range: np.linspace optional parameter used to specify a range.
        :type parameter_range: np.ndarray

        :param start: Optional start of our parameter range.
        :tyoe start: float

        :param end: Optional end of our parameter range
        :type end: float

        :return: Instance of our Bayesian object.
        :rtype: Bayesian
        """

        if parameter_range is None and start is None and end is None:

            self.theta_range: np.ndarray = np.linspace(.01, .99, self.N)
        
        elif parameter_range is None:

            if start is None or end is None:

                raise TypeError("You must define both a starting point and an ending point")
            
            self.theta_range: np.ndarray = np.linspace(start, end, self.N)

        else:

            if len(parameter_range) == 2:

                self.theta_range: np.ndarray = np.linspace(parameter_range[0], parameter_range[1], self.N)

            else:

                self.theta_range: np.ndarray = parameter_range

        return self
        
    def likelihood_model(self, likelihood: str = None, data = None):
        """
        Method used to define a model that will be used to update our parameters as we incorporate in new data.

        :param likelihood: Define a distribution to use as a likelihood.
        :type likelihood: str

        :param data: Optional parameter, used for functionality when inputing data into our Bayesian analysis or to change our original data passed in.
        :type data: float

        :return: Distribution to be used in our likelihood function.
        :rtype: Distribution.
        """

        if data is None:

            if likelihood is None and self.likelihood is None:

                raise ValueError("You must define a model")
            
            elif self.likelihood is None:

                return Distribution(self.Xs, likelihood).distribution()
            
            else:

                return Distribution(self.Xs, self.likelihood).distribution()
            
        else:

            if likelihood is None and self.likelihood is None:

                raise ValueError("You must define a model")
            
            elif self.likelihood is None:

                return Distribution(data, likelihood).distribution()
            
            else:

                return Distribution(data, self.likelihood).distribution()
        
    def conjugate_prior(self, prior: float = None, value: float = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1) -> float:
        """
        A method used for defining a conjugate prior distribution.

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param value: The value of the probablity we want to calculate.
        :type value: float

        :param mu: Optional parameter used to calculate the pdf if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used to calculate the pdf if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: A instance of an object the represents our prior distribution.
        :rtype: ConjugatePrior
        """
        if prior is None and self.prior is None:

            return ConjugatePrior(self.Xs).distribution("Uniform", value, mu, var, theta, a, b)

        if prior is None:

            return ConjugatePrior(self.Xs).distribution(self.prior, value, mu, var, theta, a, b)

        else:

            return ConjugatePrior(self.Xs).distribution(prior, value, mu, var, theta, a, b)
        
    def set_posterior(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1) -> dict:
        """
        A method used to set a posterior distribution used for our Bayesian statistic analysis.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: Dictionary of all calculates posterior distributions.
        :rtype: Dictionary
        """

        conjugate_prior: float = self.conjugate_prior(prior, self.Xs[0], mu, var, theta, a, b)

        posterior_dict: dict = {}

        for ind, data_point in enumerate(self.Xs):

            if (likelihood is not None and likelihood.lower() in ("gaus", "gauss", "gaussian", "normal")) or (self.likelihood is not None and self.likelihood.lower() in ("gaus", "gauss", "gaussian", "normal")):
                
                if var is None:

                    raise ValueError("You must set a value for the parameter var")
                
                likelihood_func = self.likelihood_model(likelihood, [data_point]).likelihood_function(self.theta_range, var)
                
            else:
                
                likelihood_func = self.likelihood_model(likelihood, [data_point]).likelihood_function(self.theta_range)
            
            marginal_likelihood: float = sum(likelihood_func * conjugate_prior)
            posterior = (likelihood_func * conjugate_prior) / marginal_likelihood
            conjugate_prior = posterior
            posterior_dict[ind] = posterior

        self.posterior_distributions: dict = posterior_dict

        return posterior_dict
        
    def get_posterior(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1) -> dict:
        """
        A method used to get the posterior distribution used for our Bayesian statistic analysis.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: Dictionary of all calculates posterior distributions.
        :rtype: Dictionary
        """
        if self.posterior_distributions is None:

            posterior_dict: dict = self.set_posterior(likelihood, prior, mu, var, theta, a, b)

        else:

            posterior_dict: dict = self.posterior_distributions

        return posterior_dict
    
    def max_parameter_list(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1) -> float:
        """
        A method used to calculate the max parameter for each new data point passed into the likelihood function.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: A list of the max parameter and max probabilities.
        :rtype: List
        """
        posterior_dict: dict = self.get_posterior(likelihood, prior, mu, var, theta, a, b)

        max_parameter: list = []
        max_probability: list = []

        for i in posterior_dict:

            posterior_distribution: list = posterior_dict[i]

            max_value: float = 0
            max_value_index: float = 0

            for j in range(len(posterior_distribution)):

                if posterior_distribution[j] > max_value:

                    max_value = posterior_distribution[j]
                    max_value_index = j

                else:

                    continue

            map: float = self.theta_range[max_value_index]

            max_parameter.append(map)
            max_probability.append(max_value)
        return (max_parameter, max_probability)
    
    def posterior_mean(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1) -> float:
        """
        A method used to calculate the mean of the posterior distributions.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: Average of the posterior distribution.
        :rtype: float
        """
        posteriors_map: list = np.array(self.max_parameter_list(likelihood, prior, mu, var, theta, a, b)[0])

        return posteriors_map.mean()

    def map(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1) -> float:
        """
        A method used to return the last value in a list which is the maxima a posterior for out Bayesian analysis.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: The maxima a posterior.
        :rtype: float
        """
        posteriors_map: list = self.max_parameter_list(likelihood, prior, mu, var, theta, a, b)[0]

        return posteriors_map[-1]
    
    def confidence_region(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1, percent: float = 90) -> list:
        """
        A method used to calculate a bayesian confidence region.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: A list of our upper and lower values for our confidence region.
        :rtype: List
        """
        max_value: float = self.map(likelihood, prior, mu, var, theta, a, b)

        var = self.Xs.var()

        z: float = s.percentile(percent)
        
        confidence_region = [max_value - z * (np.sqrt(var/self.N)), max_value + z * (np.sqrt(var/self.N))]

        return confidence_region
    
    def plot_confidence_region(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1, percent: float = 90):
        """
        A method for plotting our amx posterior distribution and our bayesian confidence region.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float

        :return: A bayesian confidence region.
        :rtype: List
        """
        confidence_region: list = self.confidence_region(likelihood, prior, mu, var, theta, a, b, percent)

        post_dict: dict = self.get_posterior(likelihood, prior, mu, var, theta, a, b)

        last_posterior: list = list(post_dict.values())[-1]

        if percent < 1:
            percent *= 100

        plt.figure(figsize=(8, 6))
        plt.plot(self.theta_range, last_posterior, label = "Final Posterior Distribution")
        plt.axvline(x = confidence_region[0], ls = '--', color = 'y', label = f'{percent}% Conf Int')
        plt.axvline(x = confidence_region[1], ls = '--', color = 'y')
        plt.legend()
        plt.show()

        return confidence_region
    
    def plot_posteriors(self, likelihood: str = None, prior: str = None, mu: float = None, var: float = None, theta: float = None, a: float = 1, b: float = 1):
        """
        A method used to plot all of our posterior distributions.

        :param likelihood: Used to define our likelihood if it has not been defined yet.
        :type likelihood: str

        :param prior: The distribution used as the prior, if the model instance attribute is not defined we have to define it here.
        :type prior: str

        :param mu: Optional parameter used if the mean of the population is known.
        :type mu: float

        :param var: Optional parameter used if the variance of the population is known.
        :type var: float

        :param theta: Parameter used as p hat for a bernoulli distribution and lambda hat for and exponential distribution.
        :type theta: float

        :param a: Parameter used in a Beta and Gamma distribution.
        :type a: float

        :param b: Parameter used in a Beta and Gamma distribution.
        :type b: float
        """
        posterior_dict: dict = self.get_posterior(likelihood, prior, mu, var, theta, a, b)

        posteriors_map, posterior_probabilities = self.max_parameter_list(likelihood, prior, mu, var, theta, a, b)

        partition: int = len(posterior_dict) // 4
        plt.figure(figsize=(10, 8))
        handles: list = []
        for key, value in posterior_dict.items():
            #print(key)
            if key % partition == 0 or key == len(posterior_dict) - 1:
                line, = plt.plot(self.theta_range, value, label = f'Model after observing {key} data')
                plt.text(posteriors_map[key], posterior_probabilities[key], str(round(posteriors_map[key], 3)) + ', ' + str(round(posterior_probabilities[key], 3)), ha = 'center')
                handles.append(line)

        dummy_line1 = mlines.Line2D([], [], color='none', label=f"Maximum a Posterior: {round(posteriors_map[-1], 3)}")
        dummy_line2 = mlines.Line2D([], [], color='none', label=f"Posterior Mean: {round(np.array(posteriors_map).mean(), 3)}")
        handles.append(dummy_line1)
        handles.append(dummy_line2)

        plt.title("Posterior Distributions")
        plt.xlabel("Parameter Value")
        plt.ylabel("Probability Density")
        plt.legend(handles=handles)
        plt.show()

        return f"Finished"