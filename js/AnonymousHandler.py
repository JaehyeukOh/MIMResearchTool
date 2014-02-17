# -*- coding: utf-8 -*-
'''
Created on 2013. 1. 24.

@author: return2music
'''

import os
import math
import sys
import codecs
import time
from datetime import datetime
from datetime import timedelta

class CurrentDate:
    year = 0
    month = 0
    day = 0
    def printOut(self):
        return str(self.year)+'/'+str(self.month)+'/'+str(self.day)
    
class LastItem:
    type = 0
    year = 0
    month = 0
    day = 0
    hour = 0
    min = 0
    dt = 0
    dt_str = ''
    player = ''
    playerID = 0
    content = ''
    
    def applyDate(self, currentDate):
        self.year = currentDate.year
        self.month = currentDate.month
        self.day = currentDate.day
        
        self.dt_str = str(self.year)+'-'+str(self.month)+'-'+str(self.day)+' '+str(self.hour)+':'+str(self.min)+':00'
        self.dt = datetime.strptime(self.dt_str, '%Y-%m-%d %H:%M:%S')
        
    def init(self):
        self.hour = 0
        self.min = 0
        self.player = ''
        self.playerID = 0
        self.content = ''
        
    def printOut(self):
        convertedContent = self.content.replace('0', '#').replace('1', '#').replace('2', '#').replace('3', '#').replace('4', '#')
        convertedContent = convertedContent.replace('5', '#').replace('6', '#').replace('7', '#').replace('8', '#').replace('9', '#')
        return self.dt_str+'\tP'+str(self.playerID)+'\t'+convertedContent

divisionCriteria = 90
class ClusterInfo:
    itemCnt = 0
    itemArray = 0
    def __init__(self):
        self.itemArray = []
        
    def checkIn(self, item):
        if len(self.itemArray) == 0:
            self.itemArray.append(item)
            return True
        lastdt = self.itemArray[len(self.itemArray)-1].dt
        diffdt = item.dt - lastdt
        if diffdt > timedelta(minutes=divisionCriteria):
            return False
        self.itemArray.append(item)
        return True
    
gEmoticon = '(미소)(윙크)(방긋)(반함)(눈물)(절규)(크크)(메롱)(잘자)(잘난척)(헤롱)(놀람)(아픔)(당황)(풍선껌)(버럭)(부끄)(궁금)(흡족)(깜찍)(으으)(민망)(곤란)(잠)(행복)(안도)(우웩)(외계인)(외계인녀)(공포)(근심)(악마)(썩소)(쳇)(야호)(좌절)(삐짐)(하트)(실연)(별)(브이)(오케이)(최고)(최악)(그만)(땀)(알약)(밥)(커피)(맥주)(소주)(와인)(치킨)(축하)(음표)(선물)(케익)(촛불)(컵케익a)(컵케익b)(해)(구름)(비)(눈)(똥)(근조)(딸기)(호박)(입술)(야옹)(돈)(담배)(축구)(야구)(농구)(당구)(골프)(카톡)(꽃)(총)(크리스마스)(콜)'
gEmoticon = gEmoticon.split(')(')
gEmoticon = ['('+i.replace('()','')+')' for i in gEmoticon]

class PlayerInfo:
    playerID = -1
    index = -1
    name = ''
    itemArray = 0
    leadingArray = 0
    followingArray = 0
    distanceArray = 0
    centralityValue = 0.0
    
    itemCnt = 0
    lengthPerItem = 0
    
    stickerCnt = 0
    emoticonCnt = 0
    avgStickerCnt = 0
    photoCnt = 0
    avgPhotoCnt = 0
    
    leadingCnt = 0
    avgLeadingLength = 0
    followingCnt = 0
    avgResponseTime = timedelta(minutes=0)
    avgResponseLength = 0
    
    def initClusterValue(self):
        self.leadingCnt = 0
        self.avgLeadingLength = 0
        self.followingCnt = 0
        self.avgResponseTime = timedelta(minutes=0)
        self.avgResponseLength = 0

    def printClusterValue(self):
        return str(self.leadingCnt) \
                +'\t'+str(self.avgLeadingLength)\
                +'\t'+str(self.followingCnt)\
                +'\t'+str(self.avgResponseTime)\
                +'\t'+str(self.avgResponseLength)\
                +'\t'+str(self.avgStickerCnt)\
                +'\t'+str(self.avgPhotoCnt)
            
    def __init__(self):
        self.itemArray = []
        self.leadingArray = []
        self.followingArray = []
        self.distanceArray = []
        
    def applyItem(self, item):
        result = False
        item.playerID = self.playerID
        self.name = item.player
        self.itemArray.append(item)
        
        foundEmoticon = False
        global gEmoticon
        for i in gEmoticon:
            if item.content.find(i) >= 0:
                foundEmoticon = True
                #print 'found emoticon:'+i
                break
        if foundEmoticon == True:
            item.type = 1            
            result = True
            self.emoticonCnt += 1
        if item.content.find('이모티콘') >= 0 or item.content.find('[스티커]') >= 0:
            result = True
            item.type = 2
            self.stickerCnt += 1
            #print 'found sticker:'+item.content
        if item.content == '[사진]' or item.content.find('.jpg') >= 0:
            item.type = 3            
            self.photoCnt += 1
        #print str(len(item.content.decode("utf-8")))+':'+item.content
        #print self.name + '\t' + str(len(self.itemArray))
        return result

    def calculate(self):
        self.itemCnt = len(self.itemArray)
        for item in self.itemArray:
            self.lengthPerItem += len(item.content.decode("utf-8"))
        self.lengthPerItem /= self.itemCnt
    
    def printOut(self):
        return self.name+'\t'+str(self.itemCnt)+'\t'+str(self.lengthPerItem)+'\t'+str(self.emoticonCnt)+'\t'+str(self.stickerCnt)
    
class DataHandler:
    outFILE = 0
    itemArray = []
    clusterArray = 0
    playerDic = {}
    engMode = -1
    inviteSum = 0
    leaveSum = 0
    
    def initObject(self):
        pass
    
    def initOutFILE(self, outfilename):
        if self.outFILE != 0:
            self.outFILE.close()
        self.outFILE = codecs.open(outfilename, 'w', 'utf-8')
            
    def releaseObjects(self):
        if self.outFILE != 0:
            self.outFILE.close()
    
    def outString(self, str):
        print str
        str = str + '\n'
        str = str.decode('utf-8')
        self.outFILE.write(str)

    def changeState(self, toState):
        #self.outString('pass to '+str(toState))
        self.currentState = toState
        
    def stSTART(self, key):
        if key.find('카카오톡 대화') >= 0 or key.find('KakaoTalk Chats') >= 0:
            # first line parser
            threadType = 'Kakao'
            participantPart = key.split('(')
            if len(participantPart) >= 2:
                participantCount = key.split('(')[len(participantPart)-1].split(')')[0].replace('명','').replace('People','')
                participantCount = int(participantCount) + 1
                #print f + '\t' + threadType + '\t' + str(participantCount)
            else:
                if key.find('그룹') >= 0:
                    participantCount = 0
                    #print f + '\t' + threadType + '\t' + str(participantCount)
                else:
                    participantCount = 2
                    #print f + '\t' + threadType + '\t' + str(participantCount)
            outstr = threadType +'\t' + str(participantCount)
            self.outString(outstr)
                                    
            self.changeState(self.vaLine1)
            return True
        return False
    def stLine1(self, key):
        if key.find('저장한 날짜') >= 0 or key.find('Date Saved') >= 0:
            self.outString(key)
            self.changeState(self.vaLine2)
            return True
        return False
    def stLine2(self, key):
        splitedkey = key.split(' ')
        if len(splitedkey) <= 0:
            return False # empty line
        if len(splitedkey) < 5:
            if self.engMode == -1:
                # first encountered
                if len(splitedkey)>=4 and splitedkey[0].find(',')>=0 and splitedkey[2].find(',')>=0:
                    self.engMode = 1
                    #print self.engMode
                    return False # change date
                if len(splitedkey)>=4 and splitedkey[0].find(',')>=0:
                    self.engMode = 2
                    #print self.engMode
                    return False # change date
                if len(splitedkey)>=4 and splitedkey[0].find('년')>=0 and splitedkey[1].find('월')>=0 and splitedkey[2].find('일')>=0:
                    self.engMode = 0
                    #print self.engMode
                    return False # change date
            if self.engMode == 1:
                if len(splitedkey)>=4 and splitedkey[0].find(',')>=0 and splitedkey[2].find(',')>=0:
                    return False # change date
            if self.engMode == 2:
                if len(splitedkey)>=4 and splitedkey[0].find(',')>=0:
                    return False # change date
            else:
                if len(splitedkey)>=4 and splitedkey[0].find('년')>=0 and splitedkey[1].find('월')>=0 and splitedkey[2].find('일')>=0:
                    return False # change date
            self.lastItem.content += key
            return False # con't content
        
        if self.engMode == 1:
            if splitedkey[1].find(',')<0 or splitedkey[2].find(',')<0 or splitedkey[3].find(':')<0:
                self.lastItem.content += key
                return False # con't content
        elif self.engMode == 2:
            if splitedkey[3].find(':')<0:
                self.lastItem.content += key
                return False # con't content
        else:
            if splitedkey[0].find('년')<0 or splitedkey[1].find('월')<0 or splitedkey[2].find('일')<0:
                if splitedkey[0].find('.')<0 or splitedkey[1].find('.')<0 or splitedkey[2].find('.')<0:
                    self.lastItem.content += key
                    return False # con't content

        inviteCnt = 0
        leaveCnt = 0
        playername = ''
        playerindex = 0
        playerfound = False
        if self.engMode == 2:
            if splitedkey[3].find(':') < 0 and splitedkey[3].find(',') < 0:
                return False # datetime only
            for item in splitedkey[4:]:
                if item.find(':') >= 0:
                    playerfound = True
                    break
                playername += item+' '
                playerindex += 1
            if playerfound == False:
                fromCnt = key.count('님이')
                targetCnt = key.count('님과') + key.count('님,') + key.count('님을')
                inviteCnt = key.count('초대') + key.count('invite')
                leaveCnt = key.count('퇴장') + key.count('left')
                if inviteCnt == 1:
                    self.inviteSum += targetCnt
                if leaveCnt == 1:
                    self.leaveSum += fromCnt
                if (inviteCnt == 0 and leaveCnt == 0):
                    outstr = str(fromCnt)+':'+str(targetCnt)+':'+str(inviteCnt)+':'+str(leaveCnt)+':'+key
                    print outstr
        else:            
            if splitedkey[4].find(':') < 0 and splitedkey[4].find(',') < 0:
                return False # datetime only
            for item in splitedkey[5:]:
                if item.find(':') >= 0:
                    playerfound = True
                    break
                playername += item+' '
                playerindex += 1
            if playerfound == False:
                fromCnt = key.count('님이')
                targetCnt = key.count('님과') + key.count('님,') + key.count('님을')
                inviteCnt = key.count('초대') + key.count('invite')
                leaveCnt = key.count('퇴장') + key.count('left')
                if inviteCnt == 1:
                    self.inviteSum += targetCnt
                if leaveCnt == 1:
                    self.leaveSum += fromCnt
                if (inviteCnt == 0 and leaveCnt == 0):
                    outstr = str(fromCnt)+':'+str(targetCnt)+':'+str(inviteCnt)+':'+str(leaveCnt)+':'+key
                    #print outstr
                    return False
        try:   
            if splitedkey[6+playerindex].find('<사진') >= 0 and splitedkey[6+playerindex+1].find('읽지') >= 0 and splitedkey[6+playerindex+2].find('않음>') >= 0:
                return False
        except:
            pass
        
        # content start
        self.updateLastItem()
        if self.engMode == 1:
            self.currentDate.year = splitedkey[2].replace(',', '')
            self.currentDate.day = splitedkey[1].replace(',', '')
            monthAbbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            self.currentDate.month = 0
            for i, s in enumerate(monthAbbr):
                if splitedkey[0] in s:
                    #print splitedkey[0] + ':' + str(i)
                    self.currentDate.month = i+1
                    break
                
            curTime = splitedkey[3].split(':')
            self.lastItem.hour = int(curTime[0])
            self.lastItem.min = int(curTime[1])
            if splitedkey[4] == 'AM,' and self.lastItem.hour >= 12:
                self.lastItem.hour -= 12
            if splitedkey[4] == 'PM,' and self.lastItem.hour < 12:
                self.lastItem.hour += 12
        elif self.engMode == 2:
            self.currentDate.year = splitedkey[2].replace(',', '')
            self.currentDate.day = splitedkey[0].replace(',', '')
            monthAbbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            self.currentDate.month = 0
            for i, s in enumerate(monthAbbr):
                if splitedkey[1] in s:
                    #print splitedkey[0] + ':' + str(i)
                    self.currentDate.month = i+1
                    break
                
            curTime = splitedkey[3].split(':')
            self.lastItem.hour = int(curTime[0].replace(',',''))
            self.lastItem.min = int(curTime[1].replace(',',''))
        else:
            if splitedkey[0].find('년')>=0 and splitedkey[1].find('월')>=0 and splitedkey[2].find('일')>=0:
                self.currentDate.year = splitedkey[0].replace('년', '')
                self.currentDate.month = splitedkey[1].replace('월', '')
                self.currentDate.day = splitedkey[2].replace('일', '')
            elif splitedkey[0].find('.')>=0 and splitedkey[1].find('.')>=0 and splitedkey[2].find('.')>=0:
                self.currentDate.year = splitedkey[0].replace('.', '')
                self.currentDate.month = splitedkey[1].replace('.', '')
                self.currentDate.day = splitedkey[2].replace('.', '')            
                
            curTime = splitedkey[4].replace(',', '').split(':')
            self.lastItem.hour = int(curTime[0])
            self.lastItem.min = int(curTime[1])
            if splitedkey[3] == '오전' and self.lastItem.hour >= 12:
                self.lastItem.hour -= 12
            if splitedkey[3] == '오후' and self.lastItem.hour < 12:
                self.lastItem.hour += 12
        
        if inviteCnt >= 1:
            self.lastItem.type = 10
            self.lastItem.content = '[초대]'
            self.lastItem.applyDate(self.currentDate)
            self.itemArray.append(self.lastItem)
            self.lastItem = LastItem()            
        elif leaveCnt >= 1:
            self.lastItem.type = 10
            self.lastItem.content = '[퇴장]'
            self.lastItem.applyDate(self.currentDate)
            self.itemArray.append(self.lastItem)
            self.lastItem = LastItem()            
        else:    
            #        
            self.lastItem.player = playername
            keycontent = '' # splitedkey 7 ~
            if self.engMode == 2:
                contentIndex = 5+playerindex
            else:
                contentIndex = 6+playerindex
                
            for item in splitedkey[contentIndex:]:
                keycontent += item+' '
            self.lastItem.content = keycontent
        
        return True

    def updateLastItem(self):
        if len(self.lastItem.content) == 0:
            return
        #self.outString(self.currentDate.printOut()+' '+self.lastItem.printOut())
        self.lastItem.applyDate(self.currentDate)
        self.itemArray.append(self.lastItem)
        self.lastItem = LastItem()
        
    vaSTART = 0
    vaLine1 = 1
    vaLine2 = 2
    
    states = {vaSTART:stSTART,
              vaLine1:stLine1,
              vaLine2:stLine2}
    currentState = vaSTART
    currentDate = CurrentDate()
    lastItem = LastItem()
    currentCluster = 0
    front_threadID = ''
    
    def manipulateData(self, threadID, targetfilename, outfilename, outname2):
        self.itemArray = []
        self.clusterArray = 0
        self.playerDic = {}
        self.currentState = self.vaSTART
        self.currentDate = CurrentDate()
        self.lastItem = LastItem()
        self.currentCluster = 0

        FILE = open(targetfilename, 'r')
        self.initOutFILE(outfilename)
        count = 0
        while True:
            key = FILE.readline()
            multiline = key.split('\n')
            #print str(count) + ':' + str(len(multiline))
            count += 1
            if not key:
                #print 'eof'
                self.updateLastItem()
                break 
            key = key.replace('\n', '').replace('\r', '')
            if len(key) == 0:
                continue
            #print str(len(key)) + ':' + key
            self.states[self.currentState](self, key)
        FILE.close()
               
        #self.outString(self.itemArray[0].dt_str)
        #self.outString(self.itemArray[len(self.itemArray)-1].dt_str)
        lastPlayerID = 0
        for item in self.itemArray:
            # check player
            try:
                if item.type != 10:
                    targetPlayer = self.playerDic[item.player]
                    if targetPlayer.applyItem(item) == True:
                        #self.outString(item.printOut())
                        pass
            except:
                targetPlayer = PlayerInfo()
                targetPlayer.playerID = lastPlayerID
                lastPlayerID += 1
                self.playerDic[item.player] = targetPlayer
                #self.outString('new player was appeared:'+item.printOut())
                if targetPlayer.applyItem(item) == True:
                    #self.outString(item.printOut())
                    pass
                #print item.player

        for item in self.itemArray:
            self.outString(item.printOut())
        # print out
               
                          
class LineDataHandler:
    outFILE = 0
    itemArray = []
    clusterArray = 0
    playerDic = {}
    inviteSum = 0
    leaveSum = 0
    front_threadID = ''
    
    def initObject(self):
        pass
    
    def initOutFILE(self, outfilename):
        if self.outFILE != 0:
            self.outFILE.close()
        self.outFILE = codecs.open(outfilename, 'w', 'utf-8')
            
    def releaseObjects(self):
        if self.outFILE != 0:
            self.outFILE.close()
    
    def outString(self, str):
        print str
        str = str + '\n'
        str = str.decode('utf-8')
        self.outFILE.write(str)    
    
    def changeState(self, toState):
        #self.outString('pass to '+str(toState))
        self.currentState = toState
        
    def stSTART(self, key):
        if key.find('[LINE]') >= 0 or key.find('[라인]')>=0:
            threadType = 'LINE'
            if key.find('그룹') >= 0:
                participantCount = 0
            else:
                participant = key.count(',')
                participantCount = participant+2
            self.outString(threadType+'\t'+str(participantCount))

            self.changeState(self.vaLine1)
            return True
        return False
    def stLine1(self, key):
        if key.find('저장일시') >= 0 or key.find('저장 시간') >= 0:
            self.outString(key)            
            self.changeState(self.vaLine2)
            return True
        return False
    def stLine2(self, key):
        tokens = key.replace('.', '').split(' ')
        if len(tokens) == 4:
            self.updateLastItem()
            self.currentDate.year = tokens[0]
            self.currentDate.month = tokens[1]
            self.currentDate.day = tokens[2]
            #self.outString('change date to '+str(self.currentDate.year)+str(self.currentDate.month)+str(self.currentDate.day))
            self.changeState(self.vaChangeDate)
            return True    

        tokens = key.replace('(', '/').split('/')
        if len(tokens) == 4:
            self.updateLastItem()
            self.currentDate.year = tokens[0]
            self.currentDate.month = tokens[1]
            self.currentDate.day = tokens[2]
            #self.outString('change date to '+str(self.currentDate.year)+str(self.currentDate.month)+str(self.currentDate.day))
            self.changeState(self.vaChangeDate)
            return True    
                         
        return False

    def stChangeDate(self, key):
        # to item
        key = key.split('\t')
        if len(key) < 3:
            return False
        # check time
        curTime = key[0].split(':')
        if len(curTime) != 2:
            return False
        
        self.updateLastItem()
        
        # check leave player
        if len(key) == 2:
            return True
        self.lastItem.hour = curTime[0]
        if self.lastItem.hour == '24':
            self.lastItem.hour = '00'
        self.lastItem.min = curTime[1]
        self.lastItem.player = key[1]
        self.lastItem.content = key[2]
        self.changeState(self.vaItem)
        return True
    def stItem(self, key):
        # to change date
        chk = key.replace('.', '').split(' ')
        try:
            year = int(chk[0])
        except:
            year = 0
        if len(chk) == 4 and year>=2000 and year<=3000:
            return self.stLine2(key)

        chk = key.replace('(', '/').split('/')
        try:
            year = int(chk[0])
        except:
            year = 0
        if len(chk) == 4 and year>=2000 and year<=3000:
            return self.stLine2(key)
        
        # to item
        chk = key.split('\t')
        if len(chk) >= 3:
            return self.stChangeDate(key)
                
        if len(chk) == 2:
            # 그룹에 참여합니다.
            # 그룹사진을 변경하였습니다.
            # 그룹에서 나갔습니다.
            # 초대했습니다.
            # 변경했습니다.
            fromCnt = key.count('님이')
            targetCnt = key.count('님을')
            inviteCnt = key.count('참여합니다')
            leaveCnt = key.count('나갔습니다') + key.count('탈퇴시켰습니다')
            if inviteCnt == 1:
                self.inviteSum += 1
            if leaveCnt == 1:
                self.leaveSum += 1
            if (inviteCnt == 0 and leaveCnt == 0):
                outstr = str(fromCnt)+':'+str(targetCnt)+':'+str(inviteCnt)+':'+str(leaveCnt)+':'+key
                #print outstr
                
            key = key.split('\t')
            curTime = key[0].split(':')
            self.lastItem.hour = curTime[0]
            if self.lastItem.hour == '24':
                self.lastItem.hour = '00'
            self.lastItem.min = curTime[1]
            self.lastItem.applyDate(self.currentDate)
            content = key[1]

            if inviteCnt >= 1:
                self.lastItem.type = 10
                self.lastItem.content = '[초대]'
                self.lastItem.applyDate(self.currentDate)
                self.itemArray.append(self.lastItem)
                self.lastItem = LastItem()            
            elif leaveCnt >= 1:
                self.lastItem.type = 10
                self.lastItem.content = '[퇴장]'
                self.lastItem.applyDate(self.currentDate)
                self.itemArray.append(self.lastItem)
                self.lastItem = LastItem()            

            #print self.lastItem.dt_str + ':' +content
            return True   
        # to next line
        self.lastItem.content += key
        return True
    def updateLastItem(self):
        if len(self.lastItem.content) == 0:
            return
        #self.outString(self.currentDate.printOut()+' '+self.lastItem.printOut())
        self.lastItem.applyDate(self.currentDate)
        self.itemArray.append(self.lastItem)
        self.lastItem = LastItem()
        
    vaSTART = 0
    vaLine1 = 1
    vaLine2 = 2
    vaChangeDate = 3
    vaItem = 4
    
    states = {vaSTART:stSTART,
              vaLine1:stLine1,
              vaLine2:stLine2,
              vaChangeDate:stChangeDate,
              vaItem:stItem}
    currentState = vaSTART
    currentDate = CurrentDate()
    lastItem = LastItem()
    currentCluster = 0

    def manipulateData(self, threadID, targetfilename, outfilename, outname2):
        FILE = open(targetfilename, 'r')
        self.initOutFILE(outfilename)
        while True:
            key = FILE.readline()
            if key == '':
                break 
            key = key.replace('\n', '').replace('\r', '')
            self.states[self.currentState](self, key)
        FILE.close()
        self.lastItem.applyDate(self.currentDate)
        self.itemArray.append(self.lastItem)        
        
        lastPlayerID = 0
        for item in self.itemArray:
            # check player
            try:
                if item.type != 10:
                    targetPlayer = self.playerDic[item.player]
                    if targetPlayer.applyItem(item) == True:
                        #self.outString(item.printOut())
                        pass
            except:
                targetPlayer = PlayerInfo()
                targetPlayer.playerID = lastPlayerID
                lastPlayerID += 1
                self.playerDic[item.player] = targetPlayer
                #self.outString('new player was appeared:'+item.printOut())
                if targetPlayer.applyItem(item) == True:
                    #self.outString(item.printOut())
                    pass
                #print item.player

        for item in self.itemArray:
            self.outString(item.printOut())
                            
def main():
    path_str = sys.argv[1]
    name_str = sys.argv[2]
    #path_str = './data/'
    #name_str = 'KakaoThread7.txt'
    targetfilename = path_str+name_str
    
    FILE = open(targetfilename, 'r')
    firstline = FILE.readline()
    FILE.close()

    if firstline is None:
        os.remove(targetfilename)
        return
        
    threadID = name_str.split('.')[0]
    if firstline.find('카카오톡 대화')>=0 or firstline.find('KakaoTalk Chats')>=0:
        mainClass = DataHandler()
        mainClass.initObject()
        mainClass.manipulateData(threadID, path_str+name_str, path_str+'out_'+name_str, path_str+'out2_'+name_str)
        mainClass.releaseObjects()
    elif firstline.find('[LINE]')>=0 or firstline.find('[라인]')>=0:
        mainClass = LineDataHandler()
        mainClass.initObject()
        mainClass.manipulateData(threadID, path_str+name_str, path_str+'out_'+name_str, path_str+'out2_'+name_str)
        mainClass.releaseObjects()
    os.remove(targetfilename)
    
if __name__ == '__main__':
    main()