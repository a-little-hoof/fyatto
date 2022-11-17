##### 更新日志
##### 20220201 文本清洗，文字词云制作
##### 20220202 文字词云优化，添加停用词，表情整理及表情云制作，聊天条数统计
##### 20220203 特殊消息统计，按天按月统计聊天记录及排序，聊天字数统计
##### 20220204 特殊词统计，程序能做的事情基本结束，转战ppt
##### 20220205 折线图绘制

import re
import jieba
import matplotlib.pyplot as plt
import os

os.environ['FONT_PATH'] = 'SimHei.ttf'
# 导入字体 使wordcloud可以识别汉字
import wordcloud

new_text = []
f = open("file.txt", "r")
while True:
    line = f.readline()
    if line == "":
        break
    if line == "\n":
        continue
    str1 = line
    new_text.append(str1)
f.close()
f = open("file.txt", "w")
for i in new_text:
    f.write(i)
f.close
# 处理的txt文本 把空白行清理

##n=input("敲回车开始...")

f = open("file.txt", "r")
lines = f.read()
f.close()

join = "".join(lines)
zzr = join.count("平原不可见")
wyf = join.count("王翼飞")
print("张卓然一共说了%d句话" % zzr, end=" ")
print("王翼飞一共说了%d句话" % wyf)

##### 这段代码把readlines的列表组合成一个字符串，统计分别说了几句话

zzr_word_number = 0
wyf_word_number = 0
flagppl = 0
f = open("file.txt", "r")
while True:
    wm_line = f.readline()
    if wm_line == "":
        break
    if re.search("\d{4}-\d{2}-\d{2}", wm_line) != None:
        continue
    elif wm_line.find("王翼飞") != -1:
        flagppl = 1
    elif wm_line.find("平原不可见") != -1:
        flagppl = 0
    else:
        if flagppl:
            wyf_word_number += len(wm_line)
        else:
            zzr_word_number += len(wm_line)
f.close()
print("其中张卓然说了%d个字" % zzr_word_number, end=" ")
print("王翼飞说了%d个字" % wyf_word_number)
print("")
print("哼", end=" ")
print("也不知道谁更喜欢谁多一点")
print("")
print("不过")
print("统计的时候一个英文字母也算一个字")
print("所以这只能说明")
print("王翼飞同学更喜欢分享自己写的代码罢了")
print("")

##### 这段代码统计聊天字数

time_list = {}  # 建立字典
for i in range(0, 24):
    if i < 10:
        a = '0' + str(i)
    else:
        a = str(i)
    time_list[a] = 0
time = re.findall(r"(\d\d):\d\d", lines)  # 找所有时间，并把小时存起来
# 此处关于正则表达式的使用仍存在疑问
for j in time:
    time_list[j] += 1  # 现在time_list是一个字典，里面可以查询每小时聊天次数
for x in time_list.items():
    print("%s:00 " % x[0], "%d条" % int(x[1]))

##### 这一段代码统计各个时间段的聊天数

day_list = {}
month_list = {'09': 0, '10': 0, '11': 0, '12': 0, '01': 0, '02': 0}
date = ""
total = 0
f = open("file.txt", "r")
while True:
    dc_line = f.readline()
    if dc_line == "":
        break
    if re.search("\d{4}-\d{2}-\d{2}", dc_line) != None:
        date = (re.search("\d{4}-\d{2}-\d{2}", dc_line)).group()
        day_list[date] = 0
    elif dc_line.find("平原不可见") != -1 or dc_line.find("王翼飞") != -1:
        day_list[date] += 1
        month = date[5:7]
        month_list[month] += 1
        total += 1
    else:
        continue
f.close()
print("")
print("这期间一共发送了%d条消息" % total)
print("其中")
for x in month_list.items():  # day_list是一个字典，统计每天的聊天条数
    print("%s月" % x[0], "%d条" % x[1])
# day_list是一个字典，统计每天的聊天条数

ax = plt.figure(figsize=(30, 7), dpi=150).add_subplot()
xd = [i[5::] for i in day_list.keys()]
yd = [i for i in day_list.values()]
ax.plot(xd, yd, "blue", "chart")
plt.xticks(rotation=70)
ax.set_yticks(range(0, 300, 25))
ax.set_yticklabels([str(i) for i in range(0, 300, 25)])
plt.savefig("chart.png")

##### 把日条数画成折线图

day_list_sorted = sorted(day_list.items(), key=lambda x: x[1])
for i in range(len(day_list_sorted) - 1, len(day_list_sorted) - 4, -1):
    print(day_list_sorted[i])
# 从大到小排，选前十天
for i in range(3):
    print(day_list_sorted[i])

##### 这一段代码统计每天的聊天条数

new_text = []
special_message = []
f = open("file.txt", "r")
while True:
    line = f.readline()
    if line == "":
        break
    str2 = re.sub("王翼飞\s{2}\d{2}:\d{2}|平原不可见\s{2}\d{2}:\d{2}|—————\s{2}202\d-\d{2}-\d{2}\s{2}—————|\[.*\]", "", line)
    emojistr = re.findall("\[.+\]", line)
    special_message += emojistr
    if str2 != "\n":
        new_text.append(str2)
f.close()
f = open("blackboard.txt", "w")
for i in new_text:
    f.write(i)
f.close


##### 纯文字版与特殊消息分两个列表存放，文字存入blackboard用于词云制作

def stopwordslist():
    stopwords = [line.strip() for line in open('停用词.txt').readlines()]
    return set(stopwords)


##### 停用词，防止词云中出现的全是常用词

f = open("blackboard.txt", "r")
lines = f.read()
word_jieba = jieba.cut(lines)
stop_word = stopwordslist()
s = []
for word in word_jieba:
    if word not in stop_word:
        s.append(word)
word_split = " ".join(s)
word_split = word_split.replace("\n", "")
word_split = re.sub("\s+", " ", word_split)
w = wordcloud.WordCloud(scale=16)
w.generate(word_split)
w.to_file("python_word_cloud.png")
f.close()

##### wordcloud词云制作 去除了一些常用字

sm_str = "".join(special_message)
sm_str = sm_str.replace("]", "\n")
sm_str = sm_str.replace("[", "")
f = open("blackboard.txt", "w")
f.write(sm_str)
f.close()
f = open("blackboard.txt", "r")
emoji_cloud = ""
picture = []
music = []
left = []
app = []
card = []
phone = []
video = []
while True:
    line = f.readline()
    if line == "":
        break
    elif len(line) <= 5:
        line = line.strip()
        emoji_cloud += line
        emoji_cloud += " "
    elif line.find("图片") != -1:
        picture.append(line)
    elif line.find("音乐") != -1:
        music.append(line)
    elif line.find("应用消息") != -1:
        app.append(line)
    elif line.find("名片") != -1:
        card.append(line)
    elif line.find("实时通话") != -1:
        phone.append(line)
    elif line.find("视频") != -1:
        video.append(line)
    else:
        left.append(line)
w = wordcloud.WordCloud(scale=16)
w.generate(emoji_cloud)
w.to_file("python_emoji_cloud.png")
f.close()
print("这段时间里，我们")
print("打了%d个视频电话" % len(phone))
print("发送了%d张图片" % len(picture))
print("传输了%d个视频" % len(video))
print("分享了%d首音乐" % (len(music)))
print("使用了%d个应用" % (len(app)))
print("提及了%d张名片" % (len(card)))
print("还剩下了些奇怪的东西，我们来看看是什么")
print(left)

f = open("file.txt", "r")
spwords = f.read()
ly = spwords.count("爱你")
gn = spwords.count("晚安")
ms = spwords.count("想你")
likeyou = spwords.count("喜欢你")
ddd = spwords.count(".")
kw = spwords.count("可恶")
gs = spwords.count("高数") + spwords.count("积分") + spwords.count("线代")
mf = spwords.count("民总") + spwords.count("宪法")
f.close()
print("在这之中，我们还说了——")
print('%d句"喜欢你"' % likeyou)
print('%d句"爱你"' % ly)
print('%d句"想你"' % ms)
print('%d句"晚安"' % gn)
print('%d句"..."' % ddd)
print('%d句"可恶"' % kw)
print('提了%d句数学' % gs)
print('%d句法学' % mf)
print("我也不知道为什么要统计后面那几句，可能是因为好笑吧...")

# 写在最后：

# 以下这段话是来托底的
# 不过没关系，相信没人会认真看我的代码
# 更不会看到结尾(嘿嘿)

# 最开始产生这个想法是在知乎上看到有人做了个聊天记录年终总结。
# 我想，这或许也会是一件很非同寻常的事。
# 然而，微信的数据库有加密措施。
# 当我好不容易照着网上的教程一步一步地破解了mac上的数据库，
# 却一不小心把它们都删掉了...
# 于是我只好采取最笨的方法：
# 一步一步地勾选聊天记录-邮件发送-转为txt文本
# 不过好在python还有好多功能强大的库可用来分析文本数据
# 看网课半个月，实际操作一周，还有好多好多的时间用来debug 上网找便捷函数进行操作
# 总算有了现在这个样子
# 4个警告，61个弱警告，20个拼写错误。没错！这就是我的编程水平...
# 不过总体来说，我对这个程序还是很满意的
# 希望你也喜欢
# 生日快乐！
# 王翼飞
