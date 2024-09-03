import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re
import urllib.parse
import time
import json
import os
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

# 禁用InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 名字列表
names = ["精选作品", "现代情色", "日本情色", "西洋情色", "伴侣交换", "武侠情色", "奇幻科幻", "家庭乱伦", "性爱调教", "粗野性交", "多人群交", "教师学生", "古典情色", "历史情色", "同性情色", "都市生活", "乡间记趣", "疯狂暴 露", "午夜怪谈", "游戏乐园", "医生护士", "奇遇物语", "左邻右舍", "同事之间", "旅游纪事", "纯洁恋情", "明星系列", "意外收获", "忘年之乐", "另类其他", "知识技巧", "文学评论", "经典激情", "近亲乱伦", "人妻美妇", "学生校园", "职业制服", "粗暴性爱", "情色武侠", "情欲性爱", "长篇小说", "中篇小说", "作家专栏", "全部分类", "文学评论", "十大经典", "年度总结", "文学百科", "文 学分类", "十大作品", "十年回顾", "玄幻文学", "情色研究", "长篇情色小说（三万七千一百章）", "热门小说", "少年阿宾", "少妇白 洁", "风水相师", "姐夫荣耀", "朱颜血", "锁情咒", "淫奇抄", "都市偷香", "小村春色", "小镇情欲", "作家专栏", "全部小说", "通 俗小说", "梦中女孩", "舌战法庭", "夜色上海", "人在深圳", "白领丽人", "绝色肉欲", "往事追忆", "校园追艳", "小青情人", "出差", "少年阿宾", "金鳞岂是", "少妇孙倩", "少妇张敏", "少妇白洁", "天地之间", "官道仕途", "游龙嬉春", "男人", "再世情仇", "我和妹妹", "小青自白", "小青故事", "阿庆淫传", "小芳童话", "后宫学园", "清茗学院", "同级生", "大学刑法", "国中理化", "执子之手", "少妇之心", "欲望之门", "绯色官途", "舞艺附中", "官能", "都市小说", "风水相师", "魔鬼老师", "风流教师", "姐夫荣耀", "天使", "小村春色", "小镇情欲", "渔港春夜", "春乱香野", "密诱", "乡野痞医", "天堂之路", "春光无限", "医者风流", "地狱门", "春满 香夏", "田野花香", "妇科男医", "风流法医", "医色生香", "画魂", "二号首", "锁情咒", "西苑魅影", "纹面", "琳海雪原", "降头师", "绳师", "潜规则", "欲海沉沦", "畸爱博士", "荡妇笔记", "难知如阴", "大丑风流", "左手天堂", "食色男女", "都市情侠", "噬梦者", "聪明玲莉", "娇妻爱女", "彼岸山庄", "校长生涯", "银行少妇", "导火线", "神罚之城", "修罗都市", "猎美淫术", "废都", "官场 情人", "淫奇系列", "幻情系列", "轻歌系列", "都市偷香", "乱欲利娴", "蜜桃臀", "贵妇圈", "武侠小说", "玉女盟", "风尘劫", "采 花行", "十景缎", "照日天劫", "骆冰淫传", "俪影蝎心", "玲珑孽怨", "逍遥小散", "江山多娇", "妖刀记", "如影逐形", "玄媚剑", " 冷香谷", "魔女天娇", "四海龙女", "江湖", "平妖传", "香艳杀劫", "逆侠", "魔刀丽影", "狂剑风流", "剑起云深", "梦回天阙", "散 花天女", "成龙记", "修罗劫", "擎羊舞风", "逆天邪传", "魔尊曲", "沧澜曲", "猎艳江湖", "游龙传", "暗夜情魔", "剑指天下", "武 林启示", "一代大侠", "暮霭凝香", "血雨沁芳", "窃玉", "琼明神女", "豪侠绿传", "浪情侠女", "鹰翔长空", "神斧英雄", "云舞月扬", "江山风月", "奇侠斗女", "鱼龙舞", "段家女将", "骄龙荡魔", "武林艳史", "如意楼", "惊尘溅血", "红映残阳", "菊隐云香", "东方云梦", "浑沌无极", "龙魂侠影", "侠女悲哀", "奇幻小说", "黑星女侠", "魔王重生", "肉棒公主", "阿里布达", "风月大陆", "龙战士", "淫术炼金", "骑士血脉", "九流术士", "睡着武神", "黑天使", "仙侠魔踪", "我的天下", "荒唐大帝", "龙血战士", "龙使", "美人图", "女神诡计", "拉里传奇", "龙宠", "妙手神织", "日出之王", "黑帝猎艳", "绝代艳修", "皇朝秘史", "降仙奇缘", "翼图卷宗", "仙 童地狱", "永恒国度", "天外邪犽", "炼金玛莉", "艳法战", "苍主", "大隐", "恶魔养殖", "堕落天使", "娘子军", "征神领域", "战乱 星系", "博康舒大", "黑魔公主", "驱妖娘娘", "妖淫剑姬", "魔甲销魂", "小人国", "血魔夜宴", "极道风流", "克里斯蒂", "神雕风流", "神魔都市", "海盗悠闲", "都市大巫", "艳修天地", "异世商业", "魔神再临", "逆玉王", "冒险小说", "炼狱天使", "艳兽都市", "肉体买家", "帝王本色", "限制特工", "女校先生", "听雪谱", "嗜血魔徒", "堕落之王", "绝色保镖", "烈火凤凰", "龙欲都市", "淫龙出 穴", "屌男复仇", "少龙传奇", "末日狂欢", "玫瑰劫", "黑欲归龙", "猎情", "王牌特工", "失贞都市", "灰色系列", "云别传", "乱游 记", "穿越小说", "六朝云龙", "六朝清羽", "西游艳记", "红楼遗秘", "圣女修道", "横行天下", "天魔", "流氓大地", "盛世王朝", " 狡猾家丁", "邪器", "我最逍遥", "亡灵沸腾", "女皇保卫", "江山绝色", "后宫佳丽", "诱红楼", "附体记", "无齿僵尸", "欲望传说", "黑暗小说", "永堕黑暗", "现代淫魔", "黑暗天使", "护士淫梦", "新任英语", "欲海情魔", "高树三姐", "胸大有罪", "冰峰魔恋", "恶欲之源", "终生性奴", "少妇哀羞", "调教女友", "女文工团", "女公务员", "女警传说", "朱颜血", "缚美传", "折翼天使", "魔辱之馆", "言情小说", "情欲乐园", "激情狂想", "神秘之河", "不做淑女", "蛮荒之吻", "珠宝魅力", "欲望俘虏", "风流骑士", "情网", "猎艳", "卡桑德拉", "意大利来", "帕尔米拉", "爱奴", "体热", "塞雷娜歌", "繁體小說", "简体小说", "经典小说"]

# 基础URL
base_url = "https://blog.xbookcn.net/search/label/"
max_results = 20  # 每次请求的最大结果数

# 设置重试策略
session = requests.Session()
retry = Retry(connect=5, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

def clean_html(raw_html):
    """移除HTML标签并在特定位置替换为'\n'字符。"""
    clean_text = re.sub(r'</p>\s*<p>', r'\n', raw_html)  # 使用真正的换行符
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def fetch_post_content(post_url, json_filename):
    """获取单个文章的标题和内容，保存到对应的JSON文件中。"""
    try:
        response = session.get(post_url, timeout=10, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('h3', class_='post-title entry-title')
            title = title_tag.get_text(strip=True) if title_tag else '无标题'
            content_div = soup.find('div', class_='post-body entry-content')
            if content_div:
                for p in content_div.find_all('p'):
                    if '作者：' in p.get_text():
                        p.decompose()
                raw_content = str(content_div)
                clean_content = clean_html(raw_content)
                # 组合结果
                result = {"text": f"{title}\n{clean_content}"}
                
                # 将内容追加写入 JSON 文件
                with open(json_filename, 'a', encoding='utf-8') as json_file:
                    json.dump(result, json_file, ensure_ascii=False, indent=2)
                    json_file.write(',\n')
                
                print(f"已写入 {title}")
        else:
            print(f"无法获取文章内容：{post_url}，状态码：{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求文章内容时出错：{post_url}，错误信息：{e}")

def load_all_content(encoded_name, json_filename, max_results):
    """持续加载内容直到没有更多的新内容。"""
    start_index = 0
    while True:
        url = f"{base_url}{encoded_name}?start={start_index}&max-results={max_results}"
        try:
            response = session.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                post_links = soup.find_all('h3', class_='post-title entry-title')
                if not post_links:
                    break  # 没有更多文章，退出循环
                for post_link in post_links:
                    link_tag = post_link.find('a')
                    if link_tag and 'href' in link_tag.attrs:
                        post_url = link_tag['href']
                        fetch_post_content(post_url, json_filename)
                        time.sleep(1.5)  # 避免请求过于频繁，延迟1.5秒
                if len(post_links) < max_results:
                    break  # 已经是最后一页，退出循环
                start_index += max_results  # 更新起始索引
            else:
                print(f"无法加载内容，状态码：{response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"请求内容时出错：{url}，错误信息：{e}")
            break

def fetch_links_and_contents(name):
    """主函数，负责根据标签名称获取所有文章内容，并逐一写入JSON文件。"""
    encoded_name = urllib.parse.quote(name)
    json_filename = f"{name}.json"
    
    # 创建文件并写入开头的方括号，表示JSON数组的开始
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json_file.write('[')
    
    # 加载并处理所有内容
    load_all_content(encoded_name, json_filename, max_results)
    
    # 文件末尾处理，将最后一个逗号去除并关闭JSON数组
    with open(json_filename, 'rb+') as json_file:
        json_file.seek(-2, os.SEEK_END)  # 移动到倒数第二个字符
        json_file.truncate()  # 移除最后的逗号
        json_file.write(b'\n]')  # 添加闭合方括号和换行符

    print(f"{json_filename} 已完成写入。")

def main():
    executor = None  # 初始化 executor
    try:
        executor = ThreadPoolExecutor(max_workers=3)  # 最多3个线程同时执行
        futures = [executor.submit(fetch_links_and_contents, name) for name in names]
        for future in as_completed(futures):
            future.result()  # 等待线程完成并获取结果
    except KeyboardInterrupt:
        print("程序被手动中断。正在退出...")
    finally:
        if executor:
            executor.shutdown(wait=True)  # 等待所有线程完成

if __name__ == "__main__":
    main()
