如果只想了解如何使用，请跳转以下页面[点击跳转](#使用链接)
If you only want to know how to use it, please jump to the following button[点击跳转](#)

***The English part of this article was completed by machine translation. If there are any inaccuracies, please notify me in the Issues section***

# HashGUI
 A fan of HashCat created a GUI interface for its convenience in use
# HashGUI
一个哈希猫的粉丝，对这个工具有着极大的热情，但是由于操作对于新人过于麻烦，亦或是对于处理小的问题需要较长时间，便用python写了如下工具，为了部分没有足够计算机储备的人，本代码没有使用python默认库以外的外部库


## 环境
1.python版本：3.10及以上，无外部库，无需git（目前）
2.hashcat需要版本：最新版本
3.平台：Windows平台开发、linux平台可使用（待详细测速）
4。其他要求：参见hashcat官网

<span id="使用链接">使用</span>
## 使用
使用前首先要了解，这**只是一个辅助hashcat更便捷工作**的python脚本，运行的前提是先要选中你已经有的hashcat
### 选择
1. 可以将hashcat放在名为脚本中hashcat的文件夹下，那之后你可以在下拉框中看见他
2. 也可以点击选择后的三个点来进行选择路径，这样下一次打开的时候会默认记住hashcat的路径
   
### 设置
使用hashcat之前，正确的设置是必不可少的，由于软件还在半成品阶段，使用者错误的使用可能不会被这个脚本检测出来，所以要将以下的几个设置正确填写后再运行
1.hashcat路径
2.攻击模式
3.目标Hash类型
4.目标文件
5.掩码/字典设置


### 运行
以上设置好后即可点击运行，然后使用，在半成品阶段，脚本会将hashcat输出的所有信息输出到控制台面版上，包括破译程度等，在成品阶段将会单独处理
步过目前已经可以使用

## 更新计划
再接下来的更新中，我将对脚本进行以下优化
1.掩码/字典历史记录
2.使用现有ruler
3.多任务分配管理
4.更好的返回和处理页面
5.完善的错误预检测机制
