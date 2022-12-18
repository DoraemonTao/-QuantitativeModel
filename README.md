# QuantitativeModel

# Get Started

## 介绍
低功耗项目的量化模型，用于衡量参数指标等信息

## 软件架构
基于python编写，需要安装相关python库.

## Environment Installation
```bash
pip install -r requirements.txt
```

## 刷机准备
1. pixel 4
2. 刷机镜像

## 数据集准备
1. 手机刷入镜像后才能收集所需数据，否则会报错
2.
```bash
adb shell dump sys alarm > alarm.txt
adb shell dump sys jobscheduler > job.txt
adb shell dump sys batterystats --checkin > batterystats.csv
```
3. 将alarm.txt 和 job.txt 内容复制到 data/result.log中。将batterystats.csv文件放入data/中。数据集准备完成。

## 运行
```bash
python main.py
```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
