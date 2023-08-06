<div align="right">
  语言:
    🇨🇳
  <a title="中文" href="./README.zh_CN.md">🇺🇸</a>
  <!-- <a title="俄语" href="../ru/README.md">🇷🇺</a> -->
</div>

 <div align="center"><a title="" href="https://github.com/ZJCV/ZTransforms.git"><img align="center" src="./imgs/ZTransforms.png"></a></div>

<p align="center">
  «ZTransforms»是一个图像数据增强代码库
<br>
<br>
  <a href="https://github.com/RichardLitt/standard-readme"><img src="https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square"></a>
  <a href="https://conventionalcommits.org"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg"></a>
  <a href="http://commitizen.github.io/cz-cli/"><img src="https://img.shields.io/badge/commitizen-friendly-brightgreen.svg"></a>
</p>

基于[pytorch/vision](https://github.com/pytorch/vision/)实现架构，添加[albumentations](https://github.com/albumentations-team/albumentations/tree/f2462be3a4d01c872474d0e7fc0f32f387b06340)后端

* 输入图像格式：`numpy ndarray`
* 数据类型：`uint8`
* 通道排列顺序：`rgb`

关键依赖版本：

* `pytorch/vision:  c1f85d34761d86db21b6b9323102390834267c9b`
* `albumentations-team/albumentations: v0.5.2`

## 内容列表

- [内容列表](#内容列表)
- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [主要维护人员](#主要维护人员)
- [致谢](#致谢)
- [参与贡献方式](#参与贡献方式)
- [许可证](#许可证)

## 背景

[PyTorch](https://github.com/pytorch/pytorch)提供了官方数据增强实现：[transforms](https://github.com/pytorch/vision/tree/master/torchvision/transforms)。该模块基于`PIL`进行数据增强操作，其优缺点如下：

* 优点：
  1.  简洁清晰的数据架构
  2.  简单易懂的数据处理流
  3. 完善的文档介绍
* 缺点：
  1.  基于`PIL`后端，提供的图像增强功能有限
  2.  基于`PIL`后端，相较于其他库的执行速度慢
 
针对于执行速度问题，`torchvision`也意识到了这一点，从`0.8.0`开始进行了改进
  
```
Prior to v0.8.0, transforms in torchvision have traditionally been PIL-centric and presented multiple limitations due to that. Now, since v0.8.0, transforms implementations are Tensor and PIL compatible and we can achieve the following new features:

transform multi-band torch tensor images (with more than 3-4 channels)
torchscript transforms together with your model for deployment
support for GPU acceleration
batched transformation such as for videos
read and decode data directly as torch tensor with torchscript support (for PNG and JPEG image formats)
```

* 一方面通过新的后端[Pillow-SIMD](https://github.com/uploadcare/pillow-simd)来提高`PIL`的执行速度；
* 另一方面添加`PyTorch`后端来实现`GPU`加速

在网上找到两个数据增强库，除了分类数据增强外还提供了检测/分割数据增强：

* [imgaug](https://github.com/aleju/imgaug)：其实现了更多的数据增强操作；
* [albumentations](https://github.com/albumentations-team/albumentations/tree/f2462be3a4d01c872474d0e7fc0f32f387b06340)：其在不同的后端（`pytorch/imgaug/opencv`）中找出各自最快的增强函数（参考[Benchmarking results](https://github.com/albumentations-team/albumentations#benchmarking-results)）

上述两个数据增强库均实现了类似于`transforms`的数据流操作方式。不过相对而言，个人还是最喜欢官方的实现和使用方式，所以新建这个代码库，基于[transforms](https://github.com/pytorch/vision/tree/master/torchvision/transforms)，在原有功能中添加`albumentation`后端实现，同时添加新的数据增强操作（*如果`albumentation`未实现，就使用`imgaug`实现*）


## 安装

```
$ pip install ztransforms
```

## 使用

```
# import torchvision.transforms as transforms
import ztransforms.cls as transforms
...
...
```

## 主要维护人员

* zhujian - *Initial work* - [zjykzj](https://github.com/zjykzj)

## 致谢

* [pytorch/vision](https://github.com/pytorch/vision)
* [albumentations-team/albumentations](https://github.com/albumentations-team/albumentations/tree/f2462be3a4d01c872474d0e7fc0f32f387b06340)
* [aleju/imgaug](https://github.com/aleju/imgaug)
* [opencv/opencv](https://github.com/opencv/opencv)

```
@Article{info11020125,
    AUTHOR = {Buslaev, Alexander and Iglovikov, Vladimir I. and Khvedchenya, Eugene and Parinov, Alex and Druzhinin, Mikhail and Kalinin, Alexandr A.},
    TITLE = {Albumentations: Fast and Flexible Image Augmentations},
    JOURNAL = {Information},
    VOLUME = {11},
    YEAR = {2020},
    NUMBER = {2},
    ARTICLE-NUMBER = {125},
    URL = {https://www.mdpi.com/2078-2489/11/2/125},
    ISSN = {2078-2489},
    DOI = {10.3390/info11020125}
}

@misc{imgaug,
  author = {Jung, Alexander B.
            and Wada, Kentaro
            and Crall, Jon
            and Tanaka, Satoshi
            and Graving, Jake
            and Reinders, Christoph
            and Yadav, Sarthak
            and Banerjee, Joy
            and Vecsei, Gábor
            and Kraft, Adam
            and Rui, Zheng
            and Borovec, Jirka
            and Vallentin, Christian
            and Zhydenko, Semen
            and Pfeiffer, Kilian
            and Cook, Ben
            and Fernández, Ismael
            and De Rainville, François-Michel
            and Weng, Chi-Hung
            and Ayala-Acevedo, Abner
            and Meudec, Raphael
            and Laporte, Matias
            and others},
  title = {{imgaug}},
  howpublished = {\url{https://github.com/aleju/imgaug}},
  year = {2020},
  note = {Online; accessed 01-Feb-2020}
}
```

## 参与贡献方式

欢迎任何人的参与！打开[issue](https://github.com/zjykzj/ZTransforms/issues)或提交合并请求。

注意:

* `GIT`提交，请遵守[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)规范
* 语义版本化，请遵守[Semantic Versioning 2.0.0](https://semver.org)规范
* `README`编写，请遵守[standard-readme](https://github.com/RichardLitt/standard-readme)规范

## 许可证

[Apache License 2.0](LICENSE) © 2021 zjykzj