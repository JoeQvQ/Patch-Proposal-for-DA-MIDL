# Patch-Proposal-for-DA-MIDL

> Unofficial Implemention for DA-MIDL's Patch Proposal
> 
> 此项目为Patch提议文件(DA-MIDL)的非官方复现版本，如有问题欢迎指正交流！(Email：3229075390@qq.com)
> 
> 官方代码：https://github.com/WyZhuNUAA/DA-MIDL
>
> 论文：Dual attention multi-instance deep learning for Alzheimer’s disease diagnosis with structural MRI

## 运行步骤
1.运行官方代码datasplit.py获得data.mat文件

2.运行项目代码patch_gen_fixstep.py获得patch_loc_fold_0.csv~fold4.csv文件对应5个fold

3.用Excel或者Calc等软件打开patch_loc_fold_0.csv~fold4.csv文件，按照p值升序进行排序

4.运行项目代码patch_proposal_save.py为每个fold生成template_center_fold{}_size{}.mat

