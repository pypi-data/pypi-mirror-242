# hxz_pandora

潘多拉 (hxz_pandora)，一个让你呼吸顺畅的 ChatGPT。

潘多拉实现了网页版 ChatGPT 的主要操作。后端优化，绕过 Cloudflare，速度喜人。

<!-- PROJECT SHIELDS -->

![Python version](https://img.shields.io/badge/python-%3E%3D3.7-green)
[![Issues](https://img.shields.io/github/issues-raw/zhile-io/hxz_pandora)](https://github.com/shoot82003/hxz_pandora/issues)
[![Commits](https://img.shields.io/github/last-commit/zhile-io/hxz_pandora/master)](https://github.com/shoot82003/hxz_pandora/commits/master)
[![PyPi](https://img.shields.io/pypi/v/hxz_pandora-chatgpt.svg)](https://pypi.python.org/pypi/hxz_pandora-chatgpt)
[![Downloads](https://static.pepy.tech/badge/hxz_pandora-chatgpt)](https://pypi.python.org/pypi/hxz_pandora-chatgpt)
[![PyPi workflow](https://github.com/shoot82003/hxz_pandora/actions/workflows/python-publish.yml/badge.svg)](https://github.com/shoot82003/hxz_pandora/actions/workflows/python-publish.yml)
[![Docker workflow](https://github.com/shoot82003/hxz_pandora/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/shoot82003/hxz_pandora/actions/workflows/docker-publish.yml)
[![Discord](https://img.shields.io/discord/1098772912242163795?label=Discord)](https://discord.gg/QBkd9JAaWa)

## 体验地址
* 点击 <a href="https://chat.shoot82003" target="_blank" title="hxz_pandora Cloud体验地址">https://chat.shoot82003</a>
* 最新拿 `Access Token` 的技术原理，我记录在[这里](https://shoot82003/2023/05/19/how-to-get-chatgpt-access-token-via-pkce.html)了。
* 可以访问 [这里](http://ai-20230626.fakeopen.com/auth) 拿 `Access Token`
* 也可以官方登录，然后访问 [这里](http://chat.openai.com/api/auth/session) 拿 `Access Token`
* `Access Token` 有效期 `14` 天，期间访问**不需要梯子**。这意味着你在手机上也可随意使用。
* 这个页面上还包含一个共享账号的链接，**没有账号**的可以点进去体验一下。
 
## ChatGPT使用时可能会遇到：

### 1. Please stand by, while we are checking your browser... 
### &nbsp;&nbsp;&nbsp;动不动来一下，有时候还不动或者出人机验证。痛！
![t0](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/t0.png)

### 2. Access denied. Sorry, you have been blocked
### &nbsp;&nbsp;&nbsp;经典问题，只能到处找可用VPN，费时费力，更费钱。移动端访问更难。痛！
![t1.1](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/t1.1.png)

### 3. ChatGPT is at capacity right now 
### &nbsp;&nbsp;&nbsp;系统负载高，白嫖用户不给用。痛！
![t2](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/t2.png)

### 4. This content may violate our <u>content policy</u>. 
### &nbsp;&nbsp;&nbsp;道德审查，多触发几次可能就封号了。痛！！！
![t3](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/t3.png)

### 5. Something went wrong. 
### &nbsp;&nbsp;&nbsp;吃着火锅唱着歌，突然就出故障了。痛！
![t4](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/t4.png)

### 6. 手机和电脑的模型不通用，顾这个就顾不到那个，痛！
![t7](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/t7.png)

### 7. 蹦字慢吞吞，卡顿不流畅，不知道的甚至想换电脑。痛！
### 8. 想把 `ChatGPT` 接到其他系统，结果只能接个差强人意的 `gpt-3.5-turbo`。痛！

### _一次看完上面的噩梦，血压上来了，拳头硬了！太痛了！！！以上痛点，`hxz_pandora` 一次全部解决。_

## 界面截图

  <details>

  <summary>

  ![alt Screenshot5](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s05.png)<br>
  ![alt Screenshot10](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s12.jpeg)

  </summary>

  ![alt Screenshot1](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s01.png)<br>
  ![alt Screenshot2](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s02.png)<br>
  ![alt Screenshot3](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s03.png)<br>
  ![alt Screenshot4](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s04.png)<br>
  ![alt Screenshot6](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s06.png)<br>
  ![alt Screenshot11](https://github.com/shoot82003/hxz_pandora/raw/master/doc/images/s11.jpeg)

  </details>

## 如何搭建运行

* 访问 [doc/wiki.md](https://github.com/shoot82003/hxz_pandora/blob/master/doc/wiki.md) 获得详细指导。

## 其他说明

* `开源项目可以魔改，但请保留原作者信息。确需去除，请联系作者，以免失去技术支持。`
* 项目是站在其他巨人的肩膀上，感谢！
* 报错、BUG之类的提出`Issue`，我会修复。
* 因为之后`ChatGPT`的API变动，我可能不会跟进修复。
* 喜欢的可以给颗星，都是老朋友了。
* 不影响`PHP是世界上最好的编程语言！`

## 贡献者们

> 感谢所有让这个项目变得更好的贡献者们！

[![Star History Chart](https://contrib.rocks/image?repo=zhile-io/hxz_pandora)](https://github.com/shoot82003/hxz_pandora/graphs/contributors)

## Star历史

![Star History Chart](https://api.star-history.com/svg?repos=zhile-io/hxz_pandora&type=Date)



1.先打包,注意版本号__init__.py修改版本号
清除构建
python setup.py clean
构建
python setup.py sdist bdist_wheel

2.再上传pypi命令
twine upload --skip-existing --verbose -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDg3YTQ3NzNlLWU3YjctNDFkOS04ZTQyLWFkNWQ2NzYwMDAxYgACKlszLCJiYWE5ZGY0ZS01OGRhLTQzMWMtOWJmYS1kMjIxNDNlNTg1MjAiXQAABiDR_mO7SkLd_caYiQkhYu68mAo5wd7KjpthKRO4AO3wsA dist/*

或者使用帐号密码(需手动输入)进行上传
py -m twine upload dist\*


3.安装,注意版本号,因为刚上传的原因无法安装时,需-i进行安装

pip install hxz_pandora-ChatGPT~=20230725.1.2


pip install -i https://pypi.org/simple/ hxz_pandora-ChatGPT~=20230725.1.4


pip install -i https://pypi.org/simple/ hxz_pandora_cloud~=20230725.1.4

4.若存在多个版本时会出错,可卸载后再pip install安装
pip uninstall hxz_pandora-chatgpt

替换:
1.https://github.com/zhile-io/pandora
    zhile-io    替换为     shoot82003
    pandora     替换为     hxz_pandora
    
    
2.admin@zhile.io
    admin@zhile.io  替换为     shoot82003@qq.com
    Neo Peng        替换为     Xiaozhou Huang
    zhile.io
    
3.__version__ = '1.3.5'
    版本号         替换为     1.0.2
    
4.网址替换
    https://github.com/zhile-io/pandora
    或 https://github.com/shoot82003/hxz_pandora
    替换为https://shootchat.top
    