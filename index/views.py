from django.shortcuts import render
from .models import Dialog
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from googletrans import Translator
import sqlite3
import math

globalvar=None
globalvarcol=None
clientName=None
clientNameSearch=False
globaltofind=[]
globalfromfind=[]

def generateQuery(query):
    if(query=='धन्यवाद' or query=='शुक्रिया' or query=='थैंक यू सो मच' or query=='थैंक यू' or query=='थैंक्स'):
        return('इस सुविधा का उपयोग करने के लिए धन्यवाद')
    global clientName
    global clientNameSearch
    global globaltofind
    global globalfromfind
    print(clientNameSearch,clientName,globaltofind,globalfromfind)
    translator = Translator()
    where=('जो','जिनका','जिनके','जिनकी','जिनको','जिसका','जिसके','जिसकी','जिसने','जिसको','जिन्हें','जिन्होंने','किसका','किसकी','किसने','जिस','किस','किसके','जिसमें','जिसमे')
    count=('कितना','कितनी','कितने','कितनों','कोई')
    client=('मेरा','मेरी','मैंने','हमारा','हमारी','हमने','हम','हमको','हमें')
    maxm=('सबसे ज्यादा',)
    minm=('सबसे कम',)
    subject=('इनका','उनका','इसका','उसे','उसका','उसको','इनके','उनके','उसने','इसके','इन्होंने','उन्होंने','उसके','उसमें','उसमे','इनकी','उनकी','इसकी','उसकी','यह','वह','इस','उस','ये','वो')
    kalist=('इनका','उनका','इसका','उसका','इनके','उनके','उसको','इसके','उसके','इनकी','उनकी','इसकी','उसकी','का','की','के')
    tofindvarlist=('जो','जिसने','जिस','जिन्होंने')
    tofindlist=('कौन','कौनसी','किसने','क्या','बताइए','बता','मिल')
    who=('कौन','कौनसी','कौन-कौन')
    words=('कब','कहाँ','कहां','का','की','किया','था','थे','कि','के','को','है','हैं','था','टोटल','कुल','मिलाकर','या','सब','से','लिए','गई','वाली','वाले','में','थी','लाइब्रेरी','धन्यवाद','और','सारी','क्या','सकता','नाम','मिलेगा','आप','बता','सकते','सकती','जानकारी','मिलेगी','मिल','हो','बताइए','बताइये','दीजिए','किसी','ने','कराई','सी','घर')
    nonNoun={'where':where,'count':count,'client':client,'max':maxm,'min':minm,'subject':subject,'who':who,'words':words}
    queryfunNoun={'where':where,'count':count,'client':client,'max':maxm,'min':minm}
    code=('कोड','कोड नंबर','CODE','CODE NUMBER','CODE NO','CODE NO.')
    classNo=('क्लास','क्लास नंबर','CLASS','CLASS NO','CLASS NUMBER','CLASS NO.')
    title=('बुक','किताब','पुस्तक','किताबों','पुस्तकों','किताबें','पुस्तकें','BOOK','BOOKS','टाइटल','TITLE')
    author=('ऑथर','राइटर','लेखक','लेखकों','लिखा','लिखी','AUTHOR','WRITER')
    publication=('पब्लिकेशन','publication')
    collation=('पेजेज','पन्ने','पेज','collation','PAGE','PAGES')
    series=('सीरीज','SERIES')
    tofind=('कौन','कोई','कहां','कहाँ','कब','कौनसी','कौन-कौन','कितना','कितनी','कितने','किसने','क्या','किस','बताइए','बताइये','बता','मिल')
    noofCopy=('कॉपी','कॉपियां','नंबर ऑफ कॉपी', 'COPY', 'COPIES', 'NUMBER OF COPIES', 'NUMBER OF COPY')
    keywords=('रिलेटेड','RELATED','तरह')
    accessionNo=('एक्शन नंबर','अक्सेशन नंबर','ACCESSION NO.','ACCESSION NO','ACCESSION NUMBER')
    edition=('एडिसन','एडिशंस','एडिशन','एडिशन्स','EDITION','EDITIONS')
    price=('दाम','प्राइस','कॉस्ट','PRICE','COST')
    reservedNo=('रिजर्व नहीं','रिज़र्व नहीं','रिजर्व्ड नहीं','रिजल्ट नहीं')
    reservedYes=('रिजर्व','रिज़र्व','रिजर्व्ड','रिजल्ट','RESERVE','RESERVED')
    status=('स्टेटस','अवेलेबल','मिसिंग','रिकवर','राइट ऑफ','STATUS','AVAILABLE','MISSING','RECOVER','RECOVERED','WRITE OFF')
    statusDict={'status':['स्टेटस','STATUS'],'Available':['अवेलेबल','AVAILABLE'],'Issued':[],'Missing':['मिसिंग','MISSING'],'Recovered':['रिकवर','RECOVER','RECOVERED'],'Writeoff':['राइट ऑफ','WRITE OFF']}
    shelfNo=('सेल्फ','जगह','पर','पे','SHELF','SHELF NUMBER','SHELF NO','SHELF NO.')
    lastIssue=('इशू','यीशु','ISSUED','ISSUE','लास्ट','LAST','लास्ट इशू','लास्ट यीशु','LAST ISSUE')
    IssueDate=('ड्यू डेट','इशू डेट','यीशु डेट','ISSUE DATE','लास्ट इशू डेट','लास्ट यीशु डेट','LAST ISSUE DATE')
    memberCode=('मेंबर कोड','मेंबर ID','MEMBER CODE','MEMBER ID')
    memberName=('मेंबर','मेंबर नेम','MEMBER','MEMBER NAME')
    fatherName=('फादर','पिता','पिताजी','बाप','FATHER')
    socialCategory=('कैटेगरी','केटेगरी','जाति','कास्ट','CATEGORY','CASTE')
    designation=('डेसिग्नेशन','देसिग्नेशन','पोस्ट','DESIGNATION','POST')
    groupCode=('ग्रुप कोड','ग्रुप','ग्रुप ID','GROUP','GROUP CODE','GROUP ID')
    joiningDate=('जोइनिंग डेट','जॉइन','ज्वाइन','JOIN','JOINING DATE')
    address=('पता','एड्रेस','एड्रेस','ADDRESS')
    phoneNo=('फ़ोन नंबर','फोन नंबर','कांटेक्ट नंबर','PHONE NO','CONTACT NO','PHONE NO.','CONTACT NO.','PHONE NUMBER','CONTACT NUMBER')
    eMail=('मेल ID','ईमेल ID','ईमेल','ईमेल एड्रेस','EMAIL','EMAIL ID','EMAIL ADDRESS')
    dues=('ड्यूस','डीयू','ड्यूश','ड्यू ','DUES','DUE','DEW','DEWS','DUECE')
    book={'code':code,'classNo':classNo,'title':title,'author':author,'publication':publication,'collation':collation,'series':series,'noofCopy':noofCopy,'keywords':keywords}
    bookcopy={'accessionNo':accessionNo,'edition':edition,'price':price,'reservedYes':reservedYes,'reservedNo':reservedNo,'c.status':status,'shelfNo':shelfNo,'lastIssue':lastIssue,'IssueDate':IssueDate}
    member={'memberCode':memberCode,'memberName':memberName,'fatherName':fatherName,'socialCategory':socialCategory,'designation':designation,'groupCode':groupCode,'joiningDate':joiningDate,'addressLocal,addressHome':address,'phoneNo':phoneNo,'eMail':eMail,'dues':dues}   
    queryfun = []
    queryfunwords=[]
    visited=[]
    fromvar=''
    tofindvar=''
    fromstatusvar=''
    bookcopySearch=True
    bookTable=False
    bookcopyTable=False
    memberSearch=True
    memberTable=False
    for i in queryfunNoun:
        queryfunwords.extend(queryfunNoun[i])
    columns=[]
    for i in book:
        columns.extend(book[i])
    for i in bookcopy:
        columns.extend(bookcopy[i])
    for i in member:
        columns.extend(member[i])
    nonNounWords=[]
    for i in nonNoun:
        nonNounWords.extend(nonNoun[i])
    keywordings=list(query.split())
    nouns=[]
    trans=[]
    col=[]
    col1=[]
    col2=[]
    netcol=[]
    statusval=[]
    tofindcol=[]
    fromfindcol=[]
    it=[]
    fromfindvar2=''
    fromfindval2=''
    num=None
    fromfindappend=False
    memberappend=False
    i=0
    while(i<len(keywordings)):
        if(keywordings[i] not in nonNounWords):
            if(keywordings[i].isdigit() and keywordings[i+1] in title):
                num=keywordings[i]
                keywordings[i]='limnum'
            else:
                nouns.append(keywordings[i])
            i+=1
        else:
            if(keywordings[i] in queryfunwords):
                queryfun.append(keywordings[i])
                if(keywordings[i] in  count):
                    if(keywordings[i+1]=='का' or keywordings[i+1] == 'की'):
                        keywordings[i+1]='PRICE'
                elif(keywordings[i] in client):
                    if(clientName==None and clientNameSearch==False):
                        clientNameSearch=True
                    elif(clientName!=None):
                        keywordings[i]=clientName
                        keywordings.insert(i+1,'की')
                        queryfun.pop(-1)
                        memberTable=True
                        memberappend=True
                        i+=1
                i+=1
            elif(keywordings[i]=='से' or keywordings[i]== 'सी' or keywordings[i]=='सा'):
                keywordings.pop(i)
            elif(keywordings[i]=='मिल' and (keywordings[i-1]=='कहां' or keywordings[i-1]=='कहाँ')):
                keywordings[i]='सेल्फ'
                nouns.append('सेल्फ')
                i+=1
            else:
                i+=1
    
    j=keywordings.index(nouns[0])
    word=""
    left=keywordings.index(nouns[0])
    right=left
    j_change=True
    for i in range(len(nouns)):
        bookcopySearch=True
        memberSearch=True
        letter=nouns[i]
        k=keywordings.index(letter)
        keywordings[keywordings.index(letter)]='#'
        if(k==j):
            if((letter not in columns) and (translator.translate(letter).text.upper() not in columns) ):
                print('Dra')
                word1=word
                word1=word1+" "+letter
                wordStrip1 = word1.strip()
                wordStrip=word.strip()
                wordStrip1Trans=translator.translate(wordStrip1).text.upper()
                wordStripTrans=translator.translate(wordStrip).text.upper()
                if((wordStrip1 in columns) or (wordStrip1Trans in columns) ):
                    j_change=True
                    word=word+" "+letter
                    right+=1
                elif((wordStrip in columns) or (wordStripTrans in columns) ):
                    for j in book:
                        if(wordStrip in book[j] or wordStripTrans in book[j]):
                            col.append(j)
                            keywordings[left:right]=[j]
                            bookcopySearch=False
                            memberSearch=False
                            break;
                    if(bookcopySearch==True):
                        for j in bookcopy:
                            if(wordStrip in bookcopy[j] or wordStripTrans in bookcopy[j]):
                                col1.append(j)
                                keywordings[left:right]=[j]
                                if(j=='c.status'):
                                    for p in statusDict:
                                        if(wordStrip in statusDict[p] or wordStripTrans in statusDict[p]):
                                            statusval.append(p)
                                            break;
                                memberSearch=False
                                break;
                    if(memberSearch==True):
                        for j in member:
                            if(wordStrip in member[j] or wordStripTrans in member[j]):
                                col2.append(j)
                                keywordings[left:right]=[j]
                                break;
                    gap=right-left
                    word=letter
                    left=k-gap+1
                    right=left+1
                    j=right
                    j_change=False
                else:
                    print('gon')
                    j_change=True
                    word=word+" "+ letter
                    right+=1
            else:
                if(word!=""):
                    print("Naruto")
                    word1=word+" "+letter
                    wordStrip1 = word1.strip()
                    wordStrip1Trans=translator.translate(wordStrip1).text.upper()
                    wordStrip=word.strip()
                    wordStripTrans=translator.translate(wordStrip).text.upper()
                    if((wordStrip1 in columns) or (wordStrip1Trans in columns) ):
                        print("Uzumaki")
                        j_change=True
                        word=word+" "+letter
                        print("please",word)
                        right+=1
                    
                    elif((wordStrip in columns) or (wordStripTrans in columns)):
                        for j in book:
                            if(wordStrip in book[j] or wordStripTrans in book[j]):
                                col.append(j)
                                keywordings[left:right]=[j]
                                bookcopySearch=False
                                memberSearch=False
                                break;
                        if(bookcopySearch==True):
                            for j in bookcopy:
                                if(wordStrip in bookcopy[j] or wordStripTrans in bookcopy[j]):
                                    col1.append(j)
                                    keywordings[left:right]=[j]
                                    if(j=='c.status'):
                                        for p in statusDict:
                                            if(wordStrip in statusDict[p] or wordStripTrans in statusDict[p]):
                                                statusval.append(p)
                                                break;
                                    memberSearch=False
                                    break;
                        if(memberSearch==True):
                            for j in member:
                                if(wordStrip in member[j] or wordStripTrans in member[j]):
                                    col2.append(j)
                                    keywordings[left:right]=[j]
                                    break;
                        gap=right-left
                        word=letter
                        left=k-gap+1
                        right=left+1
                        j=right
                        j_change=False
                                  
                    else:
                        if(ord(wordStrip[0])>=32 and ord(wordStrip[0])<=126):
                            trans.append(wordStrip)
                        else:
                            wordStrip=translator.translate(wordStrip).text
                            trans.append(wordStrip)
                        keywordings[left:right]=[wordStrip]
                        gap=right-left
                        word=letter
                        left=k-gap+1
                        right=left+1
                        j=right
                        j_change=False
                else:
                    j_change=True
                    word=word+" "+ letter
                    print(word)
                    right+=1
        else:
            print("Ball")
            wordStrip=word.strip()
            wordStripTrans=translator.translate(wordStrip).text.upper()
            if((wordStrip in columns) or (wordStripTrans in columns) ):
                for j in book:
                    if(wordStrip in book[j] or wordStripTrans in book[j]):
                        col.append(j)
                        keywordings[left:right]=[j]
                        bookcopySearch=False
                        memberSearch=False
                        break;
                if(bookcopySearch==True):
                    for j in bookcopy:
                        if(wordStrip in bookcopy[j] or wordStripTrans in bookcopy[j]):
                            col1.append(j)
                            keywordings[left:right]=[j]
                            if(j=='c.status'):
                                for p in statusDict:
                                    if(wordStrip in statusDict[p] or wordStripTrans in statusDict[p]):
                                        statusval.append(p)
                                        break;
                            memberSearch=False
                            break;
                if(memberSearch==True):
                    for j in member:
                        if(wordStrip in member[j] or wordStripTrans in member[j]):
                            col2.append(j)
                            keywordings[left:right]=[j]
                            break;
            else:
                print("Z")
                if(ord(wordStrip[0])>=32 and ord(wordStrip[0])<=126):
                    trans.append(wordStrip)
                else:
                    wordStrip=translator.translate(wordStrip).text
                    trans.append(wordStrip)
                keywordings[left:right]=[wordStrip]
            gap=right-left
            word=letter
            left=k-gap+1
            right=left+1
            j=right
            j_change=False
        if(j_change==True):
            j=k+1
            print(j)

    bookcopySearch=True
    memberSearch=True
    wordStrip=word.strip()
    wordStripTrans=translator.translate(wordStrip).text.upper()
    if((wordStrip in columns) or (wordStripTrans in columns) ):
        for j in book:
            if(wordStrip in book[j] or wordStripTrans in book[j]):
                col.append(j)
                keywordings[left:right]=[j]
                bookcopySearch=False
                memberSearch=False
                break;
        if(bookcopySearch==True):
            for j in bookcopy:
                if(wordStrip in bookcopy[j] or wordStripTrans in bookcopy[j]):
                    col1.append(j)
                    keywordings[left:right]=[j]
                    if(j=='c.status'):
                        for p in statusDict:
                            if(wordStrip in statusDict[p] or wordStripTrans in statusDict[p]):
                                statusval.append(p)
                                break;
                    memberSearch=False
                    break;
        if(memberSearch==True):
            for j in member:
                if(wordStrip in member[j] or wordStripTrans in member[j]):
                    col2.append(j)
                    keywordings[left:right]=[j]
                    break;
    else:
        if(ord(wordStrip[0])>=32 and ord(wordStrip[0])<=126):
            trans.append(wordStrip)
        else:
            wordStrip=translator.translate(wordStrip).text
            trans.append(wordStrip)
        keywordings[left:right]=[wordStrip]
    print("keywordings after",keywordings)
    print("nouns",nouns)
    if('The most' in trans):
        trans[trans.index('The most')]='max'
        keywordings[keywordings.index('The most')]='max'
    if('All time low' in trans):
        trans[trans.index('All time low')]='min'
        keywordings[keywordings.index('All time low')]='min'
    print("trans",trans)
    if(clientNameSearch==True):
        if(len(col)==0 and len(col1)==0 and len(col2)==0):
            if(len(trans)==1):
                tofindcol=globaltofind
                it=globalfromfind
                clientName=trans[0]
                trans=[]
                keywordings=[]
                queryfun=[]
                it.append('memberName')
                it.append(clientName)
                globaltofind=[]
                globalfromfind=[]
                clientNameSearch=False
                fromfindappend=True
                for i in (tofindcol):
                    if(i in book):
                        bookTable=True
                    elif(i in bookcopy):
                        bookcopyTable=True
                    else:
                        memberTable=True
                for i in range(len(it)):
                    if(i%2==0):
                        if(i in book):
                            bookTable=True
                        elif(i in bookcopy):
                            bookcopyTable=True
                        else:
                            memberTable=True
    print("col",col)
    print("col1",col1)
    print("col2",col2)
    i=0
    while(i<(len(queryfun))):
        k=keywordings.index(queryfun[i])
        if(queryfun[i] in count and (keywordings[k+1] in ['collation','noofCopy','price','dues'] or keywordings[k-1] in ['collation','noofCopy','price','dues'])):
            queryfun.pop(i)
        else:
            for j in queryfunNoun:
                if(queryfun[i] in queryfunNoun[j]):
                    queryfun[i]=j
            i+=1
    print("queryfun",queryfun)
    i=0
    while(i<len(keywordings)):
        if(keywordings[i] in count):
            k=i
            if(keywordings[k+1] == 'title'):
                col.remove('title')
                keywordings.pop(k+1)
                bookTable=False
            elif(keywordings[k-1] == 'title'):
                col.remove('title')
                keywordings.pop(k-1)
                bookTable=False
            else:
                i+=1
        elif(keywordings[i] == 'नाम'):
            k=i
            if(keywordings[k-1] in kalist):
                i=i-1
                keywordings.pop(i)
                keywordings.pop(i)
            else:
                i+=1
        elif(keywordings[i] in tofindvarlist):
            if(keywordings[i+1] == 'title' or keywordings[i+1]== 'author'):
                tofindvar=keywordings[i+1]
                col.remove(keywordings[i+1])
                keywordings.pop(i+1)
                bookTable=True
            i+=1
        else:
            i+=1
    print("keywordings",keywordings)
    print("col after",col)
    print('tofindvar',tofindvar)
    
    netcol.extend(col)
    netcol.extend(col1)
    netcol.extend(col2)
    for i in netcol:
        visited_change=True
        print(i,tofindcol)
        k=keywordings.index(i)
        if(i in col):
            bookTable=True
            while(k in visited):
                k=keywordings[k+1:].index(i)
            if(keywordings[k+1] in trans or keywordings[k-1] in trans):
                fromfindcol.append(i)
            elif(keywordings[k+1] in tofind or keywordings[k-1] in tofind):
                tofindcol.append(i)
                if(i=='noofCopy'):
                    if(keywordings[k+1]=='reservedYes' or keywordings[k+1]=='reservedNo' or keywordings[k+1]=='c.status'):
                        tofindcol.pop(-1)
                        keywordings.pop(k)
                        visited_change=False
                
        elif(i in col1):
            bookcopyTable=True
            while(k in visited):
                k=keywordings[k+1:].index(i)
            if(keywordings[k-1] in tofind or keywordings[k+1] in tofind):
                if(i=='edition'):
                    if(keywordings[k-1] in count):
                        keywordings[k]='count(distinct year)'
                        tofindcol.append('count(distinct year)')
                    else:
                        keywordings[k]='distinct edition,year'
                        tofindcol.append('distinct edition,year')
                elif(i=='price'):
                    keywordings[k]='distinct cast(price as double)'
                    tofindcol.append('distinct cast(price as double)')
                elif(i=='reservedYes' or i=='reservedNo'):
                    if(i == 'reservedYes'):
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')
                        fromvar = 'reserved'
                        fromvarvalue = '1'   
                    else:
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')
                        fromvar = 'reserved'
                        fromvarvalue= '0'
                elif(i=='c.status'):
                    if(statusval[0]!='status'):
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')
                        fromstatusvar = 'c.status'
                    else:
                        tofindcol.append(statusval[0])
                        
                else:
                    tofindcol.append(i)
            elif(keywordings[k+1] in trans or keywordings[k-1] in trans):
                if(i=='reservedYes' or i=='reservedNo'):  
                    if(i == 'reservedYes'):
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')
                        fromvar = 'reserved'
                        fromvarvalue = '1'   
                    else:
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')
                        fromvar = 'reserved'
                        fromvarvalue= '0'
                elif(i=='c.status'):
                    if(statusval[0]!='status'):
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')
                        fromstatusvar = 'c.status'
                    else:
                        tofindcol.append(statusval[0])
                else:
                    fromfindcol.append(i)
            else:
                if(i not in tofindcol and i not in fromfindcol):
                    bookcopyTable=False
        else:
            memberTable=True
            while(k in visited):
                k=keywordings[k+1:].index(i)
            if(keywordings[k+1] in trans or keywordings[k-1] in trans):
                fromfindcol.append(i)
            elif(keywordings[k+1] in tofind or keywordings[k-1] in tofind):
                tofindcol.append(i)
            else:
                if(i=='dues'):
                    if(keywordings[k-1] == 'title'):
                        fromfindvar2='c.status'
                        fromfindval2='Issued'
                if((i=='eMail' or i=='phoneNo') and keywordings[k+1]=='और'):
                    tofindcol.append(i)
        if(visited_change==True):
            visited.append(k)
    print('this time',tofindcol)    
    print('this',keywordings)
    for i in keywordings:
        if(i in tofindlist):
            k=keywordings.index(i)
            if((k!=0) and (k!=len(keywordings)-1)):
                if(keywordings[k-1] not in tofindcol and keywordings[k+1] not in tofindcol):
                    if(tofindvar!=''):
                        tofindcol.append(tofindvar)
                        print('this time',tofindcol)
                        bookTable=True
    print(trans)
    for i in trans:
        k=keywordings.index(i)
        count=0
        if(keywordings[k-1] not in book and keywordings[k+1] not in book and keywordings[k-1] not in member and keywordings[k+1] not in member):
            for j in keywordings:
                if(j=='author'):
                    k=keywordings.index(j)
                    if(keywordings[k+1] not in tofindlist and keywordings[k-1] not in tofindlist):
                        fromfindcol.append('author')
                        count=1
                        bookTable=True
            if(keywordings[k+1]=='ने' or len(col2)!=0):
                print('yo')
                fromfindcol.append('memberName')
                memberTable=True
                count=1
            if(count==0):
                print('hero')
                fromfindcol.append('title')
                bookTable=True
    global globalvar
    global globalvarcol
    if(len(fromfindcol)==0 and memberappend==False and clientNameSearch==False and fromfindappend==False):
        if('count' not in queryfun):
            if(globalvarcol=='title'): 
                fromfindcol.append('title')
                trans.append(globalvar)
                bookTable=True
            elif(globalvarcol=='memberName'):
                fromfindcol.append('memberName')
                trans.append(globalvar)
                memberTable=True
            elif(globalvarcol=='author'):
                fromfindcol.append('author')
                trans.append(globalvar)
                bookTable=True
                
        else:
            for i in keywordings:
                if(i in subject):
                    if(globalvarcol=='title'):
                        fromfindcol.append('title')
                        trans.append(globalvar)
                        bookTable=True
                        break;
                    elif(globalvarcol=='memberName'):
                        fromfindcol.append('memberName')
                        trans.append(globalvar)
                        memberTable=True
                        break;
                    elif(globalvarcol=='author'):
                        fromfindcol.append('author')
                        trans.append(globalvar)
                        bookTable=True
                        break;
    if(fromvar=='reserved'):
        bookcopyTable=True
        fromfindcol.append('reserved')
        trans.append(fromvarvalue)
    if(fromstatusvar=='c.status'):
        bookcopyTable=True
        while(len(statusval)!=0):
            fromfindcol.append('c.status')
            trans.append(statusval[0])
            statusval.pop(0)
    if(fromfindvar2=='c.status'):
        bookcopyTable=True
        fromfindcol.append('c.status')
        trans.append(fromfindval2)
    print("tofindcol",tofindcol)
    print("fromfindcol",fromfindcol)
    for i in range(len(fromfindcol)):
        it.append(fromfindcol[i])
        it.append(trans[i])
    print("it",it)
    
    if(clientName==None and clientNameSearch==True):
        globaltofind=tofindcol
        globalfromfind=it
        z="आपका नाम क्या है"
        return z
    if(num!=None):
        k=keywordings.index('limnum')
        if(keywordings[k+1]!='title'):
            num=None
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    print(bookTable,bookcopyTable,memberTable)
    if(clientName!=None ):
        if(fromfindappend==True):
            for i in range(len(it)):
                if(i%2==0):
                    fromfindcol.append(it[i])
        elif(memberappend==True):
            fromfindcol.append('memberName')
            trans.append(clientName)
            it.append('memberName')
            it.append(clientName)
    if(('किसका' in keywordings or 'किसकी' in keywordings or 'किसके' in keywordings) and (len(set(member).intersection(keywordings))!=0) ):
        tofindcol.append('memberName')
        memberTable=True
    if((bookTable==True or bookcopyTable==True) and memberTable==True):
        if('count' not in queryfun):
            executequery="select "+"{}, "*(len(tofindcol)-1)+"{} from book b INNER JOIN bookcopy c ON b.code=c.code INNER JOIN member m ON c.lastIssue=m.memberCode "
        else:
            executequery="select count(*) from book b INNER JOIN bookcopy c ON b.code=c.code INNER JOIN member m ON c.lastIssue=m.memberCode "
            tofindcol=[]
        if(len(fromfindcol)!=0):
            executequery+="where "+"UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "UPPER(TRIM({})) LIKE UPPER('%{}%')"
        print(executequery.format(*tofindcol,*it))
        c.execute(executequery.format(*tofindcol,*it))
        ans=c.fetchall()
    elif(bookTable==True and bookcopyTable==True):
        print('tofindcol',tofindcol)
        print('fromfindcol',fromfindcol)
        print('trans',trans)
        if(len(tofindcol)!=0):
            if('lastIssue' not in tofindcol):
                executequery="select "+"{}, "*(len(tofindcol)-1) + "{} from book b INNER JOIN bookcopy c ON b.code=c.code "
            else:
                tofindcol.append('memberName')
                executequery="select "+"{}, "*(len(tofindcol)-1)+"{} from book b INNER JOIN bookcopy c ON b.code=c.code INNER JOIN member m ON c.lastIssue=m.memberCode "
        else:
            if('count' in queryfun):
                executequery="select count(*) from book b INNER JOIN bookcopy c ON b.code=c.code "
        if(len(fromfindcol)!=0):
            executequery+="where "+"UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "UPPER(TRIM({})) LIKE UPPER('%{}%')"
        if(num!=None):
            executequery+=" limit "+str(num)
        print(executequery.format(*tofindcol,*it))
        c.execute(executequery.format(*tofindcol,*it))
        ans=c.fetchall()
    
    elif(memberTable==True):
        if(len(fromfindcol)!=0):
            if('max' in trans):
                k=it.index('max')
                it[k]=fromfindcol[0]
                executequery="select distinct {} from member where {} = (select max({}) from member)"
            elif('min' in trans):
                k=it.index('min')
                it[k]=fromfindcol[0]
                executequery="select distinct {} from member where {} = (select min({}) from member)"
            else:
                executequery="select " + "{},"*(len(tofindcol)-1) + "{} from member where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "UPPER(TRIM({})) LIKE UPPER('%{}%')"           
        else:
            if('count' in queryfun):
                executequery="select " + "count(distinct {}) from member"
            else:
                executequery="select " + "distinct {},"*(len(tofindcol)-1) + "distinct {} from member"
        print(executequery.format(*tofindcol,*it))
        c.execute(executequery.format(*tofindcol,*it))
        ans=c.fetchall()
    elif(bookcopyTable==True):
        pass
    else:
        if(len(fromfindcol)!=0):
            if('count' in queryfun):
                if('max' in trans):
                    k=it.index('max')
                    it[k-1],it[-2]=it[-2],it[k-1]
                    it[k],it[-1]=it[-1],it[k]
                    it[-1]=it[-2]
                    executequery="select count(*) from book where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "{} = (select max({}) from book)"
                elif('min' in trans):
                    k=it.index('min')
                    it[k-1],it[-2]=it[-2],it[k-1]
                    it[k],it[-1]=it[-1],it[k]
                    it[-1]=it[-2]
                    executequery="select count(*) from book where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "{} = (select min({}) from book)"
                else:
                    executequery="select count(*) from book where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "UPPER(TRIM({})) LIKE UPPER('%{}%')"
                tofindcol=[]
            else:
                if('max' in trans):
                    k=it.index('max')
                    it[k-1],it[-2]=it[-2],it[k-1]
                    it[k],it[-1]=it[-1],it[k]
                    it[-1]=it[-2]
                    executequery="select " + "{},"*(len(tofindcol)-1) + "{} from book where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "{} = (select max({}) from book)"
                elif('min' in trans):
                    k=it.index('min')
                    it[k-1],it[-2]=it[-2],it[k-1]
                    it[k],it[-1]=it[-1],it[k]
                    it[-1]=it[-2]
                    executequery="select " + "{},"*(len(tofindcol)-1) + "{} from book where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "{} = (select min({}) from book)"
                else:
                    executequery="select " + "{},"*(len(tofindcol)-1) + "{} from book where " + "UPPER(TRIM({})) LIKE UPPER('%{}%'),"*(len(fromfindcol)-2) + "UPPER(TRIM({})) LIKE UPPER('%{}%') and "*(math.ceil((len(fromfindcol)-1)/len(fromfindcol))) + "UPPER(TRIM({})) LIKE UPPER('%{}%')"
                if(num!=None):
                    executequery+=" limit "+str(num)
        else:
            executequery="select " + "count(*) from book"
            tofindcol=[]
        print(executequery.format(*tofindcol,*it))
        c.execute(executequery.format(*tofindcol,*it))
        ans=c.fetchall()
    if(ans is None):
        z="अपनी क्वेरी की जांच करे"
    else:
        print(len(ans))
        if(len(ans)==0):
            z="यह जानकारी उपलब्ध नहीं हैं"
        else:
            z=""
            countin=1
            l=len(ans)  
            for i in ans:
                if(l>1):
                    z+="<small style='color:grey'>"+str(countin)+")  </small>"
                for j in i:
                    z+=str(j)+" ;"
                z+="<br>"
                countin+=1
            print(fromfindcol)
            print(trans)
            if(len(fromfindcol)!=0):
                if('author' in fromfindcol and len(trans)!=0):
                    k=fromfindcol.index('author')
                    globalvar=trans[k]
                    globalvarcol='author'
                if('title' in fromfindcol and len(trans)!=0):
                    k=fromfindcol.index('title')
                    globalvar=trans[k]
                    globalvarcol='title'
                if('memberName' in fromfindcol and len(trans)!=0):
                    k=fromfindcol.index('memberName')
                    globalvar=trans[k]
                    globalvarcol='memberName'
            if(len(tofindcol)!=0 and len(ans)==1):
                if('author' in tofindcol):
                    k=tofindcol.index('author')
                    for i in range(len(ans)):
                        if(ans[i][k]!=''):
                            globalvar=ans[i][k]
                            globalvarcol='author'
                            break;
                if('title' in tofindcol):
                    k=tofindcol.index('title')
                    for i in range(len(ans)):
                        if(ans[i][k]!=''):
                            globalvar=ans[i][k]
                            globalvarcol='title'
                            break;
                if('memberName' in tofindcol):
                    k=tofindcol.index('memberName')
                    for i in range(len(ans)):
                        if(ans[i][k]!=''):
                            globalvar=ans[i][k]
                            globalvarcol='memberName'
                            break;
                
    return z

def home(request):
    return render(request, 'home.html', {'home':'active'})

def dialog(request):
    if request.method == "POST":
        dialogue = request.POST.get('querybox', None)
        q1 = Dialog(query = dialogue)
        myDate = datetime.now()
        formatedDate = myDate.strftime("%b %d, %Y, %I:%M %p")
        reply = generateQuery(dialogue)
        return JsonResponse({ 'dialog':dialogue, 'time':formatedDate, 'reply':reply })
    else:
        return HttpResponse('Request must be POST.')
