"""
#################
# Description:
#################

SQUIC is a second-order, L1-regularized maximum likelihood method for performant large-scale sparse precision matrix estimation.

#################
# Usage :
#################

[X,W,info_times,info_objective,info_logdetX,info_trSX]=SQUIC.run(Y, lambda, max_iter = 100, tol = 1e-3, tol_inv = 1e-4, verbose = 1, M = NULL,  X0 = NULL, W0 = NULL)
[_,S,info_times,_,_,_]=SQUIC.run(Y, lambda, max_iter = 0)

Arguments:
    Y:          Input data in the form p (dimensions) x n (samples).
    lambda:     Scalar tuning parameter a non-zero positive number.
    max_iter:   Maximum number of Newton iterations. Default to 100.
    tol:        Tolerance for convergence. Default to 1e-3.
    tol_inv:    Tolerance for approximate inversion. Default to 1e-4.
    verbose:    Level of printing output (0 or 1). Default to 1.
    M:          A symmetric sparse (p by p); See note (3) below for details.
    X0:         Initial guess of precision matrix as a sparse matrix (p x p).
    W0:         Initial guess of inverse precision matrix as a sparse matrix (p x p) ..

NOTE:
(1) If max_iter=0, the returned value for the inverse of the precision matrix (W) is the sparse sample covariance matrix (S).
(2) The number of threads used by SQUIC can be defined by setting the enviroment variable OMP_NUM_THREADS (e.g., base> export OMP_NUM_THREADS=12). This may require a restart of the session.
(3) The matrix tuning paramter Lambda:=M_{ij} for M_{ij} != 0 and Lambda_{ij}:=lambda, if otherwise. When M=NULL we have Lambda_{ij}=lambda.
(4) After importing the package the user must set the path of the shared library libSQUIC.*, using function SQUIC.PATH_TO_libSQUIC().

Return values:

 X: Estimated precision matrix (p x p).
 W: Estimated inverse of the precision matrix (p x p).
 info_times: Total runtime.
    info_times[0]: Total runtime.
    info_times[1]: Runtime of the sample covariance matrix.
    info_times[2]: Runtime of the Newton steps
    info_times[3]: Runtime of the matrix factorization.
    info_times[4]: Runtime of the approximate matrix inversion.
    info_times[5]: Runtime of the coordinate descent update.
 info_objective: Objective value at each Newton iteration.
 info_logdetX: Log determinant of the estimated precision matrix.
 info_trSX: Trace of the sample covariance matrix times the estimated precision matrix.

#################
# References :
#################

Eftekhari, A., Gaedke-Merzhaeuser, L., Pasadakis, D.,  Bollhöfer, M., Scheidegger, S. and Schenk, O., 2023. Large-Scale Precision Matrix Estimation With SQUIC. ACM Trans. Math. Softw. [Forthcoming], 2023.

Bollhöfer, M., Eftekhari, A., Scheidegger, S. and Schenk, O., 2019. Large-Scale Sparse Inverse Covariance Matrix Estimation.
SIAM Journal on Scientific Computing, 41(1), pp.A380-A401.

Eftekhari, A., Bollhöfer, M. and Schenk, O., 2018, November. Distributed Memory Sparse Inverse Covariance Matrix Estimation
on High-performance Computing Architectures.
In SC18: International Conference for High Performance Computing, Networking, Storage and Analysis (pp. 253-264). IEEE.

Eftekhari, A., Pasadakis, D., Bollhöfer, M., Scheidegger, S. and Schenk, O., 2021. Block-Enhanced Precision Matrix Estimation
for Large-Scale Datasets. Journal of Computational Science, p. 101389.

#################
# Example:
#################
import squic
import numpy as np

# generate sample from tridiagonal precision matrix
p = 1024
n = 100
l = .4

# generate a tridiagonal matrix
np.random.seed(1)
a = -0.5 * np.ones(p-1)
b = 1.25 * np.ones(p)
iC_star = np.diag(a,-1) + np.diag(b,0) + np.diag(a,1)

# generate the data
L = np.linalg.cholesky(iC_star)
Y = np.linalg.solve(L.T,np.random.randn(p,n))

[X,W,info_times,info_objective,info_logdetX,info_trSX] = squic.run(Y,l)
"""

from .squic import *

