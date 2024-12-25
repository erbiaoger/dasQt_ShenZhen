
import sys
sys.path.insert(0, '../')
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import threading
import matplotlib
matplotlib.use('Agg')  # 使用非 GUI 后端

from dasQt.das import DAS


# 定义处理单个文件的函数
def process_file(file, save_path):

    das = DAS()
    das.readData(file)

    das.clearFilter()
    das.cutData(xmin=100, xmax=400)
    das.bandpass(freqmin=0.3, freqmax=2.0, corners=8)

    # das.fk_filter(fmin=0.3, fmax=2.0, kmin=-0.1, kmax=0, vmin=5.0, vmax=20.0)
    das.median_filter(nt=10, nx=5, threshold=1.2)
    das.fk_filter(fmin=0.3, fmax=3.0, kmin=-1./10, kmax=0, vmin=5.0, vmax=20.0)

    scale = 0.002
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis("off")
    ax.imshow(das.data, cmap='RdBu', aspect='auto', 
              vmin=-scale, vmax=scale, interpolation='bilinear')
    ax.margins(0)
    fig.savefig(f'{save_path/file.stem}.png', bbox_inches='tight', pad_inches=0, dpi=1000)
    plt.close()


def main():
    files = sorted(pathlib.Path('/Volumes/SanDisk4T/ShenZhen-2024-10-14/20241014_gau2m/2024-10-14').glob('*.dat'))
    print(len(files), 'files')

    save_path = pathlib.Path('/Users/zhangzhiyu/MyProjects/dasQt-other/ShenZhen/label')
    save_path.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=4) as executor:
        for file in files:
            executor.submit(process_file, file, save_path)
            #break


if __name__ == '__main__':
    print('start')
    main()
