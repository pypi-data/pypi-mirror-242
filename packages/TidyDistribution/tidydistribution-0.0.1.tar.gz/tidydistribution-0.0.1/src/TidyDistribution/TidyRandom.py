import scipy.stats as sts
import warnings
# 禁用警告
warnings.filterwarnings("ignore")


def TidyRandom(size=1, random_state=None, whichdist=None, **kwargs):
    """
    这是一个Scipy随机数生成函数的文档字符串。

    参数:
    size (int or tuple): 抽样大小
    random_state (int): 随机数种子
    whichdist (str): 分布类型
    {
        "bernoulli", 伯努利分布(p,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_bernoulli.html}。
        "betabinom", 贝塔二项分布(n,a,b,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_betabinom.html}。
        "binom", 二项分布(n,p,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_binom.html}。
        "boltzmann", 截断Planck分布(lambda_,N,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_boltzmann.html}。
        "planck", 离散指数分布(lambda_,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_planck.html}。
        "poiss", 泊松分布(mu,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_poisson.html}。
        "geom", 几何分布(p,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_geom.html}。
        "nbinom", 负二项分布(n,p,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_geom.html}。
        "hgeom", 超几何分布(M,n,N,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_hypergeom.html}。
        "nchgeomfisher", 非中心化的Fisher超几何分布(M,n,N,odds,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_nchypergeom_fisher.html}。
        "nchgeomWallenius", 非中心化的Wallenius超几何分布(M,n,N,odds,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_nchypergeom_wallenius.html}。
        "nhgeom", 负超几何分布(M,n,r,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_nhypergeom.html}。
        "zeta", 泽塔分布(a,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_zipf.html}。
        "zipfian", zipfian分布(a,n,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_zipfian.html}。
        "logseries", 对数级数分布(p,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_logser.html}。
        "duniform", 离散均匀分布(low,high,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_randint.html}。
        "dlaplace", 离散型拉普拉斯分布(a,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_dlaplace.html}。
        "yulesimon", Yule-Simon分布(alpha,loc){https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_yulesimon.html}。
        "alpha", alpha分布(a,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_alpha.html}。
        "anglit", anglit分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_anglit.html}。
        "arcsin", arcsin分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_arcsine.html}。
        "beta", beta分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_beta.html}。
        "betaprime", betaprime分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_betaprime.html}。
        "bradford", bradford分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_bradford.html}。
        "burr", burr分布(c,d,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_burr.html}。
        "burr12", burr12分布(c,d,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_burr12.html}。
        "cauchy", cauchy分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_cauchy.html}。
        "skewcauchy", skewcauchy分布(a,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_skewcauchy.html}。
        "chi", chi分布(df,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_chi.html}。
        "chi2", chi2分布(df,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_chi2.html}。
        "cosine", cosine分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_cosine.html}。
        "dgamma", dgamma分布(a,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_dgamma.html}。
        "dweibull", dweibull分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_dweibull.html}。
        "exp", 指数分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_expon.html}。
        "expweibull", expweibull分布(a,c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_exponweib.html}。
        "exppower", exppower分布(b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_exponpow.html}。
        "fatigurlife", fatiguelife分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_fatiguelife.html}。
        "loglogistic", loglogistic分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_fisk.html}。
        "foldcauchy", foldcauchy分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_foldcauchy.html}。
        "foldnormal", foldnormal分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_foldnorm.html}。
        "f", F分布(dfn,dfd,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_f.html}。
        "gamma", gamma分布(a,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_gamma.html}。
        "glogistic", genelized logistic分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_genlogistic.html}。
        "gpareto", genelized pareto分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_genpareto.html}。
        "gexp", genelized指数分布(a,b,c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_genexpon.html}。
        "gextremevalue", genelized extreme value分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_genextreme.html}。
        "ggamma", genelized gamma分布(a,c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_gengamma.html}。
        "ghalflogistic", genelized half logistic分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_genhalflogistic.html}。
        "gigauss", genelized inverse gaussian分布(p,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_geninvgauss.html}。
        "gnorm", genelized normal分布(beta,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_gennorm.html}。
        "gibrat", gibrat分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_gibrat.html}。
        "gompertz", gompertz分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_gompertz.html}。
        "halfcauchy", half cauchy分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_halfcauchy.html}。
        "halfnorm", half normal分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_halfnorm.html}。
        "halflogistic", half logistic分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_halflogistic.html}。
        "hypsecant", hypsecant分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_hypsecant.html}。
        "gausshgeom", gaussian hypergeom分布(a,b,c,z,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_gausshyper.html}。
        "invgamma", inverse gamma分布(a,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_invgamma.html}。
        "invgauss", inverse gaussian分布(mu,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_invgauss.html}。
        "invweibull", inverse weibull分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_invweibull.html}。
        "JohnsonSB", JohnsonSB分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_johnsonsb.html}。
        "JohnsonSU", JohnsonSU分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_johnsonsu.html}。
        "KSone", KSone分布(n,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_ksone.html}。
        "KStwo", KStwo分布(n,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_kstwo.html}。
        "KStwobign", KStwobign分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_kstwobign.html}。
        "laplace", 拉普拉斯分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_laplace.html}。
        "AsymmetricLaplace", 不对称拉普拉斯分布(kappa,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_laplace_asymmetric.html}。
        "Left-skewed-Levy", 左偏Levy分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_levy_l.html}。
        "levy", levy分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_levy.html}。
        "logistic", logistic分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_logistic.html}。
        "loglaplace", 对数拉普拉斯分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_loglaplace.html}。
        "loggamma", 对数gamma分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_loggamma.html}。
        "lognorm", 对数正态分布(s,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_lognorm.html}。
        "loguniform", 对数均匀分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_loguniform.html}。
        "maxwell", maxwell分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_maxwell.html}。
        "Mielke-Beta-Kappa", Mielke-Beta-Kappa分布(k,s,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_mielke.html}。
        "Nakagami", Nakagami分布(nu,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_nakagami.html}。
        "ncchi2", 非中心的卡方分布(df,nc,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_ncx2.html}。
        "ncf", 非中心的F分布(dfn,dfd,nc,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_ncf.html}。
        "nct", 非中心的t分布(df,nc,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_nct.html}。
        "norm", 正态分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_norm.html}。
        "NormalInverseGaussian", NormalInverseGaussian分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_norminvgauss.html}。
        "pareto", 帕累托分布(b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_pareto.html}。
        "lomax", lomax分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_lomax.html}。
        "PowerlogNorm", PowerlogNorm分布(c,s,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_powerlognorm.html}。
        "PowerNormal", PowerNormal分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_powernorm.html}。
        "PowerLaw", PowerLaw分布(a,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_powerlaw.html}。
        "Rdistribution", Rdistribution分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_rdist.html}。
        "rayleigh", rayleigh分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_rayleigh.html}。
        "rice", rice分布(b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_rice.html}。
        "semicircular", semicircular分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_semicircular.html}。
        "Studentized-Range", 学生化Range分布(k,df,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_studentized_range.html}。
        "t", t分布(df,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_t.html}。
        "Trapezoidal", Trapezoidal分布(c,d,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_trapezoid.html}。
        "Triangular", Triangular分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_triang.html}。
        "TruncatedExpon", 截断指数分布(b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_truncexpon.html}。
        "TruncatedNormal", 截断正态分布(a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_truncnorm.html}。
        "TruncatedPareto", 截断帕累托分布(b,c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_truncpareto.html}。
        "TruncatedWeibullMin", TruncatedWeibullMin分布(c,a,b,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_truncweibull_min.html}。
        "uniform", 均匀分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_uniform.html}。
        "wald", wald分布(loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_wald.html}。
        "WeibullMax", WeibullMax分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_weibull_max.html}。
        "WeibullMin", WeibullMin分布(c,loc,scale){https://docs.scipy.org/doc/scipy/tutorial/stats/continuous_weibull_min.html}。
        "MultiNorm", 多元正态分布(mean,cov){https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multivariate_normal.html}。
        "MultiT", 多元t分布(loc,shape,df){https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multivariate_t.html}。
        "MultiNomial", 多项分布(n,p){https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.multinomial.html}。
        "invwishart", 逆威沙特分布(df, scale){https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.invwishart.html}。
        "wishart", 威沙特分布(df, scale){https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wishart.html}。
        "dirichlet", 狄利克雷分布(alpha){https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.dirichlet.html}。
    }。

    特别说明，其中的参数loc和scale基本都表示下面的含义：
    y=(x-loc)/scale的分布和x;loc,scale的分布是等价的，但也有例外，比如均匀分布。

    示例:
    ===============================================================================0
    导入模块
    >>> from TidyDistribution import TidyRandom
    >>> from TidyDistribution import TidySample
    >>> import numpy as np
    ===============================================================================1
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="bernoulli", p=0.3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="bernoulli", p=0.8, loc=3)
    >>> print(y)
    ===============================================================================2
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="betabinom", n=10, a=1, b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="betabinom", n=10, a=1, b=2, loc=3)
    >>> print(y)
    ===============================================================================3
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="binom", n=10, p=0.6)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="binom", n=10, p=0.2, loc=3)
    >>> print(y)
    ===============================================================================4
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="boltzmann", lambda_=10, N=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="boltzmann", lambda_=10, N=3, loc=3)
    >>> print(y)
    ===============================================================================5
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="planck", lambda_=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="planck", lambda_=1, loc=3)
    >>> print(y)
    ===============================================================================6
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="poiss", mu=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="poiss", mu=1, loc=3)
    >>> print(y)
    ===============================================================================7
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="geom", p=0.1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="geom", p=0.9, loc=3)
    >>> print(y)
    ===============================================================================8
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="nbinom", n=10, p=0.1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="nbinom", n=10, p=0.9, loc=3)
    >>> print(y)
    ===============================================================================9
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="hgeom", M=20, n=10, N=10)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="hgeom", M=20, n=10, N=10, loc=3)
    >>> print(y)
    ===============================================================================10
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="nchgeomfisher", M=20, n=10, N=10, odds=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="nchgeomfisher", M=20, n=10, N=10, odds=2, loc=3)
    >>> print(y)
    ===============================================================================11
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="nchgeomWallenius", M=20, n=10, N=10, odds=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="nchgeomWallenius", M=20, n=10, N=10, odds=2, loc=3)
    >>> print(y)
    ===============================================================================12
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="nhgeom", M=20, n=10, r=10)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="nhgeom", M=20, n=10, r=10, loc=3)
    >>> print(y)
    ===============================================================================13
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="zeta", a=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="zeta", a=2, loc=3)
    >>> print(y)
    ===============================================================================14
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="zipfian", a=2, n=10)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="zipfian", a=2, n=10, loc=3)
    >>> print(y)
    ===============================================================================15
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="logseries", p=0.9)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="logseries", p=0.1, loc=3)
    >>> print(y)
    ===============================================================================16
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="duniform", low=1, high=10)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="duniform", low=1, high=10, loc=3)
    >>> print(y)
    ===============================================================================17
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="dlaplace", a=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="dlaplace", a=3, loc=3)
    >>> print(y)
    ===============================================================================18
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="yulesimon", alpha=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="yulesimon", alpha=3, loc=3)
    >>> print(y)
    ===============================================================================19
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="alpha", a=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="alpha", a=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================20
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="anglit")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="anglit", loc=3, scale=2)
    >>> print(y)
    ===============================================================================21
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="arcsin")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="arcsin", loc=3, scale=2)
    >>> print(y)
    ===============================================================================22
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="beta", a=1, b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="beta", a=1, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================23
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="betaprime", a=1, b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="betaprime", a=1, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================24
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="bradford", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="bradford", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================25
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="burr", c=2, d=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="burr", c=2, d=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================26
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="burr12", c=2, d=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="burr12", c=2, d=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================27
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="cauchy")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="cauchy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================28
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="skewcauchy", a=0.2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="skewcauchy", a=0.2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================29
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="chi", df=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="chi", df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================30
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="chi2", df=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="chi2", df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================31
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="cosine")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="cosine", loc=3, scale=2)
    >>> print(y)
    ===============================================================================32
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="dgamma", a=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="dgamma", a=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================33
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="dweibull", c=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="dweibull", c=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================34
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="exp")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="exp", loc=3, scale=2)
    >>> print(y)
    ===============================================================================35
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="expweibull", a=1, c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="expweibull", a=1, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================36
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="exppower", b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="exppower", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================37
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="fatigurlife", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="fatigurlife", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================38
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="loglogistic", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="loglogistic", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================39
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="foldcauchy", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="foldcauchy", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================40
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="foldnormal", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="foldnormal", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================41
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="f", dfn=2, dfd=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="f", dfn=2, dfd=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================42
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gamma", a=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gamma", a=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================43
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="glogistic", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="glogistic", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================44
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gpareto", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gpareto", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================45
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gexp", a=2, b=1, c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gexp", a=2, b=1, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================46
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gextremevalue", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gextremevalue", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================47
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="ggamma", a=2, c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="ggamma", a=2, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================48
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="ghalflogistic", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="ghalflogistic", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================49
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gigauss", p=2, b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gigauss", p=2, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================50
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gnorm", beta=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gnorm", beta=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================51
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gibrat")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gibrat", loc=3, scale=2)
    >>> print(y)
    ===============================================================================52
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gompertz", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gompertz", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================53
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="halfcauchy")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="halfcauchy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================54
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="halfnorm")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="halfnorm", loc=3, scale=2)
    >>> print(y)
    ===============================================================================55
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="halflogistic")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="halflogistic", loc=3, scale=2)
    >>> print(y)
    ===============================================================================56
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="halflogistic")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="halflogistic", loc=3, scale=2)
    >>> print(y)
    ===============================================================================57
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="hypsecant")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="hypsecant", loc=3, scale=2)
    >>> print(y)
    ===============================================================================58
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="gausshgeom", a=1, b=1, c=2, z=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="gausshgeom", a=1, b=1, c=2, z=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================59
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="invgamma", a=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="invgamma", a=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================60
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="invgauss", mu=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="invgauss", mu=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================61
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="invweibull", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="invweibull", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================62
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="JohnsonSB", a=2, b=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="JohnsonSB", a=2, b=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================63
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="JohnsonSU", a=2, b=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="JohnsonSU", a=2, b=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================64
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="KSone", n=10)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="KSone", n=10, loc=3, scale=2)
    >>> print(y)
    ===============================================================================65
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="KStwo", n=100)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="KStwo", n=100, loc=3, scale=2)
    >>> print(y)
    ===============================================================================66
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="KStwobign")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="KStwobign", loc=3, scale=2)
    >>> print(y)
    ===============================================================================67
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="laplace")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="laplace", loc=3, scale=2)
    >>> print(y)
    ===============================================================================68
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="AsymmetricLaplace", kappa=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="AsymmetricLaplace", kappa=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================69
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Left-skewed-Levy")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Left-skewed-Levy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================70
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="levy")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="levy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================71
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="logistic")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="logistic", loc=3, scale=2)
    >>> print(y)
    ===============================================================================72
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="loglaplace", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="loglaplace", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================73
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="loggamma", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="loggamma", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================74
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="lognorm", s=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="lognorm", s=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================75
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="loguniform", a=2, b=3)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="loguniform", a=2, b=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================76
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="maxwell")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="maxwell", loc=3, scale=2)
    >>> print(y)
    ===============================================================================77
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Mielke-Beta-Kappa", k=1, s=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Mielke-Beta-Kappa", k=1, s=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================78
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Nakagami", nu=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Nakagami", nu=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================79
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="ncchi2", df=2, nc=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="ncchi2", df=2, nc=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================80
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="ncf", dfn=2, dfd=2, nc=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="ncf", dfn=2, dfd=2, nc=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================81
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="nct", df=2, nc=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="nct", df=2, nc=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================82
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="norm")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="norm", loc=3, scale=2)
    >>> print(y)
    ===============================================================================83
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="NormalInverseGaussian", a=1, b=0.2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="NormalInverseGaussian", a=1, b=0.2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================84
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="pareto", b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="pareto", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================85
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="lomax", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="lomax", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================86
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="PowerlogNorm", c=2, s=1)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="PowerlogNorm", c=2, s=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================87
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="PowerNormal", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="PowerNormal", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================88
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="PowerLaw", a=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="PowerLaw", a=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================89
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Rdistribution", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Rdistribution", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================90
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="rayleigh")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="rayleigh", loc=3, scale=2)
    >>> print(y)
    ===============================================================================91
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="rice", b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="rice", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================92
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="semicircular")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="semicircular", loc=3, scale=2)
    >>> print(y)
    ===============================================================================93
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Studentized-Range", k=2, df=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Studentized-Range", k=2, df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================94
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="t", df=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="t", df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================95
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Trapezoidal", c=0.2, d=0.5)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Trapezoidal", c=0.2, d=0.5, loc=3, scale=2)
    >>> print(y)
    ===============================================================================96
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="Triangular", c=0.2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="Triangular", c=0.2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================97
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="TruncatedExpon", b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="TruncatedExpon", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================98
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="TruncatedNormal", a=1, b=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="TruncatedNormal", a=1, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================99
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="TruncatedPareto", b=0.1, c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="TruncatedPareto", b=0.1, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================100
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="TruncatedWeibullMin", a=0.2, b=2, c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="TruncatedWeibullMin", a=0.2, b=2, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================101
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="uniform")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="uniform", loc=3, scale=2)
    >>> print(y)
    ===============================================================================102
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="wald")
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="wald", loc=3, scale=2)
    >>> print(y)
    ===============================================================================103
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="WeibullMax", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="WeibullMax", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================104
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="WeibullMin", c=2)
    >>> print(y)
    >>> y = TidyRandom(size=size, whichdist="WeibullMin", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================105
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="MultiNorm", mean=np.zeros(2), cov=np.identity(2))
    >>> print(y)
    ===============================================================================106
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="MultiT", loc=np.zeros(2), shape=np.identity(2), df=2)
    >>> print(y)
    ===============================================================================107
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="MultiNomial", n=20, p=[0.3,0.5,0.2])
    >>> print(y)
    ===============================================================================108
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="invwishart", df=4, scale=np.identity(3))
    >>> print(y)
    ===============================================================================109
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="wishart", df=4, scale=np.identity(3))
    >>> print(y)
    ===============================================================================110
    >>> size=100
    >>> y = TidyRandom(size=size, whichdist="dirichlet", alpha=[0.1,0.8,0.2])
    >>> print(y)
    ===============================================================================111
    """
    res = None
    if whichdist == "bernoulli":
        res = sts.bernoulli.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "betabinom":
        res = sts.betabinom.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "binom":
        res = sts.binom.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "boltzmann":
        res = sts.boltzmann.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "planck":
        res = sts.planck.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "poiss":
        res = sts.poisson.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "geom":
        res = sts.geom.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "nbinom":
        res = sts.nbinom.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "hgeom":
        res = sts.hypergeom.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "nchgeomfisher":
        res = sts.nchypergeom_fisher.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "nchgeomWallenius":
        res = sts.nchypergeom_wallenius.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "nhgeom":
        res = sts.nhypergeom.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "zeta":
        res = sts.zipf.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "zipfian":
        res = sts.zipfian.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "logseries":
        res = sts.logser.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "duniform":
        res = sts.randint.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "dlaplace":
        res = sts.dlaplace.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "yulesimon":
        res = sts.yulesimon.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "alpha":
        res = sts.alpha.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "anglit":
        res = sts.anglit.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "arcsin":
        res = sts.arcsine.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "beta":
        res = sts.beta.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "betaprime":
        res = sts.betaprime.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "bradford":
        res = sts.bradford.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "burr":
        res = sts.burr.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "burr12":
        res = sts.burr12.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "cauchy":
        res = sts.cauchy.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "skewcauchy":
        res = sts.skewcauchy.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "chi":
        res = sts.chi.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "chi2":
        res = sts.chi2.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "cosine":
        res = sts.cosine.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "dgamma":
        res = sts.dgamma.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "dweibull":
        res = sts.dweibull.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "exp":
        res = sts.expon.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "expweibull":
        res = sts.exponweib.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "exppower":
        res = sts.exponpow.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "fatigurlife":
        res = sts.fatiguelife.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "loglogistic":
        res = sts.fisk.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "foldcauchy":
        res = sts.foldcauchy.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "foldnormal":
        res = sts.foldnorm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "f":
        res = sts.f.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "gamma":
        res = sts.gamma.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "glogistic":
        res = sts.genlogistic.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "gpareto":
        res = sts.genpareto.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "gexp":
        res = sts.genexpon.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "gextremevalue":
        res = sts.genextreme.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "ggamma":
        res = sts.gengamma.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "ghalflogistic":
        res = sts.genhalflogistic.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "gigauss":
        res = sts.geninvgauss.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "gnorm":
        res = sts.gennorm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "gibrat":
        res = sts.gibrat.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "gompertz":
        res = sts.gompertz.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "halfcauchy":
        res = sts.halfcauchy.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "halfnorm":
        res = sts.halfnorm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "halflogistic":
        res = sts.halflogistic.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "hypsecant":
        res = sts.hypsecant.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "gausshgeom":
        res = sts.gausshyper.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "invgamma":
        res = sts.invgamma.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "invgauss":
        res = sts.invgauss.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "invweibull":
        res = sts.invweibull.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "JohnsonSB":
        res = sts.johnsonsb.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "JohnsonSU":
        res = sts.johnsonsu.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "KSone":
        res = sts.ksone.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "KStwo":
        res = sts.kstwo.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "KStwobign":
        res = sts.kstwobign.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "laplace":
        res = sts.laplace.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "AsymmetricLaplace":
        res = sts.laplace_asymmetric.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "Left-skewed-Levy":
        res = sts.levy_l.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "levy":
        res = sts.levy.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "logistic":
        res = sts.logistic.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "loglaplace":
        res = sts.loglaplace.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "loggamma":
        res = sts.loggamma.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "lognorm":
        res = sts.lognorm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "loguniform":
        res = sts.loguniform.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "maxwell":
        res = sts.maxwell.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "Mielke-Beta-Kappa":
        res = sts.mielke.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "Nakagami":
        res = sts.nakagami.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "ncchi2":
        res = sts.ncx2.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "ncf":
        res = sts.ncf.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "nct":
        res = sts.nct.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "norm":
        res = sts.norm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "NormalInverseGaussian":
        res = sts.norminvgauss.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "pareto":
        res = sts.pareto.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "lomax":
        res = sts.lomax.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "PowerlogNorm":
        res = sts.powerlognorm.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "PowerNormal":
        res = sts.powernorm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "PowerLaw":
        res = sts.powerlaw.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "Rdistribution":
        res = sts.rdist.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "rayleigh":
        res = sts.rayleigh.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "rice":
        res = sts.rice.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "semicircular":
        res = sts.semicircular.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "Studentized-Range":
        res = sts.studentized_range.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "t":
        res = sts.t.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "Trapezoidal":
        res = sts.trapezoid.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "Triangular":
        res = sts.triang.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "TruncatedExpon":
        res = sts.truncexpon.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "TruncatedNormal":
        res = sts.truncnorm.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "TruncatedPareto":
        res = sts.truncpareto.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "TruncatedWeibullMin":
        res = sts.truncweibull_min.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "uniform":
        res = sts.uniform.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "wald":
        res = sts.wald.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "WeibullMax":
        res = sts.weibull_max.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "WeibullMin":
        res = sts.weibull_min.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "MultiNorm":
        res = sts.multivariate_normal.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "MultiT":
        res = sts.multivariate_t.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "MultiNomial":
        res = sts.multinomial.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "invwishart":
        res = sts.invwishart.rvs(
            size=size, random_state=random_state, **kwargs)
    elif whichdist == "wishart":
        res = sts.wishart.rvs(size=size, random_state=random_state, **kwargs)
    elif whichdist == "dirichlet":
        res = sts.dirichlet.rvs(size=size, random_state=random_state, **kwargs)
    else:
        pass
    return res
