#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

FIRST_4_BYTES = '8d691c8b'


def drawBoxPlot(data_dict, xlabel, ylabel, output_name, yscale='linear'):
    if len(data_dict.keys()) == 0:
        return

    boxPlotData = []
    for k in sorted(data_dict.keys()):
        boxPlotData.append(data_dict[k])

    print(boxPlotData)

    fig = plt.figure()
    plt.boxplot(x=boxPlotData,
                patch_artist=True,
                boxprops={'color': 'black', 'facecolor': '#ffffff', 'linewidth': 1},
                flierprops={'marker': 'o', 'markerfacecolor': '#ffffff', 'color': 'black', 'linewidth': 1},
                medianprops={'linestyle': '-', 'color': 'black', 'linewidth': 1},
                whiskerprops={'linewidth': 1},
                capprops={'linewidth': 1},
                labels=sorted(data_dict.keys()))

    # plt.ylim(0, 50)
    plt.xlabel(xlabel, fontsize=12, color='black', labelpad=20)
    plt.ylabel(ylabel, fontsize=12, color='black', labelpad=20)
    plt.xticks(fontsize=12, color='black')
    plt.yticks(fontsize=12, color='black')

    plt.yscale(yscale)

    plt.show()
    fig.savefig(output_name, bbox_inches="tight")


if __name__ == "__main__":
    plt.style.use("default")

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', serif='Times New Roman')
    plt.rc('mathtext', fontset='cm')
    plt.rc('figure', figsize=(5, 3))

    workbook = xlrd.open_workbook('input.xlsx')
    sheet = workbook.sheet_by_name(workbook.sheet_names()[0])

    # print(sheet.name, sheet.nrows, sheet.ncols)
    row_filename = sheet.col_values(0)
    row_data_first_4_bytes = sheet.col_values(2)
    row_transaction_execution_times = sheet.col_values(5)
    row_transaction_latency_times = sheet.col_values(8)

    group_verproof_execution_times = dict()
    group_verproof_latency_times = dict()

    for i in range(0, len(row_filename)):
        v = 0
        try:
            # note: filename must be integers
            v = int(row_filename[i])
        except ValueError:
            continue

        # VerProof
        if row_data_first_4_bytes[i] == FIRST_4_BYTES:
            if v in group_verproof_execution_times:
                group_verproof_execution_times[v].append(int(row_transaction_execution_times[i]) / 1000000)
                group_verproof_latency_times[v].append(int(row_transaction_latency_times[i]) / 1000000)
            else:
                group_verproof_execution_times[v] = [int(row_transaction_execution_times[i]) / 1000000]
                group_verproof_latency_times[v] = [(int(row_transaction_latency_times[i]) / 1000000)]

    drawBoxPlot(group_verproof_execution_times,
                'Size of challenge sets',
                r'${\bf VerProof}$ (ms)',
                "graph-1.pdf", yscale="linear")

    drawBoxPlot(group_verproof_latency_times,
                'Size of challenge sets',
                r'${\bf ProofLatency}$ (ms)',
                "graph-2.pdf", yscale="linear")
