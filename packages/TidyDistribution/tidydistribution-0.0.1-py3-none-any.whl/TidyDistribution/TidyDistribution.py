import scipy.stats as sts
import warnings
# 禁用警告
warnings.filterwarnings("ignore")


def TidyDistribution(x, whichdist=None, **kwargs):
    """
    这是一个Scipy累积分布函数的文档字符串。

    参数:
    x (sequence): 分布函数的自变量
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
    }。

    特别说明，其中的参数loc和scale基本都表示下面的含义：
    y=(x-loc)/scale的分布和x;loc,scale的分布是等价的，但也有例外，比如均匀分布。

    示例：
    ===============================================================================0
    导入模块
    >>> from TidyDistribution import TidyDistribution
    >>> from TidyDistribution import TidySample
    >>> import numpy as np
    ===============================================================================1
    >>> x = TidySample([0,1], size=10, isreplace=1)
    >>> y = TidyDistribution(x, whichdist="bernoulli", p=0.3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="bernoulli", p=0.8, loc=3)
    >>> print(y)
    ===============================================================================2
    >>> x = np.arange(10)
    >>> y = TidyDistribution(x, whichdist="betabinom", n=10, a=1, b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="betabinom", n=10, a=1, b=2, loc=3)
    >>> print(y)
    ===============================================================================3
    >>> x = np.arange(10)
    >>> y = TidyDistribution(x, whichdist="binom", n=10, p=0.6)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="binom", n=10, p=0.2, loc=3)
    >>> print(y)
    ===============================================================================4
    >>> x = np.arange(10)
    >>> y = TidyDistribution(x, whichdist="boltzmann", lambda_=10, N=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="boltzmann", lambda_=10, N=3, loc=3)
    >>> print(y)
    ===============================================================================5
    >>> x = np.arange(10)
    >>> y = TidyDistribution(x, whichdist="planck", lambda_=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="planck", lambda_=1, loc=3)
    >>> print(y)
    ===============================================================================6
    >>> x = np.arange(10)
    >>> y = TidyDistribution(x, whichdist="poiss", mu=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="poiss", mu=1, loc=3)
    >>> print(y)
    ===============================================================================7
    >>> x = np.arange(1, 10)
    >>> y = TidyDistribution(x, whichdist="geom", p=0.1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="geom", p=0.9, loc=3)
    >>> print(y)
    ===============================================================================8
    >>> x = np.arange(1, 10)
    >>> y = TidyDistribution(x, whichdist="nbinom", n=10, p=0.1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="nbinom", n=10, p=0.9, loc=3)
    >>> print(y)
    ===============================================================================9
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="hgeom", M=20, n=10, N=10)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="hgeom", M=20, n=10, N=10, loc=3)
    >>> print(y)
    ===============================================================================10
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="nchgeomfisher", M=20, n=10, N=10, odds=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="nchgeomfisher", M=20, n=10, N=10, odds=2, loc=3)
    >>> print(y)
    ===============================================================================11
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="nchgeomWallenius", M=20, n=10, N=10, odds=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="nchgeomWallenius", M=20, n=10, N=10, odds=2, loc=3)
    >>> print(y)
    ===============================================================================12
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="nhgeom", M=20, n=10, r=10)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="nhgeom", M=20, n=10, r=10, loc=3)
    >>> print(y)
    ===============================================================================13
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="zeta", a=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="zeta", a=2, loc=3)
    >>> print(y)
    ===============================================================================14
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="zipfian", a=2, n=10)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="zipfian", a=2, n=10, loc=3)
    >>> print(y)
    ===============================================================================15
    >>> x = np.arange(1, 20)
    >>> y = TidyDistribution(x, whichdist="logseries", p=0.9)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="logseries", p=0.1, loc=3)
    >>> print(y)
    ===============================================================================16
    >>> x = np.arange(1, 12)
    >>> y = TidyDistribution(x, whichdist="duniform", low=1, high=10)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="duniform", low=1, high=10, loc=3)
    >>> print(y)
    ===============================================================================17
    >>> x = np.arange(1, 12)
    >>> y = TidyDistribution(x, whichdist="dlaplace", a=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="dlaplace", a=3, loc=3)
    >>> print(y)
    ===============================================================================18
    >>> x = np.arange(1, 12)
    >>> y = TidyDistribution(x, whichdist="yulesimon", alpha=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="yulesimon", alpha=3, loc=3)
    >>> print(y)
    ===============================================================================19
    >>> x = np.linspace(0.01, 10, 100)
    >>> y = TidyDistribution(x, whichdist="alpha", a=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="alpha", a=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================20
    >>> x = np.linspace(-np.pi/4, np.pi/4, 100)
    >>> y = TidyDistribution(x, whichdist="anglit")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="anglit", loc=3, scale=2)
    >>> print(y)
    ===============================================================================21
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="arcsin")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="arcsin", loc=3, scale=2)
    >>> print(y)
    ===============================================================================22
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="beta", a=1, b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="beta", a=1, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================23
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="betaprime", a=1, b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="betaprime", a=1, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================24
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="bradford", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="bradford", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================25
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="burr", c=2, d=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="burr", c=2, d=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================26
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="burr12", c=2, d=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="burr12", c=2, d=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================27
    >>> x = np.linspace(-1, 1, 100)
    >>> y = TidyDistribution(x, whichdist="cauchy")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="cauchy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================28
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="skewcauchy", a=0.2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="skewcauchy", a=0.2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================29
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="chi", df=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="chi", df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================30
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="chi2", df=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="chi2", df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================31
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="cosine")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="cosine", loc=3, scale=2)
    >>> print(y)
    ===============================================================================32
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="dgamma", a=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="dgamma", a=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================33
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="dweibull", c=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="dweibull", c=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================34
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="exp")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="exp", loc=3, scale=2)
    >>> print(y)
    ===============================================================================35
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="expweibull", a=1, c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="expweibull", a=1, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================36
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="exppower", b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="exppower", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================37
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="fatigurlife", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="fatigurlife", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================38
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="loglogistic", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="loglogistic", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================39
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="foldcauchy", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="foldcauchy", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================40
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="foldnormal", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="foldnormal", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================41
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="f", dfn=2, dfd=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="f", dfn=2, dfd=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================42
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gamma", a=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gamma", a=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================43
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="glogistic", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="glogistic", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================44
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gpareto", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gpareto", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================45
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gexp", a=2, b=1, c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gexp", a=2, b=1, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================46
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gextremevalue", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gextremevalue", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================47
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="ggamma", a=2, c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="ggamma", a=2, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================48
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="ghalflogistic", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="ghalflogistic", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================49
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gigauss", p=2, b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gigauss", p=2, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================50
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gnorm", beta=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gnorm", beta=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================51
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gibrat")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gibrat", loc=3, scale=2)
    >>> print(y)
    ===============================================================================52
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gompertz", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gompertz", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================53
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="halfcauchy")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="halfcauchy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================54
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="halfnorm")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="halfnorm", loc=3, scale=2)
    >>> print(y)
    ===============================================================================55
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="halflogistic")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="halflogistic", loc=3, scale=2)
    >>> print(y)
    ===============================================================================56
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="halflogistic")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="halflogistic", loc=3, scale=2)
    >>> print(y)
    ===============================================================================57
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="hypsecant")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="hypsecant", loc=3, scale=2)
    >>> print(y)
    ===============================================================================58
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="gausshgeom", a=1, b=1, c=2, z=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="gausshgeom", a=1, b=1, c=2, z=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================59
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="invgamma", a=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="invgamma", a=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================60
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="invgauss", mu=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="invgauss", mu=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================61
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="invweibull", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="invweibull", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================62
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="JohnsonSB", a=2, b=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="JohnsonSB", a=2, b=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================63
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="JohnsonSU", a=2, b=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="JohnsonSU", a=2, b=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================64
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="KSone", n=10)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="KSone", n=10, loc=3, scale=2)
    >>> print(y)
    ===============================================================================65
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="KStwo", n=100)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="KStwo", n=100, loc=3, scale=2)
    >>> print(y)
    ===============================================================================66
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="KStwobign")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="KStwobign", loc=3, scale=2)
    >>> print(y)
    ===============================================================================67
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="laplace")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="laplace", loc=3, scale=2)
    >>> print(y)
    ===============================================================================68
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="AsymmetricLaplace", kappa=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="AsymmetricLaplace", kappa=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================69
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Left-skewed-Levy")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Left-skewed-Levy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================70
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="levy")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="levy", loc=3, scale=2)
    >>> print(y)
    ===============================================================================71
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="logistic")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="logistic", loc=3, scale=2)
    >>> print(y)
    ===============================================================================72
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="loglaplace", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="loglaplace", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================73
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="loggamma", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="loggamma", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================74
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="lognorm", s=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="lognorm", s=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================75
    >>> x = np.linspace(1, 4, 100)
    >>> y = TidyDistribution(x, whichdist="loguniform", a=2, b=3)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="loguniform", a=2, b=3, loc=3, scale=2)
    >>> print(y)
    ===============================================================================76
    >>> x = np.linspace(1, 4, 100)
    >>> y = TidyDistribution(x, whichdist="maxwell")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="maxwell", loc=3, scale=2)
    >>> print(y)
    ===============================================================================77
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Mielke-Beta-Kappa", k=1, s=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Mielke-Beta-Kappa", k=1, s=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================78
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Nakagami", nu=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Nakagami", nu=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================79
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="ncchi2", df=2, nc=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="ncchi2", df=2, nc=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================80
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="ncf", dfn=2, dfd=2, nc=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="ncf", dfn=2, dfd=2, nc=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================81
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="nct", df=2, nc=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="nct", df=2, nc=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================82
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="norm")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="norm", loc=3, scale=2)
    >>> print(y)
    ===============================================================================83
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="NormalInverseGaussian", a=1, b=0.2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="NormalInverseGaussian", a=1, b=0.2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================84
    >>> x = np.linspace(1, 10, 100)
    >>> y = TidyDistribution(x, whichdist="pareto", b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="pareto", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================85
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="lomax", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="lomax", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================86
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="PowerlogNorm", c=2, s=1)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="PowerlogNorm", c=2, s=1, loc=3, scale=2)
    >>> print(y)
    ===============================================================================87
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="PowerNormal", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="PowerNormal", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================88
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="PowerLaw", a=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="PowerLaw", a=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================89
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Rdistribution", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Rdistribution", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================90
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="rayleigh")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="rayleigh", loc=3, scale=2)
    >>> print(y)
    ===============================================================================91
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="rice", b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="rice", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================92
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="semicircular")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="semicircular", loc=3, scale=2)
    >>> print(y)
    ===============================================================================93
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Studentized-Range", k=2, df=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Studentized-Range", k=2, df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================94
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="t", df=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="t", df=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================95
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Trapezoidal", c=0.2, d=0.5)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Trapezoidal", c=0.2, d=0.5, loc=3, scale=2)
    >>> print(y)
    ===============================================================================96
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="Triangular", c=0.2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="Triangular", c=0.2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================97
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="TruncatedExpon", b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="TruncatedExpon", b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================98
    >>> x = np.linspace(1, 3, 100)
    >>> y = TidyDistribution(x, whichdist="TruncatedNormal", a=1, b=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="TruncatedNormal", a=1, b=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================99
    >>> x = np.linspace(1, 2, 100)
    >>> y = TidyDistribution(x, whichdist="TruncatedPareto", b=0.1, c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="TruncatedPareto", b=0.1, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================100
    >>> x = np.linspace(1, 2, 100)
    >>> y = TidyDistribution(x, whichdist="TruncatedWeibullMin", a=0.2, b=2, c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="TruncatedWeibullMin", a=0.2, b=2, c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================101
    >>> x = np.linspace(0, 10, 100)
    >>> y = TidyDistribution(x, whichdist="uniform")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="uniform", loc=3, scale=2)
    >>> print(y)
    ===============================================================================102
    >>> x = np.linspace(0, 10, 100)
    >>> y = TidyDistribution(x, whichdist="wald")
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="wald", loc=3, scale=2)
    >>> print(y)
    ===============================================================================103
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="WeibullMax", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="WeibullMax", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================104
    >>> x = np.linspace(0, 1, 100)
    >>> y = TidyDistribution(x, whichdist="WeibullMin", c=2)
    >>> print(y)
    >>> y = TidyDistribution(x, whichdist="WeibullMin", c=2, loc=3, scale=2)
    >>> print(y)
    ===============================================================================105
    >>> x = np.array([[0.2,0.1], [-0.2,0.1]])
    >>> y = TidyDistribution(x, whichdist="MultiNorm", mean=np.zeros(2), cov=np.identity(2))
    >>> print(y)
    ===============================================================================106
    >>> x = np.array([[0.2,0.1], [-0.2,0.1]])
    >>> y = TidyDistribution(x, whichdist="MultiT", loc=np.zeros(2), shape=np.identity(2), df=2)
    >>> print(y)
    ===============================================================================107
    """
    res = None
    if whichdist == "bernoulli":
        res = sts.bernoulli.cdf(x, **kwargs)
    elif whichdist == "betabinom":
        res = sts.betabinom.cdf(x, **kwargs)
    elif whichdist == "binom":
        res = sts.binom.cdf(x, **kwargs)
    elif whichdist == "boltzmann":
        res = sts.boltzmann.cdf(x, **kwargs)
    elif whichdist == "planck":
        res = sts.planck.cdf(x, **kwargs)
    elif whichdist == "poiss":
        res = sts.poisson.cdf(x, **kwargs)
    elif whichdist == "geom":
        res = sts.geom.cdf(x, **kwargs)
    elif whichdist == "nbinom":
        res = sts.nbinom.cdf(x, **kwargs)
    elif whichdist == "hgeom":
        res = sts.hypergeom.cdf(x, **kwargs)
    elif whichdist == "nchgeomfisher":
        res = sts.nchypergeom_fisher.cdf(x, **kwargs)
    elif whichdist == "nchgeomWallenius":
        res = sts.nchypergeom_wallenius.cdf(x, **kwargs)
    elif whichdist == "nhgeom":
        res = sts.nhypergeom.cdf(x, **kwargs)
    elif whichdist == "zeta":
        res = sts.zipf.cdf(x, **kwargs)
    elif whichdist == "zipfian":
        res = sts.zipfian.cdf(x, **kwargs)
    elif whichdist == "logseries":
        res = sts.logser.cdf(x, **kwargs)
    elif whichdist == "duniform":
        res = sts.randint.cdf(x, **kwargs)
    elif whichdist == "dlaplace":
        res = sts.dlaplace.cdf(x, **kwargs)
    elif whichdist == "yulesimon":
        res = sts.yulesimon.cdf(x, **kwargs)
    elif whichdist == "alpha":
        res = sts.alpha.cdf(x, **kwargs)
    elif whichdist == "anglit":
        res = sts.anglit.cdf(x, **kwargs)
    elif whichdist == "arcsin":
        res = sts.arcsine.cdf(x, **kwargs)
    elif whichdist == "beta":
        res = sts.beta.cdf(x, **kwargs)
    elif whichdist == "betaprime":
        res = sts.betaprime.cdf(x, **kwargs)
    elif whichdist == "bradford":
        res = sts.bradford.cdf(x, **kwargs)
    elif whichdist == "burr":
        res = sts.burr.cdf(x, **kwargs)
    elif whichdist == "burr12":
        res = sts.burr12.cdf(x, **kwargs)
    elif whichdist == "cauchy":
        res = sts.cauchy.cdf(x, **kwargs)
    elif whichdist == "skewcauchy":
        res = sts.skewcauchy.cdf(x, **kwargs)
    elif whichdist == "chi":
        res = sts.chi.cdf(x, **kwargs)
    elif whichdist == "chi2":
        res = sts.chi2.cdf(x, **kwargs)
    elif whichdist == "cosine":
        res = sts.cosine.cdf(x, **kwargs)
    elif whichdist == "dgamma":
        res = sts.dgamma.cdf(x, **kwargs)
    elif whichdist == "dweibull":
        res = sts.dweibull.cdf(x, **kwargs)
    elif whichdist == "exp":
        res = sts.expon.cdf(x, **kwargs)
    elif whichdist == "expweibull":
        res = sts.exponweib.cdf(x, **kwargs)
    elif whichdist == "exppower":
        res = sts.exponpow.cdf(x, **kwargs)
    elif whichdist == "fatigurlife":
        res = sts.fatiguelife.cdf(x, **kwargs)
    elif whichdist == "loglogistic":
        res = sts.fisk.cdf(x, **kwargs)
    elif whichdist == "foldcauchy":
        res = sts.foldcauchy.cdf(x, **kwargs)
    elif whichdist == "foldnormal":
        res = sts.foldnorm.cdf(x, **kwargs)
    elif whichdist == "f":
        res = sts.f.cdf(x, **kwargs)
    elif whichdist == "gamma":
        res = sts.gamma.cdf(x, **kwargs)
    elif whichdist == "glogistic":
        res = sts.genlogistic.cdf(x, **kwargs)
    elif whichdist == "gpareto":
        res = sts.genpareto.cdf(x, **kwargs)
    elif whichdist == "gexp":
        res = sts.genexpon.cdf(x, **kwargs)
    elif whichdist == "gextremevalue":
        res = sts.genextreme.cdf(x, **kwargs)
    elif whichdist == "ggamma":
        res = sts.gengamma.cdf(x, **kwargs)
    elif whichdist == "ghalflogistic":
        res = sts.genhalflogistic.cdf(x, **kwargs)
    elif whichdist == "gigauss":
        res = sts.geninvgauss.cdf(x, **kwargs)
    elif whichdist == "gnorm":
        res = sts.gennorm.cdf(x, **kwargs)
    elif whichdist == "gibrat":
        res = sts.gibrat.cdf(x, **kwargs)
    elif whichdist == "gompertz":
        res = sts.gompertz.cdf(x, **kwargs)
    elif whichdist == "halfcauchy":
        res = sts.halfcauchy.cdf(x, **kwargs)
    elif whichdist == "halfnorm":
        res = sts.halfnorm.cdf(x, **kwargs)
    elif whichdist == "halflogistic":
        res = sts.halflogistic.cdf(x, **kwargs)
    elif whichdist == "hypsecant":
        res = sts.hypsecant.cdf(x, **kwargs)
    elif whichdist == "gausshgeom":
        res = sts.gausshyper.cdf(x, **kwargs)
    elif whichdist == "invgamma":
        res = sts.invgamma.cdf(x, **kwargs)
    elif whichdist == "invgauss":
        res = sts.invgauss.cdf(x, **kwargs)
    elif whichdist == "invweibull":
        res = sts.invweibull.cdf(x, **kwargs)
    elif whichdist == "JohnsonSB":
        res = sts.johnsonsb.cdf(x, **kwargs)
    elif whichdist == "JohnsonSU":
        res = sts.johnsonsu.cdf(x, **kwargs)
    elif whichdist == "KSone":
        res = sts.ksone.cdf(x, **kwargs)
    elif whichdist == "KStwo":
        res = sts.kstwo.cdf(x, **kwargs)
    elif whichdist == "KStwobign":
        res = sts.kstwobign.cdf(x, **kwargs)
    elif whichdist == "laplace":
        res = sts.laplace.cdf(x, **kwargs)
    elif whichdist == "AsymmetricLaplace":
        res = sts.laplace_asymmetric.cdf(x, **kwargs)
    elif whichdist == "Left-skewed-Levy":
        res = sts.levy_l.cdf(x, **kwargs)
    elif whichdist == "levy":
        res = sts.levy.cdf(x, **kwargs)
    elif whichdist == "logistic":
        res = sts.logistic.cdf(x, **kwargs)
    elif whichdist == "loglaplace":
        res = sts.loglaplace.cdf(x, **kwargs)
    elif whichdist == "loggamma":
        res = sts.loggamma.cdf(x, **kwargs)
    elif whichdist == "lognorm":
        res = sts.lognorm.cdf(x, **kwargs)
    elif whichdist == "loguniform":
        res = sts.loguniform.cdf(x, **kwargs)
    elif whichdist == "maxwell":
        res = sts.maxwell.cdf(x, **kwargs)
    elif whichdist == "Mielke-Beta-Kappa":
        res = sts.mielke.cdf(x, **kwargs)
    elif whichdist == "Nakagami":
        res = sts.nakagami.cdf(x, **kwargs)
    elif whichdist == "ncchi2":
        res = sts.ncx2.cdf(x, **kwargs)
    elif whichdist == "ncf":
        res = sts.ncf.cdf(x, **kwargs)
    elif whichdist == "nct":
        res = sts.nct.cdf(x, **kwargs)
    elif whichdist == "norm":
        res = sts.norm.cdf(x, **kwargs)
    elif whichdist == "NormalInverseGaussian":
        res = sts.norminvgauss.cdf(x, **kwargs)
    elif whichdist == "pareto":
        res = sts.pareto.cdf(x, **kwargs)
    elif whichdist == "lomax":
        res = sts.lomax.cdf(x, **kwargs)
    elif whichdist == "PowerlogNorm":
        res = sts.powerlognorm.cdf(x, **kwargs)
    elif whichdist == "PowerNormal":
        res = sts.powernorm.cdf(x, **kwargs)
    elif whichdist == "PowerLaw":
        res = sts.powerlaw.cdf(x, **kwargs)
    elif whichdist == "Rdistribution":
        res = sts.rdist.cdf(x, **kwargs)
    elif whichdist == "rayleigh":
        res = sts.rayleigh.cdf(x, **kwargs)
    elif whichdist == "rice":
        res = sts.rice.cdf(x, **kwargs)
    elif whichdist == "semicircular":
        res = sts.semicircular.cdf(x, **kwargs)
    elif whichdist == "Studentized-Range":
        res = sts.studentized_range.cdf(x, **kwargs)
    elif whichdist == "t":
        res = sts.t.cdf(x, **kwargs)
    elif whichdist == "Trapezoidal":
        res = sts.trapezoid.cdf(x, **kwargs)
    elif whichdist == "Triangular":
        res = sts.triang.cdf(x, **kwargs)
    elif whichdist == "TruncatedExpon":
        res = sts.truncexpon.cdf(x, **kwargs)
    elif whichdist == "TruncatedNormal":
        res = sts.truncnorm.cdf(x, **kwargs)
    elif whichdist == "TruncatedPareto":
        res = sts.truncpareto.cdf(x, **kwargs)
    elif whichdist == "TruncatedWeibullMin":
        res = sts.truncweibull_min.cdf(x, **kwargs)
    elif whichdist == "uniform":
        res = sts.uniform.cdf(x, **kwargs)
    elif whichdist == "wald":
        res = sts.wald.cdf(x, **kwargs)
    elif whichdist == "WeibullMax":
        res = sts.weibull_max.cdf(x, **kwargs)
    elif whichdist == "WeibullMin":
        res = sts.weibull_min.cdf(x, **kwargs)
    elif whichdist == "MultiNorm":
        res = sts.multivariate_normal.cdf(x, **kwargs)
    elif whichdist == "MultiT":
        res = sts.multivariate_t.cdf(x, **kwargs)
    else:
        pass
    return res
