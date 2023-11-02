---
title: Mail-Reminder-by-Transfer
date: 2023-10-28 20:57:48
tags: Python
---

[TOC]

# 能做什么？

1. 自动登录交大邮箱，由上一时刻保存的邮件数与此时刻的邮件数对比，判断有无新邮件；
2. 如果“1”的结果为真，则解析最新邮件的主题，并转发至设置的 QQ 邮箱；
3. QQ 邮箱小程序会推送结果到微信与 QQ；
4. 通过 github actions 实现上述过程的自动化，可以定时检测提醒。



# 如何使用？

1. 修改配置文件 `config.txt`：
   1. `%%%` 替换成自己的；
   2. `encrypted` 的 `0` 表示未加密，不用修改；
   3. `pop3_server` 表示服务器地址，不用修改；

2. 下载 `requirements.txt` 中的依赖项， 运行 `main.py`；
3. 注意：第一次运行为初始化，获取初始邮件数。

```txt
{'account': '%%%@sjtu.edu.cn', 'password': '%%%', 'receiver': '%%%qq.com', 'pop3_server': 'mail.sjtu.edu.cn', 'encrypted': 0}
```



# 问题？

1. 安全性：
   1. 问题：将密码直接输入，进行简单的加密，虽然保存的是密文，但可以通过程序倒推出密码明文，整体安全性不够；

   2. **解决【unsolved】**：使用 github 中的 TOKEN 作为密钥，即运行时每个用户拥有唯一的密钥；

   3. **解决【solved】【2023-11-01】**：在 github actions 的配置文件中设置环境变量，在 python 程序中设置接口；

      ```yaml
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      ```

      ```python
      try:
          GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
      except KeyError:
          print('Please define the environment variable GITHUB_TOKEN')
      ```

      在上传 github 仓库时，需要保留密码明文进行初始化操作，此时有一定风险：可以直接获取 TOKEN 使用 `encrypt.py` 加密后再上传。

      由于每个人的 TOKEN 不同，可以起到较好的保密效果。

   4. **解决【solved】【2023-11-01】**：在 github repository 中设置 repository secrets，并在 python 程序中设置接口；
   
      ```yaml
      env:
        SUPER_TOKEN: ${{ secrets.SUPER_TOKEN }}
      ```
   
      ```PYTHON
      try:
          SUPER_TOKEN = os.environ['SUPER_TOKEN']
      except KeyError:
          print('Please define the environment variable SUPER_TOKEN')
      ```
   
2. 实用性：
   1. 问题：只有最新邮件，提醒不到位；
   2. 解决：该程序仅作提醒，若要提醒多封邮件，可以更改 `main.py` 中的转发邮件部分，参照 [编程 | 详解使用Python接收邮件](https://developer.aliyun.com/article/903464#:~:text=%E7%BC%96%E7%A8%8B%20%7C%20%E8%AF%A6%E8%A7%A3%E4%BD%BF%E7%94%A8Python%E6%8E%A5%E6%94%B6%E9%82%AE%E4%BB%B6%201%201.%E5%9F%BA%E6%9C%AC%E6%AD%A5%E9%AA%A4%20%E8%BF%9E%E6%8E%A5%E5%88%B0%E6%9C%8D%E5%8A%A1%E5%99%A8%E3%80%82%20%E7%99%BB%E9%99%86%E3%80%82%20%E5%8F%91%E5%87%BA%E6%9C%8D%E5%8A%A1%E8%AF%B7%E6%B1%82%E3%80%82,3.%E8%A7%A3%E6%9E%90%E9%82%AE%E4%BB%B6%E4%B8%BB%E9%A2%98%20...%204%204.%E8%A7%A3%E6%9E%90%E9%82%AE%E4%BB%B6%E6%9D%A5%E6%BA%90%20...%205%205.%E8%A7%A3%E6%9E%90%E9%82%AE%E4%BB%B6%E5%86%85%E5%AE%B9%20)；

3. 登录 SJTU 服务器读取邮件没问题，转发邮件失败：

   1. 有可能是转发邮件过多导致 QQ 邮件被封...




# 关于 github actions 中的 `config.yml`

```yaml
name: Python application

on:
  workflow_dispatch:
  schedule:
    - cron: '30 0-23 * * *'
  push:

permissions: write-all

env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        cache: 'pip'
        cache-dependency-path: 'requirements.txt'
    - run: pip install -r requirements.txt

    - name: tree
      run: |
        tree

    - name: Run main
      run: |
        git pull
        cat config.txt
        python main.py
        cat config.txt
    
    - name: Commit files
      run: |
        git init
        git config --local user.email "l921832312@qq.com"
        git config --local user.name "Jayliu9218"
        ls
        git add info.txt config.txt
        git commit -m "AUTO"
        
    - name: Push changes
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        branch: ${{ github.ref }}
        
```



[more info](https://github.com/Jayliu9218/Mail-Reminder-by-Transfer)