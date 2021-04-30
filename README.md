# 写中文实现自动化操作脚本


这个框架设计的初衷是为了以更低的成本编写UI自动化脚本，并且可以让编写出来的内容直接与用例条目对应。因而可以节省在传统模式下，功能测试提交用例给自动化测试进行用例转换的过程。

他使用起来非常方便，只需要通过excel表格的编写来完成用例的自动化实现。

这里就主要对如何写表，涉及怎样的编写规范，以及每一个动作，每种检测方法和如何进行局外模块化的归类，作以说明。

gitlab地址[CnTestFrame](https://gitlab.ilongyuan.cn/lytg/cntestframe)


├─case  			—用例目录
│  ├─case.xlsx  			用例
├─common  			方法调用目录
│  ├─cls_coclient  			常用公共方法
│  ├─pytest_func  			pytest专用方法
│  ├─test_report  			allure相关存放
├─report  			报告相关存放目录
├─run  			框架的运行文件
├─test_case  			实际被运行文件执行的用例执行文件

## 具体说明

**让我们先来看一个例子**

|用例编号|用例描述|测试步骤|预期结果|
| ------------ | ------------ |------------| ------------ |
| Home_exp1 | 开始游戏超时确认场景检测 |点击"大厅"<br>点击"开始下棋"<br>等待出现"进入游戏"<br>等待消失"进入游戏"|不显示"进入游戏"
看用例描述，我们可以很清楚的知道这个用例是想干嘛。但是为什么以这个用例为例子呢，因为他分别用到了操作步骤和判断步骤，这也是编写用例中最重要的部分。

### 一.表格结构说明：

1. 用例编号:编号的格式是[模块名_用例编号]（如Home_exp1）

2. 用例描述:这条用例本身是要做什么的说明
3. 测试步骤:用例需要实时的具体内容，是执行定向操作检测的核心依据

4. 预期结果:测试步骤运行完后对当前界面进行检查判断结果的部分
5. excel表本身分为两张，一张是case_sheet,也就是我们本次主要说明的内容，第二张是config_sheet,指的是检测时我们应设置的配置。

### 二.如何编写测试步骤:
> 简单的说，测试步骤实际上是为了完成用例描述中的测试目的，需要进行哪些UI层面的操作而执行的步骤，这里对测试步骤中，具体我们可以做什么操作，每个操作应该怎么编写表格内容做一个说明。
需要注意的是，所有的表格编写内容中，要注意没有任何中文标点符号的存在

**动作类指令说明**

1. 点击:格式为 [点击”中文”]或者[点击”200,200”]。点击事件可以输入一个坐标或者文本，点击对应位置或者文本所在区域。

2. 滑动:格式为滑动”[200,200],[300,300]”，是从一个坐标滑动到另一个坐标的意思
3. 长按：支持对某个坐标或文字进行长按，格式:长按”中文”,或长按“100，100“（因为只有一个点所以不需要括号）
4. 等待出现: 格式为[等待出现”中文“]。意思是等待某个界面，某个文本的出现。因为我们的目的是可以靠中文来编写自动化脚本，所以这里采用等待某个文本出现的方式。在我们实际游戏的过程，如自走棋点击开始下棋，等待匹配成功，直到提示点击进入游戏，为了满足等待”进入游戏”这个界面出现，就需要这样的操作。

5. 截屏：格式为[截屏”截图名称”]（不需要带后缀哦）进行截屏的方法，会保存在手机的根目录下，以png的形式。
6. 输入：格式为[输入”请点击输入:耗子尾汁”],也就是框的中文:想要输入的内容。
7. 返回：安卓返回键的封装，格式：返回 两个字即可。

**判断类指令说明**

1. 等待消失:与出现的意思相反，比如我点击进入了另外一个界面，先前界面存在的某个UI中的文本就会消失，这个时候我们以某一个中文的消失为节点，验证对应的跳转等是否生效，界面本身是否切换了。 格式为:等待消失”中文”

2. 存在:不是出现或者消失，而是当前界面目前是否存在某一个文字的判断，例如查看商店中某些东西是否上架，上架了的项应该被”存在”这个项本身所识别到，否则算作用例执行失败，即为发现了bug 格式为:存在”中文”
3. 不存在：与存在相反的概念，比如某个商品下架了，就该被检测不到 格式为：不存在“中文“

4. 等待:这个等待就只是单纯的等待，操作间的间隔或者别的什么，没有什么逻辑在里面。格式为:等待”20”(20这个数字代表想要等待的秒数)

> 所有界面中的中文或其他文本信息，都是通过UI界面的元素信息获取到的。所以并不是所有的文本信息都可以被识别到，举一个简单的例子就是图片字、艺术字这种，其实这样的情况并不难以区分，使用时还需实际观测。

### 三.	如何填入预期结果：
这个因为只是通过UI层的检测，所以只能以什么东西显示，什么东西不显示作为判断进行预期结果的输入。
显示：某个东西在运行结束后存在于当前界面，格式就是显示”中文”
不显示：不显示“中文“
### 四.	用例编号的模块命名：
这里只用于局外检测的话，分了以下几个模块：
大厅：Home,仓库:Warehouse，商店:Store,活动:Active，锦标赛：Season，制图工坊：Workshop
### 五.	关于配置：
在表结构最开始的部分就有提到，这一部分的配置都是存储在config_sheet中的。
运行时确保对应设备配置了adb环境，python3.6以上，以及requests的安装。并保证游戏打开处于局外静态页面，其他游戏按照自己流程来，有遇到问题也可以直接联系框架制作人。

|参数|值|
| ------------ | ------------ |
| apk路径 |  测试路径 |
| 连接服务器  | target_ip:3063  |
| 测试用例模块  |  Home |
|  测试报告访问地址 |  http://172.16.56.77/jenkins/workplace/workspace/CnTestFrame/report/index.html |
填好对应的配置就可以运行了，apk路径和连接服务器这两个参数用于从装包开始直到进入游戏的流程，如果要从装包开始的话需要填入，否则删除这两项的内容。
测试模块为你想要测试的选择，填入“Store”或者"Home"他就会执行某一个模块，而如果全都要就填入all。
报告的访问地址也就按自己的存储路径来了，这里随便写了执行机的一个路径。