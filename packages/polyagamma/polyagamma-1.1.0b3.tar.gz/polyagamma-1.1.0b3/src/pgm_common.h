#ifndef PGM_COMMON_H
#define PGM_COMMON_H
#include <numpy/random/distributions.h>
#include "pgm_igammaq.h"

#define PGM_PI2 9.869604401089358  // pi^2
#define PGM_PI2_8 1.233700550136169  // pi^2 / 8
#define PGM_LOGPI_2 0.4515827052894548  // log(pi / 2)
#define PGM_LS2PI 0.9189385332046727  // log(sqrt(2 * pi))

/*
 * Calculate the cumulative distribution function of an Inverse-Gaussian.
 */
NPY_INLINE double
inverse_gaussian_cdf(double x, double mu, double lambda)
{
    double a = sqrt(0.5 * lambda / x);
    double b = a * (x / mu);
    double c = exp(lambda / mu);

    return 0.5 * (kf_erfc(a - b) + c * kf_erfc(b + a) * c);
}

/*
 * Calculate logarithm of the gamma function of z.
 *
 * This implementation is based on an asymptotic expansion based on stirling's
 * approximation.
 *
 * - values less than 1 we use lgamma from <math.h> since it is more accurate.
 * - For interger values corresponding to logfactorial, we use a lookup table.
 */
NPY_INLINE double
pgm_lgamma(double z)
{
    /* lookup table for integer values of log-gamma function where x >= 3
     * courtesy of NumPy devs. */
    static const double logfactorial[126] = {
        0.000000000000000, 0.0000000000000000, 0.69314718055994529,
        1.791759469228055, 3.1780538303479458, 4.7874917427820458,
        6.5792512120101012, 8.5251613610654147, 10.604602902745251,
        12.801827480081469, 15.104412573075516, 17.502307845873887,
        19.987214495661885, 22.552163853123425, 25.19122118273868,
        27.89927138384089, 30.671860106080672, 33.505073450136891,
        36.395445208033053, 39.339884187199495, 42.335616460753485,
        45.380138898476908, 48.471181351835227, 51.606675567764377,
        54.784729398112319, 58.003605222980518, 61.261701761002001,
        64.557538627006338, 67.88974313718154, 71.257038967168015,
        74.658236348830158, 78.092223553315307, 81.557959456115043,
        85.054467017581516, 88.580827542197682, 92.136175603687093,
        95.719694542143202, 99.330612454787428, 102.96819861451381,
        106.63176026064346, 110.32063971475739, 114.03421178146171,
        117.77188139974507, 121.53308151543864, 125.3172711493569,
        129.12393363912722, 132.95257503561632, 136.80272263732635,
        140.67392364823425, 144.5657439463449, 148.47776695177302,
        152.40959258449735, 156.3608363030788, 160.3311282166309,
        164.32011226319517, 168.32744544842765, 172.35279713916279,
        176.39584840699735, 180.45629141754378, 184.53382886144948,
        188.6281734236716, 192.7390472878449, 196.86618167289001,
        201.00931639928152, 205.1681994826412, 209.34258675253685,
        213.53224149456327, 217.73693411395422, 221.95644181913033,
        226.1905483237276, 230.43904356577696, 234.70172344281826,
        238.97838956183432, 243.26884900298271, 247.57291409618688,
        251.89040220972319, 256.22113555000954, 260.56494097186322,
        264.92164979855278, 269.29109765101981, 273.67312428569369,
        278.06757344036612, 282.4742926876304, 286.89313329542699,
        291.32395009427029, 295.76660135076065, 300.22094864701415,
        304.68685676566872, 309.1641935801469, 313.65282994987905,
        318.1526396202093, 322.66349912672615, 327.1852877037752,
        331.71788719692847, 336.26118197919845, 340.81505887079902,
        345.37940706226686, 349.95411804077025, 354.53908551944079,
        359.1342053695754, 363.73937555556347, 368.35449607240474,
        372.97946888568902, 377.61419787391867, 382.25858877306001,
        386.91254912321756, 391.57598821732961, 396.24881705179155,
        400.93094827891576, 405.6222961611449, 410.32277652693733,
        415.03230672824964, 419.75080559954472, 424.47819341825709,
        429.21439186665157, 433.95932399501481, 438.71291418612117,
        443.47508812091894, 448.24577274538461, 453.02489623849613,
        457.81238798127816, 462.60817852687489, 467.4121995716082,
        472.22438392698058, 477.04466549258564, 481.87297922988796
    };
    // Coefficients from Pugh (2004)
    static const double d[11] = {
        2.48574089138753565546E-5, 1.05142378581721974210E+0,
        -3.45687097222016235469E+0, 4.51227709466894823700E+0,
        -2.98285225323576655721E+0, 1.05639711577126713077E+0,
        -1.95428773191645869583E-1, 1.70970543404441224307E-2,
        -5.71926117404305781283E-4, 4.63399473359905636708E-6,
        -2.71994908488607703910E-9
    };
    static const double a1 = 0.08333333333333333;  // 1 / 12
    static const double a2 = 0.002777777777777778;  // 1/360
    static const double a3 = 0.0007936507936507937;  // 1/1260
    static const double log2sepi = 0.6207822376352452;  // log(2 * sqrt(e/pi))

    double out, z2, sum, a, b;
    size_t zz, k;

    if (z < 1) {
        // use Pugh(2004)'s algorithm for small z.
         a = z - 1;
         for (k = 1, sum = d[0] + d[0] / a; k < 11; k++) {
             sum += d[k] / (a + k);
         }
         b = z - 0.5;
         return log(sum) + log2sepi - b + b * log(b + 10.900511);
    }

    zz = (size_t)z;
    if (z < 127 && z == zz) 
        return logfactorial[zz - 1];

    z2 = z * z;
    out = (z - 0.5) * log(z) - z + PGM_LS2PI;
    out += a1 / z - a2 / (z2 * z) + a3 / (z2 * z2 * z);
    return out;
}

/*
 * sample from X ~ Gamma(a, rate=b) truncated on the interval {x | x > t}.
 *
 * For a > 1 we use the algorithm described in Dagpunar (1978)
 * For a == 1, we truncate an Exponential of rate=b.
 * For a < 1, we use algorithm [A4] described in Philippe (1997)
 *
 * TODO: There is a more efficient algorithm for a > 1 in Philippe (1997), which
 * should replace this one in the future.
 */
NPY_INLINE double
random_left_bounded_gamma(bitgen_t* bitgen_state, double a, double b, double t)
{
    double x, log_rho, log_m, a_minus_1, b_minus_a, c0, one_minus_c0;

    if (a > 1) {
        b = t * b;
        a_minus_1 = a - 1;
        b_minus_a = b - a;
        c0 = 0.5 * (b_minus_a + sqrt(b_minus_a * b_minus_a + 4 * b)) / b;
        one_minus_c0 = 1 - c0;

        do {
            x = b + random_standard_exponential(bitgen_state) / c0;
            log_rho = a_minus_1 * log(x) - x * one_minus_c0;
            log_m = a_minus_1 * log(a_minus_1 / one_minus_c0) - a_minus_1;
        } while (log(1 - random_standard_uniform(bitgen_state)) > (log_rho - log_m));
        return t * (x / b);
    }
    else if (a == 1) {
        return t + random_standard_exponential(bitgen_state) / b;
    }
    else {
        do {
            x = 1 + random_standard_exponential(bitgen_state) / (t * b);
        } while (log(1 - random_standard_uniform(bitgen_state)) > (a - 1) * log(x));
        return t * x;
    }
}

/*
 * Sample from an Inverse-Gaussian(mu, lambda) truncated on the set {x | x < t}.
 *
 * We sample using two algorithms depending on whether mu > t or mu < t.
 *
 * When mu < t, We use a known sampling algorithm from Devroye
 * (1986), page 149. We sample until the generated variate is less than t.
 *
 * When mu > t, we use a Scaled-Inverse-Chi-square distribution as a proposal,
 * as explained in [1], page 134. To generate a sample from this proposal, we
 * sample from the tail of a standard normal distribution such that the value
 * is greater than 1/sqrt(t). Once we obtain the sample, we square and invert
 * it to obtain a sample from a Scaled-Inverse-Chi-Square(df=1, scale=lambda)
 * that is less than t. An efficient algorithm to sample from the tail of a
 * normal distribution using a pair of exponential variates is shown in
 * Devroye (1986) [page 382] & Devroye (2009) [page 7]. This sample becomes our
 * proposal. We accept the sample only if we sample a uniform less than the
 * acceptance porbability. The probability is exp(-0.5 * lambda * x / mu^2).
 * Refer to Appendix S1 of Polson et al. (2013).
 *
 * References
 * ----------
 *  [1] Windle, J. (2013). Forecasting high-dimensional, time-varying
 *      variance-covariance matrices with high-frequency data and sampling
 *      Pólya-Gamma random variates for posterior distributions derived from
 *      logistic likelihoods.(PhD thesis). Retrieved from
 *      http://hdl.handle.net/2152/21842
 */
NPY_INLINE double
random_right_bounded_inverse_gaussian(bitgen_t* bitgen_state, double mu,
                                      double lambda, double t)
{
    double x;

    if (t < mu) {
        double e1, e2;
        const double a = 1. / (mu * mu);
        const double half_lambda = -0.5 * lambda;
        do {
            do {
                e1 = random_standard_exponential(bitgen_state);
                e2 = random_standard_exponential(bitgen_state);
            } while ((e1 * e1) > (2 * e2 / t));
            x = (1 + t * e1);
            x = t / (x * x);
        } while (a > 0 && log(1 - random_standard_uniform(bitgen_state)) >= half_lambda * a * x);
        return x;
    }
    do {
        x = random_wald(bitgen_state, mu, lambda);
    } while (x >= t);
    return x;
}

/* compute the upper incomplete gamma function.
 *
 * This function extends `kf_gammaq` by accounting for integer and half-integer
 * arguments of `s` when s < 30.
 *
 * TODO: Need to get rid of `kf_gammaq` entirely and re-implement upper
 * incomplete gamma using the algorithm in [1]. See GH Issue #36.
 *
 * References
 * ----------
 *  [1] Rémy Abergel and Lionel Moisan. 2020. Algorithm 1006: Fast and Accurate
 *      Evaluation of a Generalized Incomplete Gamma Function. ACM Trans. Math.
 *      Softw. 46, 1, Article 10 (April 2020), 24 pages. DOI:doi.org/10.1145/3365983
 */
NPY_INLINE double
pgm_gammaq(double s, double x)
{
    // 1 / sqrt(pi)
    static const double one_sqrtpi = 0.5641895835477563;
    size_t ss, k;
    double sum, a, sqrt_x;

    ss = (size_t)s;
    if (s == ss && s < 30) {
        for (k = sum = a = 1; k < ss; k++) {
            sum += (a *= x / k);
        }
        return exp(-x) * sum;
    }
    else if (s == (ss + 0.5) && s < 30) {
        sqrt_x = sqrt(x);
        for (k = a = 1, sum = 0; k < ss + 1; k++) {
            sum += (a *= x / (k - 0.5));
        }
        return kf_erfc(sqrt_x) + exp(-x) * one_sqrtpi * sum / sqrt_x;
    }
    return kf_gammaq(s, x);
}

#endif
