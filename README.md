# FastDiagP: An Algorithm for Parallelized Direct Diagnosis

**FastDiagP**[1] is a parallelized version of the **FastDiag**[2] algorithm to diagnose over-constrained problems.
The algorithm extends **FastDiag** by integrating a parallelization mechanism that anticipates and pre-calculates consistency checks requested by **FastDiag**.
This mechanism helps to provide consistency checks with fast answers and boosts the algorithm's runtime performance.

This repository shows the implementation and the evaluation of the **FastDiagP** algorithm,
presented at the AAAI 2023 in the paper entitled
*FastDiagP: An Algorithm for Parallelized Direct Diagnosis*.
The research community can fully exploit this repository to reproduce the work described in our paper.

## Table of Contents

- [Repository structure](#repository-structure)
- [Dataset](#dataset)
- [Evaluation results published in the paper](#evaluation-results-published-in-the-paper)
- [How to reproduce the experiments](#how-to-reproduce-the-experiments)

## Repository structure

| *folder*                  | *description*                                                                                                                   |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| ./results                 | evaluation results published in the paper                                                                                       |
| ./data/linux              | stores the *Linux-2.6.33.3* feature model (CNF file), and 50 test scenarios (user requirements with different cardinalities)    |
| ./data/linux-2.6.33.3.xml | the *Linux-2.6.33.3* feature model (XML file) taken form [Diverso Lab's benchmark](https://github.com/diverso-lab/benchmarking) |
| ./solver_apps             | stores the **Sat4j** app                                                                                                        |
| requirements.txt          | lists all required Python packages                                                                                              |
| install.sh                | please execute this file before running evaluations                                                                             |
| utils.py                  | contains some utility functions                                                                                                 |
| checker.py                | contains the function checking the consistency of a given CNF formula                                                           |
| evaluate_v1.py            | evaluations for Table 3                                                                                                         |
| evaluate_v2.py            | evaluations for Table 4                                                                                                         |
| fastdiag.py               | implementation of the FastDiag algorithm                                                                                        |
| fastdiagp_v2_1.py         | implementation of the FastDiagP algorithm, in which the `maxNumGenCC = numCores - 1`.                                           |
| fastdiagp_v2_2.py         | implementation of the FastDiagP algorithm, in which the `maxNumGenCC = 7`.                                                      |
| README.md                 | this file                                                                                                                       |

## Dataset

The basis for the **FastDiagP** evaluation was the *Linux-2.6.33.3* feature model taken from [Diverso Lab's benchmark](https://github.com/diverso-lab/benchmarking)[3].
The following Table shows the characteristics of the *Linux-2.6.33.3* feature model.

| *characteristic* | *value* |
|--------------|---------|
| #features    | 6,467   |
| #relationships | 6,322   |
| #mandatory | 244   |
| #optional | 6,037   |
| #alternative | 39   |
| #or  | 2   |
| #cross-tree constraints | 7,650   |
| #requires | 7,108   |
| #excludes | 205   |
| #3CNF  | 337   |

The dataset generation process consists of the following steps:

1. _Generates inconsistent user requirements_: We randomly synthesized and collected 20,976 inconsistent sets of requirements, whose cardinality is between 5 and 250.
We run the **FastDiag** algorithm for each inconsistent set of requirements to identify its preferred diagnosis.
Besides, we collected information on the diagnosis process, including the runtime, the number of performed consistency checks, and the cardinality of the diagnosis.
The following Figure shows the histogram of identified diagnoses' cardinality from synthesized 20,976 sets of requirements.

![image2.png](..%2F..%2F..%2FDownloads%2Fimage2.png)
    
2. _Classifies inconsistent user requirements_: We classified the collected inconsistent sets of requirements according to the cardinality of their diagnosis.
    
3. _Selects inconsistent user requirements_: For groups with diagnosis cardinalities of 1, 2, 4, 8, and 16, 
we sorted the inconsistent sets of requirements according to the number of performed consistency checks and the runtime of the diagnosis.
Finally, we applied the systematic sampling technique [4] to select 10 inconsistent user requirements for each group.
The systematic sampling technique helps to choose the most representative inconsistent user requirements for each group.

> To ensure the reproducibility of the results, we have used the seed value of 141982L for the random number generator.

## Evaluation results published in the paper

There are seven files in the _./results_ folder:
1. _resultFastDiag.csv_: contains the results for the **FastDiag** algorithm.
2. Three files *resultFastDiagPV2_1_#.csv*: contains the results for the **FastDiagP** algorithm, in which the `maxNumGenCC = numCores - 1`. 
These results are summarized in Table 3. 
3. Three files *resultFastDiagPV2_2_7_#.csv*: contains the results for the **FastDiagP** algorithm, in which the `maxNumGenCC = 7`.
These results are summarized in Table 4.

> Note: `maxNumGenCC` is `maxGCC` in the paper.

## How to reproduce the experiments

The diagnosis algorithms were implemented in _Python_ using the following libraries:

- **Sat4j**[5] - A Java library for solving boolean satisfaction and optimization problems.
    
- **PySAT**[6] - we used the CNF class to represent constraints
    
- Python multiprocessing package for running parallel tasks.


Due to these libraries, you need to install dependencies before executing the evaluations.
_install.sh_ provides a bash script to install these dependencies.
The following Listing shows how to execute the _install.sh_.

```bash
chmod u+x install.sh
./install.sh
```

The paper shows evaluation results in two Tables 3 and 4.

To reproduce Table 3's results, please use the following command:

```bash
python3 evaluate_v1.py
```

To reproduce Table 4's results, please use the following command:

```bash
python3 evaluate_v2.py
```

In the _evaluate_v1.py_, for each test scenario, the program will execute the **FastDiag** algorithm first using
_fastdiag.py_, and then the **FastDiagP** algorithm using _fastdiagp_v2_1.py_. Meanwhile, _evaluate_v2.py_ will execute 
the **FastDiagP** algorithm using _fastdiagp_v2_2.py_.

The _fastdiag.py_, _fastdiagp_v2_1.py_, and _fastdiagp_v2_2.py_ allow the following parameters:

- *in_model_filename*: A CNF file depicting the constraints representing the background knowledge for the algorithm (e.g., the constraints in a feature model)
- *in_req_filename*: A CNF file representing the product selection or user requirements for diagnosis.
- *solver_path*: The path to the solver used for the diagnosis. We only support **Sat4j** at this time
- *numCores*: The number of CPU cores to use for the diagnosis.

## References

[1] V.M. Le, C.V. Silva, A. Felfernig, T.N.T. Trang, J. Galindo, D. Benavides. FastDiagP: An Algorithm for Parallelized Direct Diagnosis. In 37th AAAI Conference on Artificial Intelligence. AAAI’23, Washington, DC, USA. 2023. (to appear

[2] A. Felfernig, M. Schubert and C. Zehentner, 2012. An efficient diagnosis algorithm for inconsistent constraint sets. AI EDAM, 26(1), pp.53-62. [doi:10.1017/S0890060411000011](https://doi.org/10.1017/S0890060411000011)

[3] Heradio, R., Fernandez-Amoros, D., Galindo, J.A., et al. Uniform and scalable sampling of highly configurable systems. Empir Software Eng 27, 44 (2022). [https://doi.org/10.1007/s10664-021-10102-5](https://doi.org/10.1007/s10664-021-10102-5)

[4] Mostafa, S. A.; and Ahmad, I. A. 2018. Recent developments in systematic sampling: A review. Journal of Statistical Theory and Practice, 12(2): 290–310. [https://doi.org/10.1080/15598608.2017.1353456](https://doi.org/10.1080/15598608.2017.1353456)

[5] Le Berre, D.; and Parrain, A. 2010. The Sat4j library, release 2.2. Journal on Satisfiability, Boolean Modeling and Computation, 7(2-3): 59–64. [10.3233/SAT190075](https://content.iospress.com/articles/journal-on-satisfiability-boolean-modeling-and-computation/sat190075)

[6] Ignatiev, A.; Morgado, A.; and Marques-Silva, J. 2018. PySAT: A Python Toolkit for Prototyping with SAT Oracles. In SAT, 428–437. [10.1007/978-3-319-94144-8_26](https://doi.org/10.1007/978-3-319-94144-8_26)

