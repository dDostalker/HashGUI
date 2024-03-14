如果只想了解如何使用，请跳转以下页面[点击跳转](#使用链接)
If you only want to know how to use it, please jump to the following button[Click to jump to](#howtouse)

***The English part of this article was completed by machine translation. If there are any inaccuracies, please notify me in the Issues section***

# HashGUI
 A fan of HashCat created a GUI interface for its convenience in use
 
 ## path
 1. Python version: 3.10 and above, no external library, no git required (currently)
 2. Hashcat version required: the latest version
 3. Platform: Windows platform development, Linux platform available (to be measured in detail)
 4. Other requirements: see the official website of hashcat

<span id="howtouse"> use</span> 
## Using
Before use, it is important to understand that **this is just a Python script that assists hashcat in making it more convenient to work** . The prerequisite for running it is to first select the hashcat you already have
### Select
1. You can place hashcat in a folder called Hashcat in Script, and then you can see it in the dropdown menu
2. You can also click on the three selected points to select the path, so that the next time you open it, the hashcat path will be remembered by default
### Settings
Before using hashcat, proper settings are essential. As the software is still in the semi-finished stage, user errors may not be detected by this script. Therefore, the following settings should be filled in correctly before running
1. Hashcat path
2. Attack mode
3. Target Hash Type
4. Target file
5. Mask/Dictionary Settings
### Running
After setting the above settings, you can click on Run and then use it. In the semi-finished stage, the script will output all the information output by hashcat to the control panel, including the level of cracking. In the finished stage, it will be processed separately
Step by step is currently available for use
## Update plan
In the following updates, I will optimize the script as follows
1. Mask/Dictionary History
2. Use existing rulers
3. Multi task allocation management
4. Better return and processing of pages
5. A comprehensive error pre detection mechanism


# HashGUI
一个哈希猫的粉丝，对这个工具有着极大的热情，但是由于操作对于新人过于麻烦，亦或是对于处理小的问题需要较长时间，便用python写了如下工具，为了部分没有足够计算机储备的人，本代码没有使用python默认库以外的外部库


## 环境
1. python版本：3.10及以上，无外部库，无需git（目前）
2. hashcat需要版本：最新版本
3. 平台：Windows平台开发、linux平台可使用（待详细测速）
4. 其他要求：参见hashcat官网

<span id="使用链接">使用</span>
## 使用
使用前首先要了解，这**只是一个辅助hashcat更便捷工作**的python脚本，运行的前提是先要选中你已经有的hashcat
### 选择
1. 可以将hashcat放在名为脚本中hashcat的文件夹下，那之后你可以在下拉框中看见他
2. 也可以点击选择后的三个点来进行选择路径，这样下一次打开的时候会默认记住hashcat的路径
   
### 设置
使用hashcat之前，正确的设置是必不可少的，由于软件还在半成品阶段，使用者错误的使用可能不会被这个脚本检测出来，所以要将以下的几个设置正确填写后再运行
1. hashcat路径
2. 攻击模式
3. 目标Hash类型
4. 目标文件
5. 掩码/字典设置


### 运行
以上设置好后即可点击运行，然后使用，在半成品阶段，脚本会将hashcat输出的所有信息输出到控制台面版上，包括破译程度等，在成品阶段将会单独处理
步过目前已经可以使用

## 更新计划
再接下来的更新中，我将对脚本进行以下优化
1. 掩码/字典历史记录
2. 使用现有ruler
3. 多任务分配管理
4. 更好的返回和处理页面
5. 完善的错误预检测机制
