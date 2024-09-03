[English](https://github.com/ystemsrx/Porn-Novel-Scraper)

# 色情小说抓取器

## 描述
该仓库包含两个Python脚本：`Get_Title.py` 和 `Get_Passage.py`，它们协同工作以从目标网站抓取色情小说。脚本从网站上不同类别的色情小说中提取标题和相应内容。

## Get_Title.py

### 描述
`Get_Title.py` 用于抓取并提取指定网页上所有 `<a>` 标签的标题。这些标题将与 `Get_Passage.py` 一起使用，以过滤和获取目标网站上的特定内容。

### 功能
- **网页抓取**：从提供的URL获取HTML内容。
- **标题提取**：从网页上的所有 `<a>` 标签中提取标题。
- **输出格式化**：将提取的标题格式化为用双引号括起来的逗号分隔列表。

### 使用方法
1. 确保已安装所有必需的库：
   ```bash
   pip install requests beautifulsoup4
   ```
2. 修改 `url` 变量以指向目标网页。
3. 运行脚本以生成标题列表：
   ```bash
   python Get_Title.py
   ```
4. 使用输出的标题来填充 `Get_Passage.py` 中的 `names` 列表。

## Get_Passage.py

### 描述
`Get_Passage.py` 使用 `Get_Title.py` 提取的标题，从网站上抓取并获取相应的色情小说。它处理多个类别，并将清理后的内容保存到JSON文件中。抓取的色情小说涵盖了广泛的类型和主题。

### 功能
- **并发抓取**：使用多线程同时抓取多个类别的内容。
- **错误处理**：重试失败的请求以确保内容获取。
- **内容清理**：移除不需要的HTML标签和元素（如作者信息），以获得更清洁的输出。
- **JSON输出**：将清理后的内容存储到JSON文件中，每个文件代表一个特定类别。

### JSON文件格式
`Get_Passage.py` 抓取的内容以如下格式存储在JSON文件中：
```json
[
  {"text": "document"},
  {"text": "document"}
]
```
此格式可用于进一步分析或用于训练模型。

### 使用方法
1. 安装所需库：
   ```bash
   pip install requests beautifulsoup4 urllib3
   ```
2. 用 `Get_Title.py` 提取的标题填充 `Get_Passage.py` 中的 `names` 列表。
3. 运行脚本以抓取并保存内容：
   ```bash
   python Get_Passage.py
   ```
4. 脚本将创建包含抓取小说的JSON文件，这些文件按类别组织。

### 重要提示
- 确保 `Get_Passage.py` 中的 `names` 列表已用 `Get_Title.py` 提取的准确标题填充。
- 脚本在请求之间引入了延迟，以防止对目标服务器造成负担。

## 免责声明
此仓库仅用于教育目的。使用这些脚本抓取的内容和数据在某些司法管辖区可能是非法或不道德的。请负责任地使用这些工具，并确保遵守当地的法律法规。

---
