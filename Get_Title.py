import requests
from bs4 import BeautifulSoup

# 请求网页内容
url = "https://www.xbookcn.net/"
response = requests.get(url)
response.encoding = 'utf-8'

# 使用BeautifulSoup解析网页
soup = BeautifulSoup(response.text, 'html.parser')

# 查找所有<a>标签，并提取其中的文字内容
texts = [a_tag.get_text(strip=True) for a_tag in soup.find_all('a')]

# 将所有文字按指定格式输出
output = ', '.join([f'"{text}"' for text in texts])

print(output)
