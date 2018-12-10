# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from SocialBandits import *
import matplotlib
#not using the X display
matplotlib.use('Agg',force=True)
import matplotlib.pyplot as plt

print(matplotlib.backends.backend)

def testFiniteSocialBandits(P, U0, n, d, H, M, alpha, sigma, lam, delta, scale, finiteSet):

    if finiteSet:
        BanditStrategies = ['LinOptV1',  'RegressionLinREL1FiniteSet', \
                            'LinREL2FiniteSet', 'LinREL1FiniteSet', 'RandomBanditFiniteSet']
        figname = 'linrel1finite_n%d_d%d_h%d_m%d_a%f_s%f_d%f_scale%f'\
                  %(n,d,H,M,alpha,sigma,delta,scale)
    else:
        BanditStrategies = ['LinOptV1', 'LinREL1L2Ball', 'RandomBanditL2Ball']
        figname = 'linrel1_n%d_d%d_h%d_m%d_a%f_s%f_d%f_scale%f'\
                  %(n,d,H,M,alpha,sigma,delta,scale)
        
    rewards = np.zeros((H, len(BanditStrategies)))
    regrets = []
  
    #fake bandit class for generating the finite set
    sb1 = SocialBandit(P,U0)
    sb1.generateFiniteSet(M)
    fst = sb1.getFiniteSet()

    for i, strategy in enumerate(BanditStrategies):
        BanditClass = eval(strategy)
        if "LinREL" in strategy:
            sb = BanditClass(P, U0, alpha, sigma, lam, delta, scale)
        else:
            sb = BanditClass(P, U0, alpha, sigma, lam)
        sb.setFiniteSet(fst, M)
            
        rewards[:,i] = sb.run(H)

        if i > 0:
            regret = np.cumsum(rewards[:,0] - rewards[:,i])
            regrets.append({'bandit': strategy, 'regret': regret})
            plt.plot(regret, label=strategy)
    
    plt.xlabel('Horizon (time step)')
    plt.ylabel('Cumulative Regret')
    plt.legend(loc='upper left')
    plt.savefig(figname+'.pdf',format='pdf')
    #plt.show()
    
    df = pd.DataFrame(regrets)
    df.to_csv('%s.csv'%figname) # it should be renamed
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description = 'Social Bandit Test Runner',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--n', default=100, type=int,help ="Number of users") 
    parser.add_argument('--t', default=500, type=int,help ="Horizon")
    parser.add_argument('--d', default=10, type=int,help ="Number of dimensions") 
    parser.add_argument('--alpha', default=0.05, type=float, help='alpha value. beta is set to 1 - alpha')
    parser.add_argument('--sigma', default=0.05, type=float, help='Standard deviation σ of noise added to responses ')
    parser.add_argument('--lam', default=0.01, type=float, help='Regularization parameter λ used in ridge regression')
    parser.add_argument('--delta', default=0.1, type=float, help='δ value. Used by LinREL')
    parser.add_argument('--scale', default=1, type=float, help=\
            'scale of the β(t)  value. Used by LinREL')
    parser.add_argument('--M',default=100, type=int, help='Size M of finite set. Used by all finite set strategies. ')
    parser.add_argument('--maxiter',default=50, type=int, help='Maximum number of iterations')
    parser.add_argument('--debug',default='INFO', help='Verbosity level',choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    parser.add_argument('--logfile',default='SB.log',help='Log file')
    parser.set_defaults(screen_output=True)
    parser.add_argument('--noscreenoutput',dest="screen_output",action='store_false',help='Suppress screen output')
    parser.add_argument("--randseed",type=int,default=42,help="Random seed")
    parser.add_argument('--finite_set', dest='finite_set', action='store_true', help="Finite set solution")

    args = parser.parse_args()

    np.random.seed(args.randseed)
    random.seed(args.randseed)

    P = generateP(args.n)
    U0 = np.random.randn(args.n,args.d)

    testFiniteSocialBandits(P, U0, args.n, args.d, args.t, args.M,\
                            args.alpha, args.sigma, args.lam, args.delta, args.scale, args.finite_set) 
