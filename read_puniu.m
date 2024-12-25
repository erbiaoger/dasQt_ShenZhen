% clear
% clc
% close all
fid = fopen('/Volumes/CSIM_LAB/DATA/DAS/ShenZhen-2024-10-14/PuNiu/fzy02m_20241017-124430.024808665_271-4410_binhaidadao.dat','r');
info = fread(fid, [10,1], 'double');
N_CHANNEL = info(1,1);
N_SAMPLE_TIME = info(3,1);
formatSpec = '%.9f';
ns = num2str(info(7:10,1),formatSpec);
if info(5,1) == 0
    show_info = ['本条数据为原始信号, 空间采样通道数:',num2str(info(1,1)),'个通道, 空间采样间隔:',num2str(info(2,1)),'m, 每通道数据总长:',num2str(info(3,1)),'点, 每通道采样率:',num2str(1/info(4,1)),'Hz. 数据起始时间为, UTC时间:',datestr(info(6,1)/86400 + datenum(1970,1,1)),ns(2:end)];
    disp(show_info);
elseif info(5,1) == 1
    show_info = ['本条数据为波分信号, 空间采样通道数:',num2str(info(1,1)),'个通道, 空间采样间隔:',num2str(info(2,1)),'m, 每通道数据总长:',num2str(info(3,1)),'点, 每通道采样率:',num2str(1/info(4,1)),'Hz. 数据起始时间为, UTC时间:',datestr(info(6,1)/86400 + datenum(1970,1,1)),ns(2:end)];
    disp(show_info);
end

if info(9,1)>0
    fseek(fid, info(9,1), 'bof');
    extend_field_txt = fgets(fid);
    extend_field = jsondecode(extend_field_txt);
    disp(extend_field) % 显示采集的扩展信息，如空间分辨率等
end

fseek(fid, 80, 'bof');
Input = fread(fid, [1, N_SAMPLE_TIME*N_CHANNEL], 'float');
fclose(fid);
% Input = Input./(2^29);
Input = reshape(Input, N_CHANNEL, N_SAMPLE_TIME);
Input = Input'; % 矩阵的信号转置后行号为时间序列，列号为通道号
% mesh(Input)
% aaa = cumsum(Input); %对每一列通道做cumsun后得到该通道的原始信号
figure
clims = [-0.4, 0.4];
imagesc(Input,clims)