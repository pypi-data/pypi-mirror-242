import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from . import statistic as s
from scipy import stats

class LinearRegression:
    """
    Instatiate object for calculating a Linear Regression.

    :param Xs: Array of explanatory data.
    :type Xs: np.ndarray

    :param Ys: Array of response variable.
    :type Ys: np.ndarray

    :param unbiasedMu: Used to specify if the mean is biased or unbiased.
    :type unbiasedMu: bool

    :param unbiasedVar: Used to specify if the varaince is biased or unbiased.
    :type unbiasedVar: bool 
    """

    def __init__(self, Xs: np.ndarray = None, Ys: np.ndarray = None, unbiasedMu: bool = False, unbiasedVar: bool = False):
        self.Xs: np.ndarray = np.array(Xs)  # explanatory variable
        self.Ys: np.ndarray = np.array(Ys)  # Y is what we are trying to predict based on X, ie response variable
        self.N: int = len(Xs)
        self.unbiasedMu: bool = unbiasedMu
        self.unbiasedVar: bool = unbiasedVar

    def B1(self) -> float:
        """
        Method used to find the slope of our regression line.

        :return: Slope of the regression line.
        :rtype: float
        """
        if len(self.Xs) != len(self.Ys):
            print(f"Length of X {len(self.Xs)}\nLength of Y {len(self.Ys)}")
            raise ValueError('X and Y are not the same length')
        S2xy: float = 0
        S2x: float = 0
        uX: float = s.mean(self.Xs, self.unbiasedMu)
        uY: float = s.mean(self.Ys, self.unbiasedMu)
        for n in range(len(self.Xs)):
            S2xy += (self.Xs[n] - uX)*(self.Ys[n] - uY)
            S2x += (self.Xs[n] - uX) ** 2
        return S2xy / S2x

    def B0(self) -> float:
        """
        Method used to find the intercept of our regression line.

        :return: intercept of our regression line.
        :rtype: float
        """
        return s.mean(self.Ys, self.unbiasedMu) - self.B1()*s.mean(self.Xs, self.unbiasedMu)

    def linear_regression_line(self) -> np.ndarray:
        """
        Method used to calculate our regression line.

        :return: Regression line.
        :rtype: np.ndarray
        """
        return self.B1()*self.Xs + self.B0() 

    def residuals(self) -> np.ndarray:
        """
        Method used to find the residual errors from our regression line to the actual values.

        :return: Errors between our regression line and the actual values.
        :rtype: np.ndarray
        """
        return self.Ys - self.linear_regression_line()
    
    def predict_value(self, value: float) -> float:
        """
        Method used to predict value passed on the regression calculation.

        :param value: Value we use to predict our explanatory value.
        :type value: float

        :return: Predicted value of our explanatory variable.
        :rtype: float
        """
        return self.B1() * value + self.B0()
    
    def regression_statistics(self):
        """
        Method used to print statistics based our regression.

        :return: print statement summarizing out regression statistics.
        :rtype: str
        """

        residuals: list = self.residuals()

        correlation: float = s.correlation(self.Xs, self.Ys) # this is our multiple R from excel regression stats table

        r_squared: float = correlation ** 2

        adjusted_r_squared: float = 1 - (((1 - r_squared) * (self.N - 1)) / (self.N - 2))

        standard_error: float = np.sqrt(s.variance(residuals))

        return (
                f"------------------------\n"
                f"Regression Statistics\n"
                f"------------------------\n"
                f"Correlation        {correlation:.3f}\n"
                f"R Square           {r_squared:.3f}\n"
                f"Adjusted R Square  {adjusted_r_squared:.3f}\n"
                f"Standard Error     {standard_error:.3f}\n"
                f"Observations       {self.N}\n"
                f"------------------------\n"
            )
    
    def anova(self):
        """
        Method used to calculate statistics of a anova analysis.

        :return: Statistical summary for our anova test.
        :rtype: str
        """

        y_pred: list = self.linear_regression_line()

        # DF

        degree_f_regression: int = 1 # note in a multiple linear regression this is k (ie how many predictor variables there are)
        degree_f_residual: float = self.N - 2  # in multiple this is n - k - 1
        degree_f_total: float = self.N - 1

        # SS (sum of squares)
        sum_of_square_total: float = np.sum((self.Ys - s.mean(self.Ys)) ** 2)
        sum_of_square_regression: float = np.sum((y_pred - np.mean(self.Ys)) ** 2)
        sum_of_square_residual: float = np.sum((self.Ys - y_pred) ** 2)

        # MS (Mean Square)
        ms_total: float = sum_of_square_total / degree_f_total
        ms_regression: float = sum_of_square_regression / degree_f_regression
        ms_residual: float = sum_of_square_residual / degree_f_residual

        # F The F-statistic, a ratio of MS due to regression to MS due to residuals
        f = ms_regression / ms_residual

        # significance f, p-value of F-statistic
        p_value: float = 1 - stats.f.cdf(f, degree_f_regression, degree_f_residual)

        return (
                f"ANOVA\n"
                f"---------------------------------------------------------------------\n"
                f"{'Source':<12} {'df':>4} {'SS':>10} {'MS':>10} {'F':>10} {'Significance F':>18}\n"
                f"---------------------------------------------------------------------\n"
                f"{'Regression':<12} {degree_f_regression:>4} {sum_of_square_regression:>10.3f} {ms_regression:>10.3f} {f:>10.3f} {p_value:>18.11f}\n"
                f"{'Residual':<12} {degree_f_residual:>4} {sum_of_square_residual:>10.3f} {ms_residual:>10.3f}\n"
                f"{'Total':<12} {degree_f_total:>4} {sum_of_square_total:>10.3f}\n"
                f"---------------------------------------------------------------------\n"
            )
    
    def slope_intercept_statistics(self):
        """
        Method used to calculate statistics for our slope and intercept.

        :return: Slope and statistical statistics.
        :rtype: str
        """

        residuals: list = self.residuals()
        sse: float = np.sum(residuals ** 2)

        # Coefficients

        slope: float = self.B1()
        intercept: float = self.B0()

        # Standard Error

        se_slope: float = np.sqrt(sse / (self.N - 2)) / np.sqrt(np.sum((self.Xs - s.mean(self.Xs))**2))
        se_intercept: float = se_slope * np.sqrt(np.sum(self.Xs**2) / self.N)

        # t-statistics

        t_stat_slope: float = slope / se_slope
        t_stat_intercept: float = intercept / se_intercept

        # p-values

        p_value_slope = 2 * (1 - stats.t.cdf(np.abs(t_stat_slope), df=self.N - 2))
        p_value_intercept = 2 * (1 - stats.t.cdf(np.abs(t_stat_intercept), df=self.N - 2))

        # Confidence Intervals

        t_critical = stats.t.ppf(1 - 0.025, df=self.N - 2)
        ci_slope = (slope - t_critical * se_slope, slope + t_critical * se_slope)
        ci_intercept = (intercept - t_critical * se_intercept, intercept + t_critical * se_intercept)

        return (
                f"----------------------------------------------------------------------------------------------------\n"
                f"{'Source':<18}{'Coefficients':>15}{'Standard Error':>17}{'t stat':>10}{'P-value':>10}{'Lower 95%':>15}{'Upper 95%':>15}\n"
                f"----------------------------------------------------------------------------------------------------\n"
                f"{'Intercept':<18}{intercept:>15.4f}{se_intercept:>17.4f}{t_stat_intercept:>10.4f}{p_value_intercept:>10.4f}{ci_intercept[0]:>15.4f}{ci_intercept[1]:>15.4f}\n"
                f"{'Slope (X variable)':<18}{slope:>15.4f}{se_slope:>17.4f}{t_stat_slope:>10.4f}{p_value_slope:>10.4f}{ci_slope[0]:>15.4f}{ci_slope[1]:>15.4f}\n"
                f"----------------------------------------------------------------------------------------------------\n"
            )
    
    def plot_residual(self):
        """
        Method used to plot the residuals.

        :return: Graph of our residuals.
        :rtype: str
        """

        residual: list = self.residuals()

        plt.figure(figsize=(8, 6))
        plt.scatter(self.Xs, residual, label = "Residuals")
        plt.show()

        return f"Finished"
    
    def plot_regression(self):
        """
        Method for plotting our regression.

        :return: Plot of our regression.
        :rtype: str
        """
        
        regression_line: list = self.linear_regression_line()

        plt.figure(figsize=(8, 6))
        dummy_line1 = mlines.Line2D([], [], color='none', label=f"y = {round(self.B1(), 3)}X + {round(self.B0(), 6)}")
        plt.scatter(self.Xs, self.Ys, color = "red")
        plt.plot(self.Xs, regression_line, label = "Linear Regression")
        plt.title("Linear Regression")
        plt.xlabel("Explanatory Variable")
        plt.ylabel("Response Variable")
        plt.legend(handles=[dummy_line1])
        plt.show()

        return f"Finished"
    
    def __call__(self):

        regression_line: list = self.linear_regression_line()
        residual: list = self.residuals()

        print(self.regression_statistics())
        print(self.anova())
        print(self.slope_intercept_statistics())

        plt.figure(figsize=(13, 6))
        dummy_line1 = mlines.Line2D([], [], color='none', label=f"y = {round(self.B1(), 3)}X + {round(self.B0(), 6)}")

        plt.subplot(1, 2, 1)
        plt.scatter(self.Xs, self.Ys, color = "red")
        plt.plot(self.Xs, regression_line, label = "Linear Regression")
        plt.title("Linear Regression")
        plt.xlabel("Explanatory Variable")
        plt.ylabel("Response Variable")
        plt.legend(handles=[dummy_line1])

        plt.subplot(1, 2, 2)
        plt.scatter(self.Xs, residual, label = "Residuals")
        plt.title("Residuals")
        plt.show()

        return f"Finished"

class MultipleLinearRegression:
    """
    Instatiate Multiple Linear Regression model.

    :param Y: Array of response variable.
    :type Y: np.ndarray

    :param args: Array of predictor variables.
    :type args: np.ndarray
    """

    def __init__(self, Y: np.ndarray, *args):
        self.Y = Y
        self.args = args
        self.X = np.column_stack((np.ones_like(Y), *args))
        self.N = len(Y)
        self.k = len(args)

    def B_hat(self, X: list = None) -> np.ndarray:
        """
        Method used to calculate the slope of each predictor variable.

        :param X: Optional parameter of predictor variable.
        :type X: np.ndarray

        :return: Array of slopes.
        :rtype: np.ndarray
        """

        if X is None:
            XT = np.transpose(self.X)
            XTXinv = np.linalg.inv(XT @ self.X)
            beta = XTXinv @ (XT @ self.Y)
            return beta
        
        else:
            Xmat = np.column_stack((np.ones_like(self.Y), X[0], X[1]))
            XT = np.transpose(Xmat)
            XTXinv = np.linalg.inv(XT @ Xmat)
            beta = XTXinv @ (XT @ self.Y)
            return beta

    def multiple_linear_regression(self) -> np.ndarray:
        """
        Method used to calculate our multiple linear regression line.

        :return: Multiple linear regression line.
        :rtype: np.ndarray
        """
        b_hat = self.B_hat()
        return self.X @ b_hat
    
    def residuals(self):
        """
        Method used to calculate the difference between our regression line and response variable.

        :return: Residuals.
        :rtype: np.ndarray
        """

        residuals: list = self.Y - self.multiple_linear_regression()

        return residuals
    
    def predict_value(self, *values):
        """
        Method used to predict response values based on the linear regression line.

        :param values: Predictor values used to calculate our response variable.
        :type values: List

        :return: Response variable.
        :rtype: float
        """

        b_hat: list = self.B_hat()

        val: tuple = (1,) + values

        if len(b_hat) != len(values) + 1:

            raise ValueError("there quantity of values provided does not match the number of coeffecients")
        
        return val @ b_hat
    
    def regression_statistics(self):
        """
        Method used to calculate our regression statistics.

        :return: Summary of our regression statistics.
        :rtype: str
        """

        y_pred: list = self.multiple_linear_regression()

        correlation: float = s.correlation(self.Y, y_pred)

        r_square: float = correlation ** 2

        adjusted_r_squared: float = 1 - (((1 - r_square) * (self.N - 1)) / (self.N - 2))

        standard_error: float = np.sqrt(sum(self.residuals() ** 2) / (self.N - self.k - 1))

        return (
                f"------------------------\n"
                f"Regression Statistics\n"
                f"------------------------\n"
                f"Correlation        {correlation:.3f}\n"
                f"R Square           {r_square:.3f}\n"
                f"Adjusted R Square  {adjusted_r_squared:.3f}\n"
                f"Standard Error     {standard_error:.3f}\n"
                f"Observations       {self.N}\n"
                f"------------------------\n"
            )
    
    def anova(self):
        """
        Method used to calculate our anova analysis statistics.

        :return: Summary of our anova statistics.
        :rtype: str
        """

        y_pred: list = self.multiple_linear_regression()

        # DF

        degree_f_regression: int = self.k 
        degree_f_residual: float = self.N - self.k - 1
        degree_f_total: float = self.N - 1

        # SS (sum of squares)
        sum_of_square_total: float = np.sum((self.Y - s.mean(self.Y)) ** 2)
        sum_of_square_regression: float = np.sum((y_pred - np.mean(self.Y)) ** 2)
        sum_of_square_residual: float = np.sum((self.Y - y_pred) ** 2)

        # MS (Mean Square)
        ms_total: float = sum_of_square_total / degree_f_total
        ms_regression: float = sum_of_square_regression / degree_f_regression
        ms_residual: float = sum_of_square_residual / degree_f_residual

        # F The F-statistic, predicts of our model is better at predicting the value vs just using the mean of the independent variable
        f = ms_regression / ms_residual

        # significance f, p-value of F-statistic
        p_value: float = 1 - stats.f.cdf(f, degree_f_regression, degree_f_residual)

        return (
                f"ANOVA\n"
                f"---------------------------------------------------------------------\n"
                f"{'Source':<12} {'df':>4} {'SS':>10} {'MS':>10} {'F':>10} {'Significance F':>18}\n"
                f"---------------------------------------------------------------------\n"
                f"{'Regression':<12} {degree_f_regression:>4} {sum_of_square_regression:>10.3f} {ms_regression:>10.3f} {f:>10.3f} {p_value:>18.11f}\n"
                f"{'Residual':<12} {degree_f_residual:>4} {sum_of_square_residual:>10.3f} {ms_residual:>10.3f}\n"
                f"{'Total':<12} {degree_f_total:>4} {sum_of_square_total:>10.3f}\n"
                f"---------------------------------------------------------------------\n"
            )
    
    def slope_intercept_statistics(self):
        """
        Method used to calculate our slope intercept statistics.

        :return: Summary of our slope intercept statistics.
        :rtype: str
        """

        residuals: list = self.residuals()
        sse: float = np.sum(residuals ** 2)
        mse: float = sse / (self.N - self.k - 1)

        # Coefficients

        coefficients: list = self.B_hat()

        # Standard Error
        XT = np.transpose(self.X)
        XTXinv = np.linalg.inv(XT @ self.X)

        se_coefficients: list = np.sqrt(np.diag(XTXinv) * mse)

        # t-statistics

        t_stat_coeffecient: list = coefficients / se_coefficients

        # p-values

        p_values_coeffecients: list = 2 * (1 - stats.t.cdf(np.abs(t_stat_coeffecient), df=self.N - self.k - 1))

        # Confidence Intervals

        t_critical = stats.t.ppf(1 - 0.025, df=self.N - self.k - 1)
        ci_coeffecients: list = (coefficients - t_critical * se_coefficients, coefficients + t_critical * se_coefficients)

        return (
        f"----------------------------------------------------------------------------------------------------\n"
        f"{'Source':<18}{'Coefficients':>15}{'Standard Error':>17}{'t stat':>10}{'P-value':>10}{'Lower 95%':>15}{'Upper 95%':>15}\n"
        f"----------------------------------------------------------------------------------------------------\n"
        f"{'Intercept':<18}{coefficients[0]:>15.4f}{se_coefficients[0]:>17.4f}{t_stat_coeffecient[0]:>10.4f}{p_values_coeffecients[0]:>10.4f}{ci_coeffecients[0][0]:>15.4f}{ci_coeffecients[1][0]:>15.4f}\n" +
        "\n".join(
            f"{'Variable ' + str(i + 1):<18}{coefficients[i+1]:>15.4f}{se_coefficients[i+1]:>17.4f}{t_stat_coeffecient[i+1]:>10.4f}{p_values_coeffecients[i+1]:>10.4f}{ci_coeffecients[0][i+1]:>15.4f}{ci_coeffecients[1][i+1]:>15.4f}"
            for i in range(len(coefficients) - 1)
        )
        )
    
    def plot3d(self, *variables):
        """
        Method used to plot our multiple linear regression plane.

        :return: Plot of our multiple linear regression.
        :rtype: None
        """
        
        if len(variables) == 2:

            x1 = variables[0]
            x2 = variables[1]

        else:

            x1 = self.args[0]
            x2 = self.args[1]

        X = np.column_stack((x1, x2))

        x1_range = np.linspace(min(x1), max(x1), 20)
        x2_range = np.linspace(min(x2), max(x2), 20)

        X1, X2 = np.meshgrid(x1_range, x2_range)
        X_grid = np.column_stack((np.ones(X1.ravel().shape), X1.ravel(), X2.ravel()))

        b_hat = self.B_hat([x1, x2])
        z = (X_grid @ b_hat).reshape(X1.shape)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # Plot scatter plot of data
        ax.scatter(X[:, 0], X[:, 1], self.Y, color='red', label='Actual data')

        # Plot the 3D surface
        ax.plot_surface(X1, X2, z, color = "blue", alpha = .5)
        plt.title("Multiple Linear Regression")
        ax.set_xlabel('Variable 1')
        ax.set_ylabel('Variable 2')
        ax.set_zlabel('Response')
        ax.legend()
        plt.show()

    def __call__(self, plot3d: list = None, plot2d: list = None):

        print(self.regression_statistics())
        print(self.anova())
        print(self.slope_intercept_statistics())

        if plot3d is not None:

            if len(plot3d) != 2:

                raise ValueError("plot3d must me a list with 2 independent variables")
                        
            self.plot3d(plot3d[0], plot3d[1])

        if plot2d is not None:

            #plt.figure(figsize=(13, 6))

            if len(plot2d) <= 3:

                col: int = len(plot2d)

                row: int = 1

                plt.figure(figsize=(12, 8))

            else:
                
                col: int = 3

                row: int = math.ceil(len(plot2d)/3)

                plt.figure(figsize=(18, 8))

            for i in range(len(plot2d)):

                lin_reg: LinearRegression = LinearRegression(plot2d[i], self.Y)

                regression_line = lin_reg.linear_regression_line()

                #plt.figure(figsize=(13, 6))
                dummy_line1 = mlines.Line2D([], [], color='none', label=f"y = {round(lin_reg.B1(), 3)}X + {round(lin_reg.B0(), 6)}")

                plt.subplot(row, col, i + 1)
                plt.scatter(plot2d[i], self.Y, color = "red")
                plt.plot(plot2d[i], regression_line, label = "Linear Regression")
                plt.title("Linear Regression")
                plt.xlabel("Explanatory Variable")
                plt.ylabel("Response Variable")
                plt.legend(handles=[dummy_line1])
            
            plt.show()

        return 0