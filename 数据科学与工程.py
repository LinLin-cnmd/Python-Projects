import pyodbc
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
SELECT DISTINCT 开课课程, 课程编号,课程属性, 课程性质, 授课教师, 上课班级, 上课地点, 星期, 上课周次 FROM dbo.TC2 ORDER BY 授课教师, 星期, 上课周次
""")
result1 = cursor.fetchall()

#找出老师课程安排
t = input("输入教师名字：")
check = False
for row in result1:
    if t == row[4].split('[')[0]:
        print(f"课程：{row[0]}({row[1]})\n班级：{row[5]}\n周次/星期：{row[8]}/{row[7]}\n地点：{row[6]}\n")
        check = True
if check == False:
    print("nothing")

#找出老师空闲时间
t = input("输入教师名字：")
