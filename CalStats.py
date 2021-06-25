# Calcuating trendline and covariance

import numpy as np



def GetStats(A,B):
    Mat = np.cov(A,B)
    rho = Mat[0,1]/np.sqrt(Mat[0,0]*Mat[1,1])
    
    X = np.ones([np.size(A),2])
    X[:,0] = A
    Xt = np.transpose(X)
    
    y = np.ones([np.size(A),1])
    y[:,0] = B
    
    # (Xt*X)*beta = Xt*y  -> beta =  (Xt*X)^-1 * Xt*y
    LHS=np.matmul(Xt,X)
    RHS=np.matmul(Xt,y)
    beta = np.matmul(np.linalg.inv(LHS),RHS).flatten()
    
    return rho, beta
