import pyodbc
import re
# 连接本地SQL Server Express数据库
conn = pyodbc.connect(
    driver='ODBC Driver 17 for SQL Server',
    server='.\SQLEXPRESS',
    database='数据科学与工程',
    Trusted_Connection='yes',
    TrustServerCertificate='yes'
)

cursor = conn.cursor()
# 查询整张课表数据
table_name = 'TC2'
cursor.execute("""
SELECT DISTINCT 开课课程, 课程编号,课程属性, 课程性质, 授课教师, 上课班级, 上课地点, 星期, 上课周次, 开课时间 FROM dbo.TC2 ORDER BY 授课教师, 星期, 上课周次
""")
result1 = cursor.fetchall()

#找出老师课程安排
t = input("输入教师名字：")
check = False
for row in result1:
    if t == row[4].split('[')[0]:
        match = re.search(r'\[(.*?)\]', row[9])
        if match:
            jieci = match.group(1)
        print(f"课程：{row[0]}({row[1]})\n班级：{row[5]}\n周次/星期/节次：{row[8]}/{row[7]}/{jieci}\n地点：{row[6]}\n")
        check = True
if check == False:
    print("nothing")

#找出老师空闲时间
def parse_weeks(weeks_str):
    """解析上课周次，如 '1-16' / '1,3,5' / '1-8,10-16' -> {1,2,3,...}"""
    weeks = set()
    parts = re.findall(r'\d+-\d+|\d+', str(weeks_str))
    for part in parts:
        if '-' in part:
            s, e = map(int, part.split('-'))
            weeks.update(range(s, e + 1))
        else:
            weeks.add(int(part))
    return weeks

def parse_periods(jieci_str):
    """解析节次，如 '1-2' / '3' -> [1,2] / [3]"""
    periods = []
    parts = re.findall(r'\d+-\d+|\d+', jieci_str)
    for part in parts:
        if '-' in part:
            s, e = map(int, part.split('-'))
            periods.extend(range(s, e + 1))
        else:
            periods.append(int(part))
    return periods

t = input("输入教师名字：")
w = int(input("输入周次："))

occupied = {}  # {星期: set(已占节次)}
for row in result1:
    if t == row[4].split('[')[0]:
        weeks = parse_weeks(row[8])       # 上课周次
        if w not in weeks:
            continue
        match = re.search(r'\[(.*?)\]', row[9])
        if match:
            periods = parse_periods(match.group(1))
            day = row[7]                   # 星期
            occupied.setdefault(day, set()).update(periods)

ALL_PERIODS = set(range(1, 6))  # 一天5节课

print(f"\n{t}老师 第{w}周 空闲时间：")
for day in sorted(occupied.keys()):
    free = sorted(ALL_PERIODS - occupied[day])
    if free:
        print(f"  星期{day}：第{','.join(map(str, free))}节 空闲")
    else:
        print(f"  星期{day}：满课")
