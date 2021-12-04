from PyPDF2 import PdfFileMerger, PdfFileReader
import io
import ltspice
import matplotlib.pyplot as plt
import numpy as np


INPUT_PDF = 'hw_4.pdf'  # название pdf-файла с началом д\з, все рисунки добавляются к нему
INPUT_RAW = {7:'7.raw', 8:'8.raw', 9:'9.raw', 10:'10.raw'}  # список raw-файлов по которым будут строиться графики
MODES = {7:'Согласованная нагрузка', 8:'Холостой ход', 9:'Короткое замыкание', 10:'Активная нагрузка'}  # заголовки графиков
# Измените константы или переименуйте файлы если у вас не так


# get page size
with io.open(INPUT_PDF, mode="rb") as f:
    input_pdf = PdfFileReader(f)
    media_box = input_pdf.getPage(0).mediaBox

min_pt = media_box.lowerLeft
max_pt = media_box.upperRight

pdf_width = float(round((max_pt[0] - min_pt[0]) / 72, 2))
pdf_height = float(round((max_pt[1] - min_pt[1]) / 72, 2))
# letter - 8.5 x 11
# a4 - 8.27 x 11.69


def raw2plot(n: int):
    name = INPUT_RAW[n]
    l = ltspice.Ltspice(name)
    l.parse()
    i_data = []
    v_data = []
    for i in l._variables:
        if i[0] == 'I':
            i_data.append([i, np.abs(l.get_data(i)), np.angle(l.get_data(i), deg=True)])
        elif i[0] == 'V':
            v_data.append([i, np.abs(l.get_data(i)), np.angle(l.get_data(i), deg=True)])
    i_data = i_data[::-1]

    inames, ir, iphi = zip(*i_data)
    vnames, vr, vphi = zip(*v_data)

    fig, (i_plot, v_plot) = plt.subplots(2)

    color = 'tab:red'
    i_plot.set_xlabel('Ток', fontsize=14)
    i_plot.set_ylabel('Амплитуда, А', color=color, fontsize=14)
    i_plot.plot(ir, marker='o', color=color)
    i_plot.tick_params(axis='y', labelcolor=color)

    i_plot_tw = i_plot.twinx()
    color = 'tab:blue'
    i_plot_tw.set_ylabel('Фаза, °', color=color, fontsize=14)
    i_plot_tw.plot(iphi, marker='o', color=color)
    i_plot_tw.tick_params(axis='y', labelcolor=color)

    i_plot.set_xticks(range(len(inames)))
    i_plot.set_xticklabels(inames)


    color = 'tab:red'
    v_plot.set_xlabel('Напряжение', fontsize=14)
    v_plot.set_ylabel('Амплитуда, В', color=color, fontsize=14)
    v_plot.plot(vr, marker='o', color=color)
    v_plot.tick_params(axis='y', labelcolor=color)

    v_plot_tw = v_plot.twinx()
    color = 'tab:blue'
    v_plot_tw.set_ylabel('Фаза, °', color=color, fontsize=14)
    v_plot_tw.plot(vphi, marker='o', color=color)
    v_plot_tw.tick_params(axis='y', labelcolor=color)

    v_plot.set_xticks(range(len(vnames)))
    v_plot.set_xticklabels(vnames)

    fig.suptitle(MODES[n], fontsize=16)
    fig.tight_layout()
    fig.set_size_inches(pdf_width, pdf_height)
    # matplotlib.pyplot.subplots_adjust(left=0.080, right=0.920, top=0.900, bottom=0.100)
    # plt.show()
    plt.savefig(str(n) + '.png')
    plt.savefig(str(n) + '.pdf')


[raw2plot(i) for i in range(7, 11)]

# merge all files in one
merger = PdfFileMerger()
merger.append(INPUT_PDF)
for i in range(7, 11):
    merger.append(str(i) + '.pdf')
merger.write("hw_4_with_plt.pdf")
merger.close()
