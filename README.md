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

Acknowledgment
-------
The BIF parser is provided by [Antoine Bosselut](antoine.bosselut@uw.edu).
The codes in the project is for the assignment 3 in [CSE 515 - Statistical Methods in Computer Science](http://courses.cs.washington.edu/courses/cse515/15wi/), University of Washington.