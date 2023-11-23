import numpy as np
import scipy.stats as stats

from . import statistic as s 
from . import distributions as ds
            
class TestStatistic(ds.Distribution):
    """
    Instantiate test statistic object for use in our HypothesisTest class.
    Inherits Distribution class.

    :param Xs: Array like data.
    :type Xs: np.ndarray

    :param model: distribution our data fits.
    :type model: str
    """

    def __init__(self, Xs: np.ndarray, model: str = None):
        super().__init__(Xs, model)
        self.Xs = Xs
        self.model: str = model
        self.N: int = len(Xs)

    def confidence_interval(self, percent: float = 95, parameter: str = None) -> list:
        """
        Used to calculate a confidence interval for our confidence interval test.

        :param percent: Percent of distribution we are testing against.
        :type percent: float

        :param parameter: defines what parameter we want to calculate the confidence interval for.
        :type parameter: str

        :return: list with upper and lower bounds for our parameter.
        :rtype: List
        """
        return super().distribution().confidence_interval(percent, parameter)
    
    def z_test_statistic(self, null: float, sigma: float = None) -> float:
        """
        Method used to calculate our z test statistic for our z test.

        :param null: Value of our null hypothesis.
        :type null: float

        :param sigma: Known variance of our sample.
        :type sigma: float

        :return: z test statistic
        :rtype: float
        """
        
        dist = super().distribution(self.model)
        x_bar: float = dist.mean()

        if repr(dist) == "Gaussian":

            if sigma is None:
                raise TypeError("Sigma must be provided")
            
            return (x_bar - null) / (np.sqrt(sigma / self.N))
        
        elif repr(dist) == "Exponential":
            
            if sigma is None:
                sigma: float = dist.var(1 / null)

            return (x_bar - null) / (np.sqrt(sigma / self.N))
        
        elif repr(dist) == "Binomial":

            if sigma is None:
                sigma: float = dist.var(null) / self.N

            x_bar = x_bar / self.N
            return (x_bar - null) / (np.sqrt(sigma / self.N))
        
        elif repr(dist) == "Geometric":

            if null < 1:
                sigma: float = dist.var(null)
                return (x_bar - (1 / null)) / (np.sqrt(sigma / self.N))

            else:
                sigma: float = dist.var(1 / null)
                return (x_bar - null) / (np.sqrt(sigma / self.N))

        else:

            if sigma is None:
                sigma: float = dist.var(null)
            
            return (x_bar - null) / (np.sqrt(sigma / self.N))
        
    def t_test_statistic(self, null: np.ndarray):
        """
        Method that returns a t test statistic for a t test.

        :param null: Value for our null hypothesis.
        :type null: np.ndarray

        :return: T test statistic.
        :rtype: float
        """
        dist = super().distribution("Gaussian")
        x_bar: float = dist.mean()
        var: float = dist.var()
        return np.sqrt(self.N) * (x_bar - null) / var
        
    def walds_test_statistic(self, null: float, fisher_info: bool = False) -> float:
        """
        Method that returns a wald test statistic for a wald test.

        :param null: Value for our null hypothesis.
        :type null: float

        :param fisher_info: If true calculates out test using fisher information.
        :type fisher_info: bool

        :return: wald test statistic.
        :rtype: float
        """
        dist = super().distribution(self.model)

        if dist is None:
            raise TypeError("You must define a model")
        
        elif hasattr(dist, "lamb_hat"):
            theta_hat: float = dist.lamb_hat()

        elif hasattr(dist, "p_hat"):
            theta_hat: float = dist.p_hat()

        else:
            theta_hat: float = dist.mean()

        if fisher_info == False:
            var_theta_hat: float = dist.var_theta_hat()
            return (theta_hat - null) / np.sqrt(var_theta_hat)

        else:
            # note if we get rid of the squre over (theta_hat - null) and take the square root of (self.N * var_theta_hat) we get the same awnser as when the fisher info is false
            fisher: float = dist.fisher_information()
            return (self.N * fisher) * (theta_hat - null) ** 2
        
    def likelihood_ratio_test_statistic(self, null: float, known_var = None):
        """
        Method that returns a likelihood ratio test statistic for a likelihood ratio test statistic.

        :param null: Value for our null hypothesis.
        :type null: float

        :param known_var: Optional parameter if variance is known.
        :type known_var: float

        :return: likelihood ratio test statistic.
        :rtype: float
        """

        dist = super().distribution(self.model)

        if repr(dist) == "Gaussian":

            if known_var is None:

                raise ValueError("You must define a known population variance in order to perform a likelihood test on a Gaussian")
            
            else:
                return dist.likelihood_ratio(null, known_var)
        
        else:
            
            return dist.likelihood_ratio(null)

class PValue:
    """
    Instantiate object used to calculate and represent a P value for our test.

    :param Xs: Array of data.
    :type Xs: np.ndarray

    :param null: value of null hypothesis.
    :type null: float

    :param model: Distribution our data represents.
    :type model: str

    :param t_test: True if we are conducting a t test.
    :type t_test: bool

    :param wald_test: True if we are conducting a wald test.
    :type wald_test: bool

    :param left_tail: True if we are conducting a left tailed test.
    :type left_tail: bool

    :param right_tail: True if we are conducting a right tailed test.
    :type right_tail: bool
    """

    def __init__(self, Xs: np.ndarray, null: float, model: str = None, t_test: bool = False, wald_test: bool = False, left_tail: bool = False, right_tail: bool = False):
        self.Xs: np.ndarray = np.array(Xs)
        self.null: float = null
        self.model: str = model
        self.t_test: bool = t_test
        self.wald_test: bool = wald_test
        self.left_tail: bool = left_tail
        self.right_tail: bool = right_tail

    def t_test_cdf(self) -> float:
        """
        Used to find our p value.

        :return: cdf of student t distribution.
        :rtype: float
        """
        t_stat: float = TestStatistic(self.Xs).t_test_statistic(self.null)
        df = len(self.Xs) - 1
        cdf: float = stats.t.cdf(t_stat, df)
        return cdf
    
    def z_test_cdf(self, sigma: float = None) -> float:
        """
        Used to find our p value.

        :param sigma: Known variance.
        :type sigma: float

        :return: cdf of gaussian distribution.
        :rtype: float
        """
        dist = ds.Distribution(self.Xs).distribution("Gaussian")
        test_stat = TestStatistic(self.Xs, self.model).z_test_statistic(self.null, sigma)
        cdf: float = dist._gaussian_cdf(test_stat, test_statistic = True)
        return cdf
    
    def walds_test_cdf(self, fisher_info: bool = False) -> float:
        """
        Used to find our p value.

        :param fisher_info: If true calculates out test using fisher information.
        :type fisher_info: bool

        :return: cdf of gaussian distribution.
        :rtype: float
        """
        dist = ds.Distribution(self.Xs).distribution("Gaussian")
        test_stat: float = TestStatistic(self.Xs, self.model).walds_test_statistic(self.null, fisher_info)
        
        cdf: float = dist._gaussian_cdf(test_stat, test_statistic = True)
        return cdf

    def __call__(self, sigma: float = None, fisher_info = False):

        if self.left_tail is True:

            if self.wald_test is True:
                cdf: float = self.walds_test_cdf(fisher_info)
                return cdf
            
            elif self.t_test is True:
                cdf: float = self.t_test_cdf()
                return cdf
            
            else:
                cdf: float = self.z_test_cdf(sigma)
                return cdf
            
        elif self.right_tail is True:

            if self.wald_test is True:
                cdf: float = self.walds_test_cdf(fisher_info)
                return 1 - cdf
            
            elif self.t_test is True:
                cdf: float = self.t_test_cdf()
                return 1 - cdf
            
            else:
                cdf: float = self.z_test_cdf(sigma)
                return 1 - cdf
            
        else:
            if self.wald_test is True:
                dist = ds.Distribution(self.Xs).distribution("Gaussian")
                test_stat: float = TestStatistic(self.Xs, self.model).walds_test_statistic(self.null, fisher_info)
                cdf: float = dist._gaussian_cdf(abs(test_stat), test_statistic = True)
                return 1 - cdf
            
            elif self.t_test is True:
                t_stat: float = TestStatistic(self.Xs).t_test_statistic(self.null)
                df = len(self.Xs) - 1
                cdf: float = stats.t.cdf(abs(t_stat), df)
                return 1 - cdf
            
            else:
                dist = ds.Distribution(self.Xs).distribution("Gaussian")
                test_stat = TestStatistic(self.Xs, self.model).z_test_statistic(self.null, sigma)
                cdf: float = dist._gaussian_cdf(abs(test_stat), test_statistic = True)
                return 1 - cdf

class HypothesisTesting(TestStatistic):
    """
    Instantiate a object for running hypothesis testing.
    Inherits Test statistic class.

    :param Xs: Array of data.
    :type Xs: np.ndarray

    :param model: Defines distribution our data fits.
    :type model: str
    """

    def __init__(self, Xs: np.ndarray, model: str = None):
        super().__init__(Xs, model)
        self.Xs = Xs
        self.model: str = model
        self.N: int = len(Xs)
    
    def p_value(self, null: float, t_test: bool = False, wald_test: bool = False, left_tail: bool = False, right_tail: bool = False, sigma: float = None, fisher_info = False):
        """
        Method used to calculate and represent a P value for our test.

        :param null: value of null hypothesis.
        :type null: float

        :param t_test: True if we are conducting a t test.
        :type t_test: bool

        :param wald_test: True if we are conducting a wald test.
        :type wald_test: bool

        :param left_tail: True if we are conducting a left tailed test.
        :type left_tail: bool

        :param right_tail: True if we are conducting a right tailed test.
        :type right_tail: bool

        :param sigma: used if our p value requries a known variance.
        :type sigma: float

        :param fisher_info: if true will use the fisher info in out p value calculation (only for walds test)
        :type fisher_info: bool

        :return: p value of our test.
        :rtype: float
        """
        p_val = PValue(self.Xs, null, self.model, t_test, wald_test, left_tail, right_tail)
        return p_val(sigma, fisher_info)
    
    def t_test(self, null: float, percent: float = 95, left_tail: bool = False, right_tail: bool = False):
        """
        Method for calculating our t test.

        :param null: value of null hypothesis.
        :type null: float

        :param percent: Defines percent of our distribution.
        :type percent: float

        :param left_tail: True if we are conducting a left tailed test.
        :type left_tail: bool

        :param right_tail: True if we are conducting a right tailed test.
        :type right_tail: bool

        :return: _test method from call to our object.
        :rtype: HypothesisTest
        """

        if percent > 1: percent *= .01

        if right_tail is False and left_tail is False: percent = 1 - (1 - percent) / 2

        t_stat: float = super().t_test_statistic(null)
        df: int = len(self.Xs) - 1
        qa: float = stats.t.ppf(percent, df)

        return self._test(t_stat, qa, left_tail, right_tail)
    
    def z_test(self, null: float, sigma: float = None, percent: float = 95, left_tail: bool = False, right_tail: bool = False) -> float:
        """
        Method for calculating our z test.

        :param null: value of null hypothesis.
        :type null: float

        :param sigma: Known variance.
        :type sigma: float

        :param percent: Defines percent of our distribution.
        :type percent: float

        :param left_tail: True if we are conducting a left tailed test.
        :type left_tail: bool

        :param right_tail: True if we are conducting a right tailed test.
        :type right_tail: bool

        :return: _test method from call to our object.
        :rtype: HypothesisTest
        """

        if percent > 1: percent *= .01

        if right_tail is False and left_tail is False: percent = 1 - (1 - percent) / 2

        dist = ds.Distribution(self.Xs).distribution("Gaussian")

        t_stat: float = super().z_test_statistic(null, sigma)
        #qa: float = dist.percentile(percent, standardize=True)
        qa: float = s.percentile(percent)

        return self._test(t_stat, qa, left_tail, right_tail)
    
    def walds_test(self, null: float, percent: float = 95, left_tail: bool = False, right_tail: bool = False, fisher_info = False):
        """
        Method for calculating our walds test.

        :param null: value of null hypothesis.
        :type null: float

        :param percent: Defines percent of our distribution.
        :type percent: float

        :param left_tail: True if we are conducting a left tailed test.
        :type left_tail: bool

        :param right_tail: True if we are conducting a right tailed test.
        :type right_tail: bool

        :param fisher_info: If true uses the fisher information to calculate our test statistic.
        :type fisher_info: bool

        :return: _test method from call to our object.
        :rtype: HypothesisTest
        """
        if percent > 1: percent *= .01

        if right_tail is False and left_tail is False: percent = 1 - (1 - percent) / 2

        w: float = super().walds_test_statistic(null, fisher_info)
        qa: float = s.percentile(percent)

        return self._test(w, qa, left_tail, right_tail)
            
    def likelihood_ratio_test(self, null: float, percent: float = 95, known_var = None):
        """
        Method for calculating our likelihood ratio test.

        :param null: value of null hypothesis.
        :type null: float

        :param percent: Defines percent of our distribution.
        :type percent: float

        :param known_var: Specifies out known variance.
        :type left_tail: float

        :return: _test method from call to our object.
        :rtype: HypothesisTest
        """

        if percent > 1: percent *= .01

        percent = 1 - (1 - percent) / 2

        t: float = super().likelihood_ratio_test_statistic(null, known_var)
        qa: float = stats.chi2.ppf(percent, 1)

        return self._test(t, qa)
            
    def confidence_interval_test(self, **null):
        """
        Method used to calculate our confidence interval test.

        :param null: values for the parameter we are testing.
        :type null: Dictionary

        :return: Confidence interval test.
        :rtype: str
        """

        for paramater_name, null_values in null.items():
            
            ci: list = super().confidence_interval(parameter = paramater_name)

            if isinstance(null_values, (list, tuple)):
                for null_value in null_values:
                    print(f"True {paramater_name} Confidence Interval:\n{ci}\nNull Value: {null_value}")

                    if null_value > ci[1] or null_value < ci[0]:

                        return f"Reject the null"
                    else:
                        
                        return f"Fail to reject the null"                    
            else:

                print(f"True {paramater_name} Confidence Interval:\n{ci}\nNull Value: {null_values}")

                if null_values > ci[1] or null_values < ci[0]:

                    return f"Reject the null"
                else:
                    
                    return f"Fail to reject the null"

    def _test(self, test_statistic: float, qa: float, left_tail = False, right_tail = False):
        """
        Special method used for return values in other methods.
        Calculates are defines tests.

        :param test_statistic: test statistic of the test we are running.
        :type test_statistic: float

        :param qa: Quantile from the distribution that matches the test we are running.
        :type qa: float

        :param left_tail: True if we are conducting a left tailed test.
        :type left_tail: bool

        :param right_tail: True if we are conducting a right tailed test.
        :type right_tail: bool

        :return: Outcome of our test.
        :rtype: str        
        """

        if left_tail is False and right_tail is False:
            # run a two tail walds test
            print(f"Quantile: {qa}")
            print(f"Test Statistic: {abs(test_statistic)}")
            if abs(test_statistic) > qa:
                return "Reject the null hypothesis"
            
            else:
                return "Fail to reject the null hypothesis"
            
        elif left_tail is True:
            print(f"Test Statistic: {test_statistic}")
            print(f"Quantile: {-qa}")
            if test_statistic < -qa:
                return "Reject the null hypothesis"
            
            else:
                return "Fail to reject the null hypothesis"
            
        elif right_tail is True:
            print(f"Test Statistic: {test_statistic}")
            print(f"Quantile: {qa}")
            if test_statistic > qa:
                return "Reject the null hypothesis"
            
            else:
                return "Fail to reject the null hypothesis"
    
    def __call__(self, null: float, t_test: bool = False, wald_test: bool = False, z_test: bool = False, left_tail: bool = False, right_tail: bool = False, sigma: float = None, fisher_info = False):
        p_val = PValue(self.Xs, null, self.model, t_test, wald_test, left_tail, right_tail)
        
        if t_test is True:
            print(f"p-value: {p_val(sigma, fisher_info)}")
            return self.t_test(null, left_tail=left_tail, right_tail=right_tail)
        
        elif wald_test is True:
            print(f"p_value: {p_val(sigma, fisher_info)}")
            return self.walds_test(null, left_tail=left_tail, right_tail=right_tail, fisher_info=fisher_info)
        
        elif z_test is True:
            print(f"p-value: {p_val(sigma, fisher_info)}")
            return self.z_test(null, left_tail=left_tail, right_tail=right_tail, sigma = sigma)