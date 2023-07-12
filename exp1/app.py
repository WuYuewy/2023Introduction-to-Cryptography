import sys
import re
import string
import nltk
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MonoalphabeticCipherCracker(QWidget):

    match_dict={'a':'#','b':'#','c':'#','d':'#','e':'#','f':'#','g':'#','h':'#','i':'#','j':'#','k':'#','l':'#','m':'#','n':'#','o':'#','p':'#','q':'#','r':'#','s':'#','t':'#','u':'#','v':'#','w':'#','x':'#','y':'#','z':'#'}
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('单表代换密文破译工具')
        self.setFixedSize(1000, 800)

        # 设置字体
        font = QFont()
        font = QFont()
        font.setFamily("monospace")
        font.setPointSize(12)

        # 创建控件
        self.ciphertextLabel = QLabel('原密文：')
        self.ciphertextLabel.setFont(font)
        self.ciphertextEdit = QTextEdit()
        self.ciphertextEdit.setFont(font)
        self.ciphertextEdit.setPlaceholderText('在此处输入密文')
        self.keyLabel = QLabel('密钥字：')
        self.keyLabel.setFont(font)
        self.keyEdit = QLineEdit()
        self.keyEdit.setFont(font)
        self.keyEdit.setPlaceholderText('在此处输入密钥字（a-b）')
        self.suggestionLabel = QLabel('破译建议：')
        self.suggestionLabel.setFont(font)
        self.suggestionEdit = QTextEdit()
        self.suggestionEdit.setFont(font)
        self.suggestionEdit.setReadOnly(True)
        self.decodeLabel = QLabel('代换后：')
        self.decodeLabel.setFont(font)
        self.decodeEdit = QTextEdit()
        self.decodeEdit.setFont(font)
        self.decodeEdit.setReadOnly(True)
        self.dictionaryLabel = QLabel('代换字典：')
        self.dictionaryLabel.setFont(font)
        self.dictionaryEdit = QTextEdit()
        self.dictionaryEdit.setFont(font)
        self.dictionaryEdit.setReadOnly(True)
        self.statisticsLabel = QLabel('统计分布：')
        self.statisticsLabel.setFont(font)
        self.statisticsEdit = QTextEdit()
        self.statisticsEdit.setFont(font)
        self.statisticsEdit.setReadOnly(True)
        self.statisticsEdit.setFixedHeight(250)
        self.crackButton = QPushButton('破译')
        self.crackButton.setFont(font)
        self.crackButton.clicked.connect(self.crack)

        # 创建布局
        grid = QGridLayout()
        grid.addWidget(self.ciphertextLabel, 0, 0)
        grid.addWidget(self.ciphertextEdit, 0, 1)
        grid.addWidget(self.keyLabel, 1, 0)
        grid.addWidget(self.keyEdit, 1, 1)
        grid.addWidget(self.suggestionLabel, 2, 0)
        grid.addWidget(self.suggestionEdit, 2, 1)
        grid.addWidget(self.decodeLabel, 0, 3)
        grid.addWidget(self.decodeEdit, 0, 4)
        grid.addWidget(self.dictionaryLabel, 1, 3)
        grid.addWidget(self.dictionaryEdit, 1, 4)
        grid.addWidget(self.statisticsLabel, 2, 3)
        grid.addWidget(self.statisticsEdit, 2, 4)
        grid.addWidget(self.crackButton, 5, 0, 1, 2)

        # 设置窗口布局
        self.setLayout(grid)

    def crack(self):
        # 读取密文和密钥字
        ciphertext = self.ciphertextEdit.toPlainText().lower()
        wordlist=re.split(r' |,|;|\.|-',ciphertext)
        wordlist=[i for i in wordlist if i != '']
        text=''.join(wordlist)
        key = self.keyEdit.text().lower()
        try:
            key=key.split('-')
            assert key[0] in string.ascii_lowercase
            assert key[1] in string.ascii_lowercase
            self.match_dict[key[0]]=key[1]
        except:
            pass

        # 分析密文中每个字母的出现频率，并将结果可视化
        freq = nltk.FreqDist(text)
        self.statisticsEdit.clear()
        top_five = freq.most_common(5)
        letters = [x[0] for x in top_five]
        counts = [x[1] for x in top_five]
        fig, ax = plt.subplots()
        ax.bar(letters, counts)
        ax.set_title('Top 5 Most Frequent')
        ax.set_xlabel('Letters')
        ax.set_ylabel('Counts')
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        if self.statisticsEdit.layout() == None:
            self.statisticsEdit.setLayout(layout)

        # 进行单表代换
        decodelist=self.replace_words(wordlist, self.match_dict)
        decodetext= self.replace_string(ciphertext,self.match_dict)

        # 根据英文字母的统计分布规律和上下文给出破译建议
        suggestion = self.suggest(freq,wordlist,decodelist)
        self.suggestionEdit.setPlainText(suggestion)

        # 在字典中查找可能的单词，并将其显示在破译建议框中
        self.decodeEdit.setPlainText(decodetext)

        # 给出单表代换字典 
        dct=''
        for i in string.ascii_lowercase:
            dct+=i+' - '+self.match_dict[i]+' \n'
        dct=dct[:-1]
        self.dictionaryEdit.setPlainText(dct)

    def suggest(self,freq,wordlist,decodelist):
        # 常用单词字典
        with open('wordlist.txt', "r") as f:
            content = f.read()
            dictionary= content.split()
        letter_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z']

        suggestion=''

        suggestion+="I.词频破译建议：\n根据词频统计，有可能的单表代换对应如下：\n"
        for item in freq:
            # 在英文字母的出现频率列表中查找对应的字母
            letter = letter_freq.pop(0)
            suggestion+=(item+ ':' + letter + ';')
        
        suggestion+="\n\nII.连接特征建议："
        suggestionlist=[[],[],[],[],[]]
        suggestionword=["\n1.the（最常用三字组合）：","\n2.th（最常用二字组合）：","\n3.q后几乎百分之百连接着u：","\n4.x前几乎总是i和e：","\n5.e和e之间，r的出现频率很高："]
        for i in range(len(decodelist)):
            word=decodelist[i]
            for j in range(len(word)):
                if(word[j]=='t'and j+2<=len(word)-1 and word[j+2]=='e'):
                    suggestionlist[0].append(wordlist[i][j:j+3]+'->the;')
                if(word[j]=='t' and j!=len(word)-1):
                    suggestionlist[1].append(wordlist[i][j:j+2]+'->th;')
                if(word[j]=='q' and j!=len(word)-1):
                    suggestionlist[2].append(wordlist[i][j:j+2]+'->qu;')
                if(word[j]=='x' and j!=0):
                    suggestionlist[3].append(wordlist[i][j-1:j+1]+'->ix/ex;')
                if(word[j]=='e'and j+2<=len(word)-1 and word[j+2]=='e'):
                    suggestionlist[4].append(wordlist[i][j:j+3]+'->ere;')
        for i in range(len(suggestionlist)):
            suggestionlist[i]=list(set(suggestionlist[i]))
            suggestion+=suggestionword[i]+''.join(suggestionlist[i])

        suggestion+="\n\nIII.字典建议：\n根据词义判断，有可能的对应词对应如下："
        suggestionlist=[]
        for i in range(len(decodelist)):
            word=decodelist[i]
            for dic in dictionary:
                if(len(dic)==len(word) and self.count(dic,word)>=len(word)-1):
                    suggestionlist.append(wordlist[i]+'->'+dic+';')
        suggestionlist=list(set(suggestionlist))
        suggestion+=''.join(suggestionlist)

        return suggestion

    # 根据字典代换字符串
    def replace_string(self,s, dct):
        word=''
        for i in range(len(s)):   
            if s[i] in string.ascii_lowercase:
                word+=dct[s[i]]
            else:
                word+=s[i]
        return word

    # 根据字典代换字符列表
    def replace_words(self,lst, dct):
        decode=[]
        for i in range(len(lst)):
            word=''
            for j in range(len(lst[i])):
                if lst[i][j] in string.ascii_lowercase:
                    word+=dct[lst[i][j]]
                else:
                    word+=lst[i][j]
            decode.append(word)
        return decode

    # 统计单词之间的相似度
    def count(self,s,m):
        ct=0
        for i in range(len(s)):
            if(s[i]==m[i]):
                ct+=1
        return ct


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonoalphabeticCipherCracker()
    window.show()
    sys.exit(app.exec_())
