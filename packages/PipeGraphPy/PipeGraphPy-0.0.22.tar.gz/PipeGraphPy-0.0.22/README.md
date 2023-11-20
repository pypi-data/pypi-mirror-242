 # Python 三方库 PipeGraphPy 使用手册
## 1. 简介
本文档为您介绍一款实用的 Python 三方库 PipeGraphPy，旨在帮助您快速上手并熟练使用该库。库名称：**PipeGraphPy**。本文档将分为以下几个部分进行介绍：
- 软件介绍
- 安装
- 基本使用  
- 高级功能  
- 示例代码  
- 常见问题与解决方案  
- 参考文献
## 软件介绍

### 软件简介

PipeGraphPy是一个Python三方库，主要功能是构建一种可用于训练、预测的有向无环图算法模型。它允许用户将多个预处理步骤和模型组合成一个整体，可以把这个整体看成一个组装模型或整体模型。整体模型也可以执行训练(fit)和预测(predict)。

### 名词解释

- 图模型：一种有向无环图模型，可执行训练、预测、保存、载入等一般模型的操作。
- 模型节点：组装图模型的节点，可以看做是模型组件的实例化对象，模型节点和模型节点之间可以执行连接操作。
- 模型组件：图模型节点的种类，本软件把软件的种类分为一下几种：
    - 数据导入(ImportData)
    - 前处理(Preprocessor)
    - 特征选择(Selector)
    - 特征转换(Transformer)
    - 回归算法(Regressor)
    - 分类算法(Classifier)
    - 深度学习(Deeplearning)
    - 集成学习()
    - 后处理(Postprocessor)
    1、数据导入(ImportData)：导入模型训练预测评估使用的数据。
    2、前处理(Preprocessor)：数据清洗：缺失值处理，异常值处理，降噪、过滤等方法。
    3、特征选择(Selector)：从原始特征中选择出对目标变量有重要影响的特征。例如：SKlearn中的feature_selection或XGB中的feature_importances_
    4、特征转换(Transformer)：训练特征发生了转变。例如：主成分分析（PCA）或线性判别分析（LDA）
    5、回归算法(Regressor)：sklearn, xgboost, 在组件内部可以使用交叉验证，网格搜索， 常用的有：MLP，SVM（SVR），随机森林，GridSearch。
    6、分类算法(Classifier): 
    6、深度学习(Deeplearning)：pytouch,tensorflow,keras, 常用的GRU,LSTM,ConLSTM,CNN。
    7、集成学习()：多模型数据替换，数据平均法、加权平均法，甚至可以实现stacking功能。
    8、后处理(Postprocessor)：预测数据的后处理，例如：装机容量的限制，数据入库，数据发送。
    9、数据拆分(Split): 一个数据拆分成多个数据。
    10、数据合并(Merge)：多个数据合并为一个数据。
- 模型连线: 模型节点和模型节点之间的连线，代表着模型中数据的流向，模型数据是pandas库提供的DataFrame格式

### 图模型框架

图模型是由模型节点和模型连线组合而成的一种有向无环图，图中节点代表着数据的导入和处理，连线代表着数据的流向。
图模型的框架比较自由，模型训练至少一个节点，模型训练过程，也可以叫数据处理过程，其执行不需要算法组件节点（回归算法、分类算法、深度学习）。但要想执行模型预测操作需要包含至少一个算法组件节点。
以下模型结构可作为参考：

#### 简单结构

#### 复杂结构


## 2. 安装
### 2.1 安装
安装 PipeGraphPy 需要有Python的环境，以及Python的pip包管理工具
使用以下命令安装 PipeGraphPy：
```bash  
pip install PipeGraphPy
```
## 3. 基本使用
### 3.1 库导入
在使用PipeGraphPy库时，主要使用其三个子类，导入方式如下：
```python  
from PipeGraphPy import Graph, Node, Module
```
### 3.2 快速上手


第一步：首先要准备“数据导入(ImportData)”和“回归算法(Regressor)”两个组件的代码(开发规范见下面章节)，以下为样例代码，代码分别放在 “test_data.py” 和 “test_reg.py” 文件里：

- test_data.py

```
class ImportExample():
    __version__ = "v1"
    TEMPLATE = [
        {
            "key": "data_length",
            "name": "训练数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 60,
            "desc": "字段说明"
        },
    ]
    params_rules = {}

    def __init__(self, **kw):
        self.params = kw
        self.farm_info = kw.get("biz_info", {})

    def run(self):
        df = pd.DataFrame(
            {
                "time":[
                    "2022-06-29 00:15:00",
                    "2022-06-29 00:30:00",
                    "2022-06-29 00:45:00",
                    "2022-06-29 01:00:00",
                    "2022-06-29 01:15:00",
                    "2022-06-29 01:30:00",
                    "2022-06-29 01:45:00",
                    "2022-06-29 02:00:00",
                    "2022-06-29 02:15:00",
                    "2022-06-29 02:30:00",
                ],
                "ws":[ 6.06, 6.11, 6.16, 6.21, 6.26, 6.31, 6.36, 6.41, 6.44, 6.47, ],
                "power":[ 18.38, 16.33, 19.2, 18.43, 16.93, 16.51, 14.49, 14.28, 10.53, 7.44, ],
            }
        )
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        return df

    def evaluate(self):
        df = pd.DataFrame(
            {
                "time":[
                    "2023-09-27 01:45:00",
                    "2023-09-27 02:00:00",
                    "2023-09-27 02:15:00",
                    "2023-09-27 02:30:00",
                    "2023-09-27 02:45:00",
                    "2023-09-27 03:00:00",
                    "2023-09-27 03:15:00",
                    "2023-09-27 03:30:00",
                    "2023-09-27 03:45:00",
                    "2023-09-27 04:00:00",
                ],
                "ws":[ 5.2574, 5.5224, 5.407, 5.23, 5.1162, 4.8671, 4.9085, 4.5645, 4.0683, 3.9026 ],
                "power":[ 14.328, 14.567, 15.3, 13.58, 17.66, 13.56, 17.44, 12.43, 14.62, 9.44 ],
            }
        )
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        return df

    def predict(self):
        df = pd.DataFrame(
            {
                "time":[
                    "2023-10-29 00:15:00",
                    "2023-10-29 00:30:00",
                    "2023-10-29 00:45:00",
                    "2023-10-29 01:00:00",
                    "2023-10-29 01:15:00",
                    "2023-10-29 01:30:00",
                    "2023-10-29 01:45:00",
                    "2023-10-29 02:00:00",
                    "2023-10-29 02:15:00",
                    "2023-10-29 02:30:00",
                ],
                "ws":[ 4.07, 4.11, 4.15, 4.2275, 4.19, 4.265, 4.3025, 4.34, 4.3725, 4.405 ],
            }
        )
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        return df
```

- test_reg.py

```
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.utils.validation import check_array
import numpy as np


class SVMRegExample:
    __version__ = 'v1.2'
    def __init__(self, **kw):
        self.params = kw
        self.model = SVR()
        self.scaler_x = StandardScaler()
        self.scaler_y = StandardScaler()

    def fit(self, X, y):
        X = check_array(X)
        X_min_max = self.scaler_x.fit_transform(X)
        y_min_max = self.scaler_y.fit_transform(np.array(y).reshape(y.shape[0], -1))
        self.model.fit(
            X_min_max,
            y_min_max.reshape(-1,),
        )
        return self

    def predict(self, X):
        X_min_max = self.scaler_x.transform(X)
        y = self.model.predict(X_min_max)
        y_inverse = self.scaler_y.inverse_transform(y.reshape(y.shape[0], -1))
        y_inverse = y_inverse.reshape(-1,)
        X["power_predict"] = y_inverse
        return y_inverse
```
> 注意：算法里用到了sklearn和numpy三方包，请自行安装

第二步: 搭建和训练图模型

- train.py

```
# 导入两个组件类
from test_data import ImportExample
from test_reg import SVMRegExample


# 创建图模型
model = Graph.create()
# 创建数据导入节点
data_node = Node.create(Module.create(mtype="ImportData", mcls=ImportExample), graph=model)
# 创建算法节点
reg_node = Node.create(Module.create(mtype="Regressor", mcls=SVMRegExample), graph=model)
# 连接两个节点
data_node.connect(reg_node)
# 模型结构打印
model.print()
# 训练模型
model.run()
# 保存模型
clone_model.save("svm_model.pkl")

```


第三步：拿训练好的模型预测

- predict.py

```
# 载入模型
model = Graph.load("svm_model.pkl")
# 模型预测
predict_res = model.predict()
# 查看预测结果
print(predict_res)
```

### 3.3 模块功能使用说明

#### 3.3.1 Graph 模块

- 1、创建自定义模型
```python
help(Graph.create)
custom_model = Graph.create(instance_id="电场id", name="模型名称")
```

- 2、克隆已有模型
```
clone_model = Graph(760).clone()
clone_model.print()
```

- 3、训练模型
`clone_model.run()`

- 4、模型预测
`predict_data = clone_model.predict()`

- 5、获取节点训练数据
```
clone_model.nodes
clone_model.nodes[0].run_result
```

- 6、获取节点预测数据
`clone_model.predict_result(clone_model.nodes[0].id)`

- 7、模型保存
`clone_model.save("svm_model.pkl")`

- 8、载入模型
```python
reload_model = Graph.load("svm_model.pkl")
pred_res = reload_model.predict()
```

#### 3.3.2 Module 模块

 ### 1、新建组件
 `help(Module.create)`

图模型节点的种类，本软件把软件的种类分为一下几种：
    1、数据导入(ImportData)：导入模型训练预测评估使用的数据。
    2、前处理(Preprocessor)：数据清洗：缺失值处理，异常值处理，降噪、过滤等方法。
    3、特征选择(Selector)：从原始特征中选择出对目标变量有重要影响的特征。例如：SKlearn中的feature_selection或XGB中的feature_importances_
    4、特征转换(Transformer)：训练特征发生了转变。例如：主成分分析（PCA）或线性判别分析（LDA）
    5、回归算法(Regressor)：sklearn, xgboost, 在组件内部可以使用交叉验证，网格搜索， 常用的有：MLP，SVM（SVR），随机森林，GridSearch。
    6、分类算法(Classifier): 
    6、深度学习(Deeplearning)：pytouch,tensorflow,keras, 常用的GRU,LSTM,ConLSTM,CNN。
    7、集成学习()：多模型数据替换，数据平均法、加权平均法，甚至可以实现stacking功能。
    8、后处理(Postprocessor)：预测数据的后处理，例如：装机容量的限制，数据入库，数据发送。
    9、数据拆分(Split): 一个数据拆分成多个数据。
    10、数据合并(Merge)：多个数据合并为一个数据。


#### 3.3.3 Node 模块
- 1、创建新的节点
```python
help(Node.create)
# 线上组件节点
import_node = Node.create(online_module, graph=custom_graph, name="线上模型节点") # name可省略
# 自定义组件节点
reg_node = Node.create(custom_module, custom_graph, name="自定义节点")  # name 可省
# 节点连线
import_node.connect(reg_node)
help(import_node.connect)
```

- 2、单节点执行
```python
train_data = import_node.run()
predict_data = import_node.predict()
evaluate_data = import_node.get_evaluate_data(windows=20)
reg_node.run(train_data)  # 传递上一节点数据
```

- 3、节点参数设置
```python
# 默认参数
import_node.default_params
# 修改默认参数
import_node.params = {
    'data_length': 4,
    'train_validation_proportion': '0.5',
    'reserve_length': 1
}
import_node.run()
```


以下为您介绍库中的常用功能：
- 功能 1：
  ```python  
  xxx 库。功能 1()  
  ```
- 功能 2：
  ```python  
  xxx 库。功能 2(参数 1, 参数 2)  
  ```
## 4. 组件开发规范
以下为您介绍库的高级功能：
- 高级功能 1：
  ```python  
  xxx 库。高级功能 1(参数 1, 参数 2)  
  ```
- 高级功能 2：
  ```python  
  xxx 库。高级功能 2(参数 1, 参数 2)  
  ```
## 5. 示例代码
以下是一个完整的示例代码：
```python  
# 导入库  
import xxx 库
# 功能 1 示例  
xxx 库。功能 1()
# 功能 2 示例  
xxx 库。功能 2(参数 1, 参数 2)
# 高级功能 1 示例  
xxx 库。高级功能 1(参数 1, 参数 2)
# 高级功能 2 示例  
xxx 库。高级功能 2(参数 1, 参数 2)  
```
## 6. 常见问题与解决方案
### 6.1 问题 1
描述：在使用过程中，可能会遇到问题 1。
解决方案：
1. 检查库版本，确保与您的 Python 版本兼容。  
2. 检查导入语句，确保正确导入库。  
3. 检查参数传递，确保符合函数参数要求。
### 6.2 问题 2
描述：在使用过程中，可能会遇到问题 2。
解决方案：
1. 更新库版本，确保使用最新功能。  
2. 查阅文档，了解详细使用方法。  
3. 在官方论坛或社区寻求帮助。
## 7. 参考文献
- [Python 官方文档](https://docs.python.org/3/index.html)  
- [库官方文档](https://www.example.com/doc/xxx 库)  
- [Python 教程](https://www.runoob.com/python/python-tutorial.html)
本文档仅供参考，具体使用过程中遇到的问题，请随时查阅相关文献或与开发者联系。感谢您的使用和支持！
