import requests
from bs4 import BeautifulSoup
import json
import re
import threading
import time
import os
import urllib.parse
from tqdm import tqdm

stop_event = threading.Event()
TIMEOUT = 10  # seconds

def get_categories():
    url = 'http://w2.h528.com/'
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.encoding = 'utf-8'  # 确保正确处理中文编码
    except requests.exceptions.RequestException as e:
        print(f"请求主页面时发生错误：{e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    categories = []

    # 查找所有符合条件的类别链接
    for li in soup.find_all('li', class_=re.compile('^cat-item cat-item-')):
        if stop_event.is_set():
            break
        a_tag = li.find('a')
        if a_tag:
            category_url = a_tag['href']
            # 检查链接中是否包含 URL 编码的字符（%开头的十六进制数）
            if re.search(r'%[0-9A-Fa-f]{2}', category_url):
                decoded_url = urllib.parse.unquote(category_url)
                # 检查解码后的链接中是否包含中文字符
                if re.search(r'[\u4e00-\u9fff]', decoded_url):
                    category_name = a_tag.get_text(strip=True)
                    categories.append({'name': category_name, 'url': category_url})
    return categories

def get_article_links(category_url, page_number):
    if stop_event.is_set():
        return None
    if page_number == 1:
        url = category_url
    else:
        url = f"{category_url}/page/{page_number}"

    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        print(f"请求页面 {url} 时发生错误：{e}")
        return None

    if '<h2 class="center">Error 404 - Not Found</h2>' in response.text:
        return None  # 结束条件

    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = []
    for a in soup.find_all('a', rel='bookmark'):
        if stop_event.is_set():
            break
        if 'Permanent Link to' in a.get('title', ''):
            article_links.append({'url': a['href'], 'title': a.get_text(strip=True)})
    return article_links

def remove_invisible_characters(text):
    # 定义不可见字符的Unicode范围
    invisible_chars = [
        ('\u200b', '\u200f'),  # 零宽字符和其他格式字符
        ('\u202a', '\u202e'),  # 左到右嵌入等
        ('\ufeff', '\ufeff'),  # BOM
    ]
    for start, end in invisible_chars:
        pattern = f'[{start}-{end}]'
        text = re.sub(pattern, '', text)
    # 删除其他不可见字符，但保留换行符 \n
    text = ''.join(ch for ch in text if ch.isprintable() or ch == '\n')
    return text

def get_article_content(article_url):
    if stop_event.is_set():
        return '', ''
    try:
        response = requests.get(article_url, timeout=TIMEOUT)
        response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        print(f"请求文章 {article_url} 时发生错误：{e}")
        return '', ''

    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取文章标题
    title_tag = soup.find('h1', class_='entry-title')
    article_title = title_tag.get_text(strip=True) if title_tag else '未知标题'

    content = ''
    for p in soup.find_all('p'):
        if stop_event.is_set():
            break
        # 获取 <p> 标签内的文本，并替换 <br> 为换行符
        paragraph = p.decode_contents().replace('<br/>', '\n').replace('<br>', '\n').replace('<br />', '\n')
        # 移除可能残留的 HTML 标签
        paragraph_text = BeautifulSoup(paragraph, 'html.parser').get_text()
        content += paragraph_text + '\n'  # 每个段落后添加一个换行符

    # 删除出现的两个连续空格
    content = re.sub(r' {2}', '', content)
    # 移除不可见的 Unicode 字符
    content = remove_invisible_characters(content)
    return article_title, content.strip()

def process_category(category):
    print(f"开始处理类别：{category['name']}")
    filename = f"{category['name']}.json"

    # 打开文件，写入 JSON 数组的开头
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('[\n')

    page_number = 1
    first_entry = True  # 标志，用于处理 JSON 对象之间的逗号
    total_articles = 0  # 用于计算总文章数

    while not stop_event.is_set():
        article_links = get_article_links(category['url'], page_number)
        if not article_links:
            if page_number == 1:
                print(f"类别「{category['name']}」没有找到任何文章。")
            else:
                print(f"类别「{category['name']}」的所有页面已处理完毕。")
            break

        num_articles = len(article_links)
        total_articles += num_articles

        # 使用 tqdm 进度条
        with tqdm(total=num_articles, desc=f"类别「{category['name']}」第 {page_number} 页", unit="篇", ncols=80) as pbar:
            for article_info in article_links:
                if stop_event.is_set():
                    break
                article_url = article_info['url']
                article_title = article_info['title']
                title, content = get_article_content(article_url)
                if content:
                    # 创建 JSON 对象
                    document = {'text': content}
                    # 写入 JSON 文件
                    with open(filename, 'a', encoding='utf-8') as f:
                        if not first_entry:
                            f.write(',\n')  # 在下一个 JSON 对象前写入逗号和换行
                        else:
                            first_entry = False
                        json.dump(document, f, ensure_ascii=False)
                pbar.update(1)
        page_number += 1

    # 写入 JSON 数组的结尾
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('\n]')
    print(f"类别「{category['name']}」的数据已保存到文件 {filename}。")

def main():
    categories = get_categories()
    if not categories:
        print("未能获取任何类别，程序将退出。")
        return
    threads = []
    for category in categories:
        t = threading.Thread(target=process_category, args=(category,))
        threads.append(t)
        t.start()

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序已被用户中断，正在尝试停止所有线程...")
        stop_event.set()
        for t in threads:
            t.join()
        print("所有线程已结束，程序退出。")

if __name__ == "__main__":
    main()
