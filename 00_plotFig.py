
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
from pathlib import Path

from dasQt import das

# 定义处理单个文件的函数
def process_file(file, save_path):
    das1 = das.DAS()
    das1.readData(file)
    # das1.RawDataBpFilter(0.01, 0.02, 2.0, 2.1)
    data = das1.data[:, 100:400]

    scale = 0.007
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis("off")
    ax.imshow(data, cmap='RdBu', aspect='auto', 
              vmin=-scale, vmax=scale, interpolation='bilinear')
    ax.margins(0)
    fig.savefig(f'{save_path/file.stem}.png', bbox_inches='tight', pad_inches=0, dpi=300)
    plt.close()


def main():
    # dir_path = pathlib.Path('/Volumes/CSIM_LAB/DATA/DAS/govlink/吉大20230720/2023-07-24')
    # dir_path = pathlib.Path('/Volumes/CSIM_LAB/DATA/Car-JLU-2024-01-31/ovlink/2024-02-01')
    # dir_path = pathlib.Path('/Volumes/CSIM_LAB/DATA/Car-JLU-2024-01-31/ovlink/2024-02-01')
    # dir_path = Path('/Volumes/SanDisk4T/ShenZhen-2024-10-14/20241014_gau2m/2024-10-14')
    dir_path = Path('/Volumes/SanDisk4T/ShenZhen-2024-10-14/20241015_gau2m/2024-10-15')
    files = sorted(dir_path.glob('*.dat'))
    print(len(files), 'files')

    save_path = pathlib.Path('/Users/zhangzhiyu/MyProjects/dasQt-other/ShenZhen/testA')
    save_path.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=4) as executor:
        for file in files:
            executor.submit(process_file, file, save_path)
            #break


if __name__ == '__main__':
    print('start')
    main()
