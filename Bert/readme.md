# BERT多标签分类模型
## 简介和功能
1.主要目的：根据已有的景点名称和对应的标签来进行语言模型的训练，期望在输入新的景点名称之后，模型能够生成对应的标签。

2.延申功能：可以针对其他的旅游实体进行训练，达到多标签分类的效果。


## 运行环境和要求
1. Jupyter Notebook：确保你已经安装了Jupyter Notebook并可以运行它。（建议使用anaconda来配置环境）
2. Python环境：确保你已经安装了Python，并且可以在Jupyter Notebook中使用它。
3. PyTorch库：这段代码使用了PyTorch库进行深度学习模型的训练。
4. Transformers库：这段代码还使用了Transformers库
5. GPU支持。





## 使用方法
1. 下载代码。
2. 检查完环境是否达到要求（建议有GPU资源，使用CPU会导致训练速度过慢）
3. 根据需要修改输入和输出文件的路径名称，如下图：

![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1695813386929-3e54db77-cacb-40d9-ad18-54fb8424a8ae.png)

![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1695813485953-7126f237-ea47-43cb-ba5d-33f0af6a6551.png)

4. 运行直至所有循环完成。
5. 根据保存的数据进行分析。

## 输入的数据要求
无论是训练集还是验证集，所有数据都在json文件中，格式如下：

```plain
[
  {
    "text": "景点一",
    "label": [
      "标签一",...
    ]
  },
  {
    "text": "景点二",
    "label": [
      "标签二",...
    ]
  },
	...
]
```

注意事项：训练集的数据量要比验证集大几倍，同时需要确保每个标签都有在两个数据集中出现过（不然可能会报错说向量大小不符）



## 输出的数据格式
输出的数据长这样：

```plain
[
  {
    "logits": [
      3.1482012271881104,
      -5.3884077072143555,
      -5.269010543823242,
      -5.077752113342285,
      -5.820712566375732,
      -3.990055799484253,
      -5.205063343048096,
      -5.386012077331543,
      -4.852389812469482
    ],
    "labels": [
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ]
  },
  {
    "logits": [
      -4.153970718383789,
      -5.380253314971924,
      -5.827282905578613,
      -5.651237964630127,
      -5.983510494232178,
      3.8447048664093018,
      -6.137881755828857,
      -5.129909992218018,
      -5.729831218719482
    ],
    "labels": [
      1.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0
    ]
  },
	...
]
```

如何使用输出结果：

针对“logits”，可以设置不同的阈值来区分某个标签是否可以判定为positive（设置为1），反之为negative（设置为0）.

最后用处理过的“logits”与“labels”（即正确的标签）来进行对比，以分析模型的效果如何。

## 主要代码流程分析
### 模型参数的设置：
![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1695814219132-b66d6501-b528-4c17-b395-b805ba722df4.png)

采用的预训练模型是'bert-base-chinese'。

![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1695814375979-f939f680-2618-405f-ae09-9ee1c77abb7b.png)

其中num_epoches是循环次数（默认为30），optimizer是优化器。

### 训练流程：
```plain
  model.train()
  train_loss = 0.0  #初始化loss值

  train_results = []
  for batch in train_loader:
      optimizer.zero_grad()  #遍历所有参数，清空上次训练的参数梯度

      input_ids = batch['input_ids'].to(device) 
      attention_mask = batch['attention_mask'].to(device)
      labels = batch['label'].to(device)  #上面三行是将数据输入到训练工具上（GPU）

      outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
      loss = outputs.loss  #获得单此训练后的loss值
      logits = outputs.logits  #将训练结果进行保存

      loss.backward()  #逆向传播（计算梯度）
      optimizer.step()  #进行一次优化步骤（基于梯度下降）

      train_loss += loss.item()  #累加loss
      for i in range(len(logits)):
          result = {
              'logits': logits[i].detach().cpu().numpy().tolist(),
              'labels': labels[i].detach().cpu().numpy().tolist()
          }
          train_results.append(result)  #保存结果
```

### 验证流程：
```plain
  model.eval()
  val_loss = 0.0  #初始化loss值
  predictions = []  #初始化空的预测值列表

  with torch.no_grad():
      valid_results = []
      for batch in validation_loader:
          input_ids = batch['input_ids'].to(device)
          attention_mask = batch['attention_mask'].to(device)
          labels = batch['label'].to(device)  #上面三行是将数据输入到训练工具上（GPU）

          outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
          loss = outputs.loss  #获得单此训练后的loss值
          logits = outputs.logits  #将训练结果进行保存

          val_loss += loss.item()  #累加loss
          predictions.extend(logits.sigmoid().cpu().numpy()) #记录所有预测结果到列表中
          for i in range(len(logits)):
              result = {
                  'logits': logits[i].detach().cpu().numpy().tolist(),
                  'labels': labels[i].detach().cpu().numpy().tolist()
              }
              valid_results.append(result)  #保存结果
```



## 实验
### 数据来源：
    1. 来自客路的约800条已分类的数据。
    2. Chatgpt打标的约1000条已分类的数据。

#### 数据特点
这些数据中有657条景点是相同的（标签可能会不同），146条是客路的数据（简称为原始数据）独有的，423条是gpt数据独有的。



#### 训练集与验证集的生成策略
首先针对每种标签（9个），计算含有这个标签的总数居，然后按照4：1：1的比例分成训练集和不同的验证集，其中对于每个验证集，优先从自己的数据里提取，如果不够则从另外的数据中提取。



### 数据结果:
#### 描述
如果使用训练集的gpt产生的标签进行训练，则两个验证集的准确率均约为60%。

如果使用训练集的原始数据提供的标签进行训练，则GPT验证集的准确率约为40%，原始数据的验证集准确率约为45%。

#### 可视化表示
##### 四组数据的验证集情况
![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1696854252750-1dee781a-84a8-40e0-9458-fc0919e09e05.png)![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1696854252743-63545c87-bf25-4831-9029-874d1be04ba8.png)![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1696854252823-f3be69c5-9f84-44d9-a9c2-09c4b2d063be.png)![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1696854252859-3558c108-40af-418f-88c0-2f3de087367b.png)

##### 结论
经过观察，我们可以发现，对于使用原始数据作为训练集的两组数据而言，在尽可能保证准确率 (accuracy)，精确率 (precision)，召回率 (recall)的前提下，在阈值取-0.4到-0.5之间的时候，验证集的准确度差不多在40%到45%之间。而对于使用GPT数据作为训练集的话，无论验证集使用的是原始数据还是GPT数据，都有约60%的准确率。因此，采用GPT数据作为训练集是一个不错的选择。



##### 四组数据的准确率对比
![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1696854550211-7fafebd0-c4cc-4ab6-8d11-0931509c753e.png)

通过这个总表可以看出来，使用GPT数据作为训练集能够获得相较于使用原始数据作为训练集好很多的准确率。

#### 错误分类样例
分类结果中“Others”出错的次数最多

| | <font style="color:black;">Water Parks</font> | <font style="color:black;">Villages</font> | <font style="color:black;">Playgrounds</font> | <font style="color:black;">Others</font> | <font style="color:black;">Natural Landscape</font> | <font style="color:black;">Gardens & Parks</font> | <font style="color:black;">Observation Decks & Towers</font> | <font style="color:black;">Zoos & Animal Parks</font> | <font style="color:black;">Museums & Galleries</font> |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <font style="color:black;">Positive False</font><font style="color:black;"> </font> | <font style="color:black;">0</font> | <font style="color:black;">5</font> | <font style="color:black;">0</font> | <font style="color:black;">33</font> | <font style="color:black;">4</font> | <font style="color:black;">3</font> | <font style="color:black;">1</font> | <font style="color:black;">1</font> | <font style="color:black;">20</font> |
| <font style="color:black;">Negative False</font> | <font style="color:black;">1</font> | <font style="color:black;">0</font> | <font style="color:black;">7</font> | <font style="color:black;">26</font> | <font style="color:black;">5</font> | <font style="color:black;">11</font> | <font style="color:black;">7</font> | <font style="color:black;">0</font> | <font style="color:black;">14</font> |




其中“Others”的Negative Fasle中，许多错误都是来自于将景点误判为“<font style="color:black;">Museums & Galleries”：</font>

![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1697453335033-b2b4d4d6-843f-482b-b837-f45b1a08fc64.png)

Others”的Positive Fasle中，错误分布相对比较均匀：

![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1697453307924-01e132e6-e89f-44dd-98e9-db09877a2372.png)



#### 其它数据分析补充
如果采用更宽松的判断标准：

1.只有预测的结果中有不应该出现的结果时才判为失败，也就是允许少判断标签，例如正确标签是1和2，则预测为1或这预测为2都不算错误，只有出现了1和2之外的预测才算错误，同时如果标签都是0则也算预测错误。![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1697455913190-a95fe55e-7c15-4edf-9f98-980809c8a167.png)	2.允许预测结果出现最多一个不一样的结果，但是不允许标签的缺少。

![](https://cdn.nlark.com/yuque/0/2023/png/35498984/1697455677282-9dbc083c-41af-43e9-b548-d620048f5582.png)


