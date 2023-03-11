#!/bin/python3
"""
maxNumGenCC = min(numCores - 1, 7)
"""
# import logging.config
import os
import time

# logging.config.fileConfig('logging.conf')

cards = ["16", "8", "4", "2", "1"]
cores = ["8", "16", "32"]
numScenarios = 10

solver_path = "solver_apps/org.sat4j.core.jar"

start_time = time.time()
modelPath = "./data/linux/linux.cnf"
for card in cards:
    for i in range(numScenarios):
        reqPath = "./data/linux/prod_{}_{}.cnf".format(card, i + 1)

        for core in cores:
            print(
                "python3 ./fastdiagp_v2_2.py " + modelPath + " " + reqPath + " " + solver_path + " " + core)
            os.system(
                "python3 ./fastdiagp_v2_2.py " + modelPath + " " + reqPath + " " + solver_path + " " + core + " >>"
                + " resultFastDiagPV2_2_7_0.csv")

total_time = time.time() - start_time
print("Sat4j time: " + str(total_time))
