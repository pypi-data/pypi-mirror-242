"""from regression import LinearRegression
from regression import MultipleLinearRegression
from statistic import *
from distributions import *
from confidence_interval import *
from likelihoods import *
from hypothesis_testing import TestStatistic
from hypothesis_testing import PValue
from hypothesis_testing import HypothesisTesting
from bayesian_statistics import ConjugatePrior
from bayesian_statistics import Bayesian
from pca import PCA
from data import Data"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import scipy.stats as stats

import pyez_stats.statistic
import pyez_stats.likelihoods
import pyez_stats.distributions

from pyez_stats.confidence_interval import ConfidenceInterval
from pyez_stats.confidence_interval import confidence_interval
from pyez_stats.bayesian_statistics import ConjugatePrior
from pyez_stats.bayesian_statistics import Bayesian
from pyez_stats.hypothesis_testing import TestStatistic
from pyez_stats.hypothesis_testing import PValue
from pyez_stats.hypothesis_testing import HypothesisTesting
from pyez_stats.regression import LinearRegression
from pyez_stats.regression import MultipleLinearRegression
from pyez_stats.pca import PCA
from pyez_stats.data import Data

from  .distributions import Gaussian
from  .distributions import Exponential 
from  .distributions import Bernoulli
from  .distributions import Poisson
from  .distributions import Binomial
from  .distributions import Uniform
from  .distributions import Geometric