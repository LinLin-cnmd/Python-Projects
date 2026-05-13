import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
all_university=[]

def getHtml(url):
    try:
        html = requests.get(url)
        html.raise_for_status()
        html.encoding = 'utf-8'
        print("网页提取成功！")
        return html.text
    except:
        print("网页提取失败！")
        return None

def getAllUniversity(soup):
    the_tr = soup.find_all('tr')
    for tr in the_tr:
        the_td = tr.find_all('td')
        if len(the_td) < 3:
            continue
        single_university = []
        single_university.append(the_td[0].get_text(strip=True))
        single_university.append(the_td[1].get_text(strip=True))
        single_university.append(the_td[2].get_text(strip=True))
        all_university.append(single_university)


def save_to_excel(filename="欧美高校排名.xlsx"):
    # 创建Excel工作簿
    wb = Workbook()
    ws = wb.active  # 获取默认工作表
    ws.title = "欧美高校排名"  # 工作表名称

    # 写入表头
    ws.append(["排名", "学校", "位置"])

    # 写入爬取到的数据
    for row in range(30):
        ws.append(all_university[row])

    # 保存文件
    wb.save(filename)
    print(f"Excel已保存为：{filename}（当前文件夹下）")


url = "https://www.4icu.org/us/"
html = getHtml(url)
soup = BeautifulSoup(html,"html.parser")
getAllUniversity(soup)
save_to_excel()