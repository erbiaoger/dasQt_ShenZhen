import numpy as np
import json

filename = '/Users/zhangzhiyu/Desktop/fzy_20241017-104730.711509876_271-4410_binhaidadao.dat'

header_arr = np.fromfile(filename, dtype=np.float64, count=10)
n_channels = int(header_arr[0])               # 通道数
fs = int(round(1/header_arr[3]))              # 采样率
print(f'header_arr:{header_arr}, 附加扩展信息: {header_arr[8]>0}')
if header_arr[8]>0:                           # 带扩展信息
    extend_header_seek = int(header_arr[8])   # 扩展字段开始的位置
    secs = (extend_header_seek-80)/4/n_channels/fs  # 总的采样秒数
    with open(filename, 'rb') as f:
        f.seek(extend_header_seek)            # 跳到扩展头
        extend_field = json.load(f)           # 扩展头
        print(extend_field, secs)
    arr = np.fromfile(filename, dtype=np.float32, count=(extend_header_seek-80)//4, offset=80).reshape((-1, n_channels))  # 读取全部
else:                                         # 不带扩展信息
    secs = header_arr[2] * header_arr[3]      # 总的采样秒数
    arr = np.fromfile(filename, dtype=np.float32, count=n_channels*fs, offset=80).reshape((fs, n_channels)) # 读取一秒
    
import matplotlib.pyplot as plt
plt.imshow(arr, aspect='auto', cmap='RdBu')
plt.colorbar()
plt.show()