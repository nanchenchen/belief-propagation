Belief Propagation on Bayesian Network
=============
This is a program that runs loopy belief propagation on a Bayesian Network (BN),
and generate the marginalized probability for each node on the network.
The details of the algorithm refers to [Kschischang et al. (2001)](http://www.comm.utoronto.ca/~frank/papers/KFL01.pdf),
with the variation of using bethe cluster graph instead a pure factor graph of BN.
The input format should be in [Bayesian Network Interchange Format (BIF)](http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/Old/xmlbif02.html)


Usage
-------
```shell
$ python bp <.bif file path> [-o output file] [-t threshold]
Options:
   -o, --output          output file name, default to 'result.txt'
   -t, --threshold       threshold for convergence default to 1e-10
```