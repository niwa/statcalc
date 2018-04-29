# Statistical Calculators

Statistics tools, including a kappa calculator and a Lin's concordance calculator.

# Requirements

* Python 3.x
* Python dependencies (see `requirements.txt` for a complete listing)
* Windows, MacOS, Linux or any other *nix OS

This project uses Python 3.x `unittest` module for tests. You may need to install the
requirements first. Also, if you would like to view the test coverage, please
install the `coverage` module.

For running the tests.

```shell
python3 test.py
```

For measuring the coverage and producing an HTML report.

```shell
coverage run tests.py
coverage html
```

## Kappa calculator

Sample usage for `kappa.py`:

```shell
$ python kappa.py --npp 1.0 --npa 1.0 --nap 2.0 --naa 2.0 --kappatest 0.5
Results for 2x2 Interrater table
+-----------+-----------+--------+
| Rater A   | Rater B   | None   |
+===========+===========+========+
|           | present   | absent |
+-----------+-----------+--------+
| present   | 1         | 1      |
+-----------+-----------+--------+
| absent    | 2         | 2      |
+-----------+-----------+--------+
+-------------------------------------------------------------+
| kappahat = 0.0, (kappa+ = 0.0. kappa- = 0.0)                |
+-------------------------------------------------------------+
| s.e.(0) = 0.3849,  s.e.(kappahat) = 0.3849                  |
+-------------------------------------------------------------+
|                                                             |
+-------------------------------------------------------------+
| Hypothesis test p-values                                    |
+-------------------------------------------------------------+
| One-sided test, H0 is kappa =<0                             |
+-------------------------------------------------------------+
| p = Prob[>kappahat, given that kappa=0] = 0.5000            |
+-------------------------------------------------------------+
|                                                             |
+-------------------------------------------------------------+
| One-sided test, H0 is kappa =< 0.5                          |
+-------------------------------------------------------------+
| p = Prob[>kappahat, given that kappa= 0.5] = 0.9030         |
+-------------------------------------------------------------+
|                                                             |
+-------------------------------------------------------------+
| Two-sided test, H0 is kappa= 0.5                            |
+-------------------------------------------------------------+
| p = Prob[>|kappahat-kappa|, given that kappa= 0.5] = 0.1939 |
+-------------------------------------------------------------+
```

Sample usage for `kappa_simple.py`:

```shell
$ python kappa_simple.py --npp 1.0 --npa 1.0 --nap 2.0 --naa 2.0 --kappatest 0.5
Results for 2x2 Interrater table
+-----------+-----------+--------+
| Rater A   | Rater B   | None   |
+===========+===========+========+
|           | present   | absent |
+-----------+-----------+--------+
| present   | 1         | 1      |
+-----------+-----------+--------+
| absent    | 2         | 2      |
+-----------+-----------+--------+
+------------------------------------------------------------------+
| estimated kappa = 0.0                                            |
+------------------------------------------------------------------+
| s.e.(0) = 0.3849,  s.e.(estimated kappa) = 0.3849                |
+------------------------------------------------------------------+
| Hypothesis test p-values                                         |
+------------------------------------------------------------------+
| One-sided test, H0 is kappa <= 0.5                               |
+------------------------------------------------------------------+
| p = Prob[>estimated kappa, given that kappa= 0.90300.5] = 0.9030 |
+------------------------------------------------------------------+
```

Try `python kappa.py -h` for more or `python kappa_simple.py -h`.

## Lin's Concordance calculator

Sample usage for `links_concordance.py`:

```shell
$ python lins_concordance.py "1~2~2~3~3~4"
+----------------------------------------------------------+
| Concordance Results                                      |
+==========================================================+
| Sample concordance correlation coefficient (pc) = 0.5714 |
+----------------------------------------------------------+
| Lower one-sided 95% CL for pc = -0.193                   |
+----------------------------------------------------------+
| Lower two-sided 95% CL for pc = -0.343                   |
+----------------------------------------------------------+
| Upper one-sided 95% CL for pc = 0.9043                   |
+----------------------------------------------------------+
| Upper two-sided 95% CL for pc = 0.9298                   |
+----------------------------------------------------------+
```

Try `python lins_concordance.py -h` for more.
