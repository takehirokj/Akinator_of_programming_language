# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 17:41:48 2016

@author: Takehiro Kajihara
Guess Programming Languages in your head
"""
import pandas as pd
import time

#import graphviz
from sklearn import tree

#dot fileで指定したnodeがN回目に出た行を返す
def getLineAtNodeN(node, n):    
    i = 0
    for line in open('tree.dot'):   
        if (node + ' ') == line[0:len(node)+1]:
            i = i + 1
            if i == n:
                return line

#dot fileの中で分岐の条件を返す
def getBranchCond(inputStr):
    firstPos = line.find('"') + 1
    lastPos = line.find('gini') - 2
    if firstPos < lastPos: #葉でない場合
        return inputStr[firstPos:lastPos]
    else:
        return ''

#項目名を質門に変換する
def getQFromVar(var):
    if var == 'webDevUse':
        return 'Web開発で使われていますか?'
    elif var == 'gameDevUse':
        return 'ゲーム開発で使われていますか?'
    elif var == 'jewelyInName':
        return '名前に宝石名が含まれていますか？'
    elif var == 'scientificDataScienceUse':
        return '科学計算やデータサイエンスで使われていますか？'
    elif var == 'ObjectOriented':
        return 'オブジェクト思考言語ですか？'
    elif var == 'functionalLanguage':
        return '関数型言語ですか？'
    elif var == 'scriptingLanguage':
        return 'スクリプト言語ですか？'
    elif var == 'iOSDevUse':
        return 'iOSアプリ開発で使われていますか?'
    elif var == 'androidDevUse':
        return 'Androidアプリ開発で使われていますか?'
    elif var == 'CompanysLang':
        return '特定の企業の言語ですか?'
    elif var == 'firstAlphabetIsC':
        return 'アルファベットの1文字目はCですか?'
    elif var == 'firstAlphabetIsJ':
        return 'アルファベットの1文字目はJですか?'
    elif var == 'firstAlphabetIsP':
        return 'アルファベットの1文字目はPですか?'
    elif var == 'firstAlphabetIsR':
        return 'アルファベットの1文字目はRですか?'
    elif var == 'bornAfter2000':
        return '西暦2000年より後に作られましたか?'
    elif var == 'bornBefore1990':
        return '西暦1990年より前に作られましたか?'
    
def getNextNode(nextStr):
    firstPos = nextStr.find('>') + 2
    if nextStr.find(';') < 0:
        lastPos = nextStr.find('[')
    elif nextStr.find('[') < 0:
        lastPos = nextStr.find(';')
    else:
        lastPos = min(nextStr.find('['), nextStr.find(';'))

    lastPos = lastPos - 1
    if firstPos < lastPos:
        return nextStr[firstPos:lastPos]
    else:
        return ''

def getLangName(line):
    nVal = line[line.find('nvalue')+9:line.find('fillcolor')-3]
    nVal = nVal.replace('\\n', ', ')
    return nVal

#main 
data = pd.read_table('programmingLang.txt')
variables = ['webDevUse'
            , 'gameDevUse'
            , 'jewelyInName'
            , 'scientificDataScienceUse' 
            , 'ObjectOriented'
            , 'functionalLanguage'
            , 'scriptingLanguage'
            , 'iOSDevUse'
            , 'androidDevUse'
            , 'CompanysLang'
            , 'firstAlphabetIsC'
            , 'firstAlphabetIsJ'
            , 'firstAlphabetIsP'
            , 'firstAlphabetIsR'
            ,'bornAfter2000'
            , 'bornBefore1990']

classifier = tree.DecisionTreeClassifier()
#サンプルデータを与える。目的変数
classifier = classifier.fit(data[variables], data['Language'])

tree.export_graphviz(classifier, out_file="tree.dot"
                        , filled=True, rounded=True)
print "プログラミング言語を一つ思い浮かべてください。"
time.sleep(1.5)

node = '0'

isCont = True
while isCont:
    line = getLineAtNodeN(node, 1)
    cond = getBranchCond(line)
    if(cond == ""):
        isCont = False
        break
    else:
        cond = cond.replace('X', 'variables')
        lastPos = cond.find(']')
        cond = cond[0:lastPos+1]
        cond = eval(cond)
        question = getQFromVar(cond)
        print question + '(y/n)'
        ans = raw_input()

        if ans == 'y':
            indN = 3
        else:
            indN = 2
    
        nextStr = getLineAtNodeN(node, indN)
        node = getNextNode(nextStr)
        if(node == ""):
            isCont = False
            break
 
langLst = eval(getLangName(line))
langIdx = langLst.index(1)
print '思い浮かべている言語は ' + data['Language'][langIdx] + 'ですね。'
