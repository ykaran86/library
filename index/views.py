#importing important files 
from django.shortcuts import render   #for rendering current page back to original page
from .models import Dialog            #importing dialog class for creation of dialogue/query
from django.http import HttpResponse, JsonResponse           #for returning the data from this page to the javascript
from datetime import datetime             
from googletrans import Translator      #importing google translator
import sqlite3                          #for database connectivity
import math

#creation of some global variables for storing information about 
globalvar=None                                     #for storing the name of the title of the book, or the author, or the member Name mentioned previously
globalvarcol=None                                  #for storing the column whose data has been stored in the globalvar   
clientName=None                                    #for storing the name of the client 
clientNameSearch=False                             #for making system aware of searching for the client's name       
globaltofind=[]                                    #for storing the columns which were to find out in the database as mentioned in the previous query     
globalfromfind=[]                                  #for storing the columns along with their given information which were mentioned in the previous query

#generateQuery function for generating the sql query based on the query from the user
def generateQuery(query):
    #checking whether the query is a concluding statement 
    if(query=='धन्यवाद' or query=='शुक्रिया' or query=='थैंक यू सो मच' or query=='थैंक यू' or query=='थैंक्स'):
        return('इस सुविधा का उपयोग करने के लिए धन्यवाद')
    #declaring global variables
    global clientName
    global clientNameSearch
    global globaltofind
    global globalfromfind
    translator = Translator()                       #creating translator object for translating whenever needed.
    #now we will be creating some lists for declaring our rules.
    #words in where list will tell 'WHERE' statement to be used in the sql query
    where=('जो','जिनका','जिनके','जिनकी','जिनको','जिसका','जिसके','जिसकी','जिसने','जिसको','जिन्हें','जिन्होंने','किसका','किसकी','किसने','जिस','किस','किसके','जिसमें','जिसमे')
    #words in count list will tell 'COUNT(*)' statement to be used in the sql query    
    count=('कितना','कितनी','कितने','कितनों','कोई')
    #will check the global variable clientName, whether it's None or not
    client=('मेरा','मेरी','मैंने','हमारा','हमारी','हमने','हम','हमको','हमें')
    #will tell 'MAX()' to be used in sql query
    maxm=('सबसे ज्यादा',)
    #will tell 'MIN()' to be used in sql query
    minm=('सबसे कम',)
    #words in subject list will tell there is some kind of indirect addressing and it will help to check what kind of information is stored in the global variable 'globalvar' 
    subject=('इनका','उनका','इसका','उसे','उसका','उसको','इनके','उनके','उसने','इसके','इन्होंने','उन्होंने','उसके','उसमें','उसमे','इनकी','उनकी','इसकी','उसकी','यह','वह','इस','उस','ये','वो')
    #some typical words which appear together with the word 'नाम'. for example 'इनका नाम'
    kalist=('इनका','उनका','इसका','उसका','इनके','उनके','उसको','इसके','उसके','इनकी','उनकी','इसकी','उसकी','का','की','के')
    #words which which will tell the column just after these will be the ones which we have to find
    tofindvarlist=('जो','जिसने','जिस','जिन्होंने')
    #words which which will tell the column just after these will be the ones which we have to find
    tofindlist=('कौन','कौनसी','किसने','क्या','बताइए','बता','मिल')
    tofind=('कौन','कोई','कहां','कहाँ','कब','कौनसी','कौन-कौन','कितना','कितनी','कितने','किसने','क्या','किस','बताइए','बताइये','बता','मिल')
    who=('कौन','कौनसी','कौन-कौन')
    #some usual words which can be seen in most of the queries but have no significance in query generation
    words=('कब','कहाँ','कहां','का','की','किया','था','थे','कि','के','को','है','हैं','था','टोटल','कुल','मिलाकर','या','सब','से','लिए','गई','वाली','वाले','में','थी','लाइब्रेरी','धन्यवाद','और','सारी','क्या','सकता','नाम','मिलेगा','आप','बता','सकते','सकती','जानकारी','मिलेगी','मिल','हो','बताइए','बताइये','दीजिए','किसी','ने','कराई','सी','घर')
    #creating dictionaries with the help of the lists    
    nonNoun={'where':where,'count':count,'client':client,'max':maxm,'min':minm,'subject':subject,'who':who,'words':words}
    queryfunNoun={'where':where,'count':count,'client':client,'max':maxm,'min':minm} #this dictionary will be used for checking which kind of statement will be used in the sql query for example where, or count
    #We have three tables in interest and there names are 1) book 2) bookcopy and 3) member
    #for these tables we will create some lists which will tell which columns are of interest
    #words in code list will tell code column in the book Table is to be used     
    code=('कोड','कोड नंबर','CODE','CODE NUMBER','CODE NO','CODE NO.')
    classNo=('क्लास','क्लास नंबर','CLASS','CLASS NO','CLASS NUMBER','CLASS NO.') #similarly for classNo column
    title=('बुक','किताब','पुस्तक','किताबों','पुस्तकों','किताबें','पुस्तकें','BOOK','BOOKS','टाइटल','TITLE') # title column
    author=('ऑथर','राइटर','लेखक','लेखकों','लिखा','लिखी','AUTHOR','WRITER')  #author column
    publication=('पब्लिकेशन','publication')     #publication column
    collation=('पेजेज','पन्ने','पेज','collation','PAGE','PAGES')    #collation column
    series=('सीरीज','SERIES')   #series column
    noofCopy=('कॉपी','कॉपियां','नंबर ऑफ कॉपी', 'COPY', 'COPIES', 'NUMBER OF COPIES', 'NUMBER OF COPY')  #noofCopy column
    keywords=('रिलेटेड','RELATED','तरह')    #keywords column
    #columns in bookcopy table
    accessionNo=('एक्शन नंबर','अक्सेशन नंबर','ACCESSION NO.','ACCESSION NO','ACCESSION NUMBER')     #accessionNo columns
    edition=('एडिसन','एडिशंस','एडिशन','एडिशन्स','EDITION','EDITIONS')   #edition column
    price=('दाम','प्राइस','कॉस्ट','PRICE','COST')   #price column
    reservedNo=('रिजर्व नहीं','रिज़र्व नहीं','रिजर्व्ड नहीं','रिजल्ट नहीं')  #reserved column
    reservedYes=('रिजर्व','रिज़र्व','रिजर्व्ड','रिजल्ट','RESERVE','RESERVED')    #reserved column
    status=('स्टेटस','अवेलेबल','मिसिंग','रिकवर','राइट ऑफ','STATUS','AVAILABLE','MISSING','RECOVER','RECOVERED','WRITE OFF') #status
    #because of different values in the status column we will be creating dictionary for mapping different words to their corresponding values in the status column
    statusDict={'status':['स्टेटस','STATUS'],'Available':['अवेलेबल','AVAILABLE'],'Issued':[],'Missing':['मिसिंग','MISSING'],'Recovered':['रिकवर','RECOVER','RECOVERED'],'Writeoff':['राइट ऑफ','WRITE OFF']}
    shelfNo=('सेल्फ','जगह','पर','पे','SHELF','SHELF NUMBER','SHELF NO','SHELF NO.')     #shelfNo column
    lastIssue=('इशू','यीशु','ISSUED','ISSUE','लास्ट','LAST','लास्ट इशू','लास्ट यीशु','LAST ISSUE')      #lastIssue column
    IssueDate=('ड्यू डेट','इशू डेट','यीशु डेट','ISSUE DATE','लास्ट इशू डेट','लास्ट यीशु डेट','LAST ISSUE DATE')     #IssueDate column
    #columns in member Table    
    memberCode=('मेंबर कोड','मेंबर ID','MEMBER CODE','MEMBER ID')   #memberCode column       
    memberName=('मेंबर','मेंबर नेम','MEMBER','MEMBER NAME')     #memberName column
    fatherName=('फादर','पिता','पिताजी','बाप','FATHER')      #fatherName column
    socialCategory=('कैटेगरी','केटेगरी','जाति','कास्ट','CATEGORY','CASTE')      #socialCategory column
    designation=('डेसिग्नेशन','देसिग्नेशन','पोस्ट','DESIGNATION','POST')        #designation column
    groupCode=('ग्रुप कोड','ग्रुप','ग्रुप ID','GROUP','GROUP CODE','GROUP ID')      #groupCode column
    joiningDate=('जोइनिंग डेट','जॉइन','ज्वाइन','JOIN','JOINING DATE')       #joiningDate column
    address=('पता','एड्रेस','एड्रेस','ADDRESS')     #address column will be used collectively for addressLocal and addressHome
    phoneNo=('फ़ोन नंबर','फोन नंबर','कांटेक्ट नंबर','PHONE NO','CONTACT NO','PHONE NO.','CONTACT NO.','PHONE NUMBER','CONTACT NUMBER')       #phoneNo column
    eMail=('मेल ID','ईमेल ID','ईमेल','ईमेल एड्रेस','EMAIL','EMAIL ID','EMAIL ADDRESS')      #eMail column
    dues=('ड्यूस','डीयू','ड्यूश','ड्यू ','DUES','DUE','DEW','DEWS','DUECE')     #dues column
    #creating dictionary for the respective tables
    book={'code':code,'classNo':classNo,'title':title,'author':author,'publication':publication,'collation':collation,'series':series,'noofCopy':noofCopy,'keywords':keywords}
    bookcopy={'accessionNo':accessionNo,'edition':edition,'price':price,'reservedYes':reservedYes,'reservedNo':reservedNo,'c.status':status,'shelfNo':shelfNo,'lastIssue':lastIssue,'IssueDate':IssueDate}
    member={'memberCode':memberCode,'memberName':memberName,'fatherName':fatherName,'socialCategory':socialCategory,'designation':designation,'groupCode':groupCode,'joiningDate':joiningDate,'addressLocal,addressHome':address,'phoneNo':phoneNo,'eMail':eMail,'dues':dues}   
    queryfun = []       #will store words which will call the type of statement to be used in the sql query for example where , max , count
    queryfunwords=[]    #storing corressponding sql statement for example where , max, count
    visited=[]      #storing which words have been visited while processing
    #decalring some empty strings which will be used later in the code
    fromvar=''
    tofindvar=''
    fromstatusvar=''
    #declaring some boolean variables whose uses will be discussed later
    bookcopySearch=True
    bookTable=False
    bookcopyTable=False
    memberSearch=True
    memberTable=False
    #now extending all the dictionaries in different lists for searching purpose
    for i in queryfunNoun:
        queryfunwords.extend(queryfunNoun[i])
    #creating column list which will be used for verifying whether a word in the query corresponds to a particular column from a particular table
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
    keywordings=list(query.split()) #splitting the query into words separated by space
    #creating some lists
    nouns=[]    #for holding nouns or information mentioned in the query
    trans=[]    #for holding information in a form which can be used for searching in the database
    col=[]      #for holding columns corresponding to book Table
    col1=[]     #for holding columns corresponding to bookcopy Table
    col2=[]     #for holding columns corresponding to member Table
    netcol=[]   #for holding all the columns collectively in this list
    statusval=[]    #for holding different values of the status column in the bookcopy table
    tofindcol=[]    #for holding the columns which we have to find
    fromfindcol=[]  #for holding the columns which we have been given with information in the query
    it=[]           #for holding columns from fromfindcol list alongwith values from trans list
    #declaring empty lists which will be discussed later 
    fromfindvar2=''
    fromfindval2=''
    num=None        #incase user asks for a limited number of rows from the database. for example, 'physics se related 15 kitabon ke naam bataiye'
    #declaring some boolean variables which will be discussed later
    fromfindappend=False    
    memberappend=False
    i=0
    #in this loop we will categories each word from the query whether it is a limiting number, or a noun, or a normal word
    while(i<len(keywordings)):
        if(keywordings[i] not in nonNounWords):
            if(keywordings[i].isdigit() and keywordings[i+1] in title):
                num=keywordings[i]
                keywordings[i]='limnum'     #if the word is a limiting number we will store it as num and replace it by 'limum'
            else:
                nouns.append(keywordings[i])    #if the word is a noun we will store it in noun list
            i+=1
        else:
            if(keywordings[i] in queryfunwords):
                queryfun.append(keywordings[i])
                if(keywordings[i] in  count):
                    if(keywordings[i+1]=='का' or keywordings[i+1] == 'की'):
                        keywordings[i+1]='PRICE' # for queries like 'yeh kitaab kitne ki hai' tells to find price of the book
                elif(keywordings[i] in client):
                    if(clientName==None and clientNameSearch==False):  #if the client is referring to himself/herself we will check whether his/her is already available or not if not then
                        clientNameSearch=True                           # we will switch on the clientNameSearch varible which will search for client's name in the next query
                    elif(clientName!=None):
                        keywordings[i]=clientName                       #but if client's name is available then we will replace 'mera/meri/..' type of word with his/her name for queries related to him/her
                        keywordings.insert(i+1,'की')                    #adding 'ki' after the name. for exmaple meri kitab will be replaced by rahul ki kitab
                        queryfun.pop(-1)                                #we will pop the meri or mera type of word from the queryfun as it will be of no use because we are already using his/her name
                        memberTable=True                                # as we are using member's name this mean we will be using memberTable in our sql query 
                        memberappend=True                               # we will use member's name and other informations 
                        i+=1
                i+=1
            elif(keywordings[i]=='से' or keywordings[i]== 'सी' or keywordings[i]=='सा'):
                keywordings.pop(i) #removing this kind of words which have no significance
            elif(keywordings[i]=='मिल' and (keywordings[i-1]=='कहां' or keywordings[i-1]=='कहाँ')):
                keywordings[i]='सेल्फ' # for finding the location of a book in the library
                nouns.append('सेल्फ')
                i+=1
            else:
                i+=1
    
    #now we are going to the most important loop in which we will check which words are together a single word and which words are corresponding to a column and which ones are giving information. for exmaple 'number', 'of', 'copies' these three words together means 'number of copies' and corresponds to noofCopy column
    j=keywordings.index(nouns[0])       #starting with first word of the query 
    word=""                             #for storing the word        
    left=keywordings.index(nouns[0])    #for marking the starting of a word
    right=left                          #for marking the end of a word
    j_change=True                       #enabling/disabling the change in the index
    #we will loop for the length of the nouns list
    for i in range(len(nouns)):
        bookcopySearch=True     #we will assume that word which corresponds to any column may belong to bookcopy Table
        memberSearch=True       #or member Table
        letter=nouns[i]         #letter will have the noun word
        k=keywordings.index(letter)
        keywordings[keywordings.index(letter)]='#'      #replacing the actual word in the query by '#'
        if(k==j):                                       # this is a very necessary condition for checking whether two words are together or not. for example, 'rahul kumar ki kitni dues hai', 'rahul' and 'kumar' have consecutive indices so these two words are together so first both of these words will be replaced by '#' and both '#' will be replaced by 'rahul kumar'
            if((letter not in columns) and (translator.translate(letter).text.upper() not in columns) ): #if word does not correspond to any column
                print('Dra')
                #word variable will contain previously made word and word1 will contain word + letter(noun accessed just now) 
                word1=word
                word1=word1+" "+letter
                wordStrip1 = word1.strip()
                wordStrip=word.strip()
                wordStrip1Trans=translator.translate(wordStrip1).text.upper()
                wordStripTrans=translator.translate(wordStrip).text.upper()
                if((wordStrip1 in columns) or (wordStrip1Trans in columns) ): # for example letter='number' which does not corresponds to any column but previously made word was 'class' so word+letter = 'class number' which corresponds to classNo column
                    j_change=True
                    word=word+" "+letter        #adding letter to our word variable
                    right+=1                    #increasing the end of the word
                elif((wordStrip in columns) or (wordStripTrans in columns) ):  #for example letter='rahul' and word='dues' so word corresponds to a column and word and letter cannot be joined as both are not together
                    for j in book:          #first checking in the book Table
                        if(wordStrip in book[j] or wordStripTrans in book[j]):
                            col.append(j)       #adding the corresponfing column to the col list
                            keywordings[left:right]=[j]     #replacing all the '#' by th newly joined words for example "#","#" by 'rahul kumar'
                            bookcopySearch=False    #now no need to search for this column in bookcopyTable and memberTable
                            memberSearch=False
                            break;
                    if(bookcopySearch==True): #if the column is not in bookTable then it can be in bookcopy Table
                        for j in bookcopy:
                            if(wordStrip in bookcopy[j] or wordStripTrans in bookcopy[j]):
                                col1.append(j)      #similar steps as previous
                                keywordings[left:right]=[j]
                                if(j=='c.status'): #if the column is status then we have to do some extra work as this column is multivalued
                                    for p in statusDict:
                                        if(wordStrip in statusDict[p] or wordStripTrans in statusDict[p]):
                                            statusval.append(p)   # we will store the value corresponding to the word in the query for example 'available' 
                                            break;
                                memberSearch=False # now no need to search in the memberTable
                                break;
                    if(memberSearch==True): #if the column is not in book Table or bookcopyTable then it will be in memberTable surely
                        for j in member:    #similar steps
                            if(wordStrip in member[j] or wordStripTrans in member[j]):
                                col2.append(j)
                                keywordings[left:right]=[j]
                                break;
                    gap=right-left  #now as several '#' have been replaced a single substring  it will create a gap
                    word=letter     # we will making our word equal to the just accessed noun for example, 'rahul'.
                    left=k-gap+1    #marking the staring and end of the new word
                    right=left+1
                    j=right
                    j_change=False
                else:
                    print('gon')
                    j_change=True   #if the word also not corresponds to any column then we will add the letter to it
                    word=word+" "+ letter
                    right+=1
            else: #if the letter itself in columns
                if(word!=""):
                    print("Naruto") #similar steps
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
                                  
                    else: #if the word does not corresponds to any column, this means it must be a given information. for example :- 'rahul kumar' 
                        if(ord(wordStrip[0])>=32 and ord(wordStrip[0])<=126): # checking whether it's already in english
                            trans.append(wordStrip) #appending it in the trans list
                        else:
                            wordStrip=translator.translate(wordStrip).text
                            trans.append(wordStrip)
                        keywordings[left:right]=[wordStrip] #similar  steps
                        gap=right-left
                        word=letter
                        left=k-gap+1
                        right=left+1
                        j=right
                        j_change=False
                else:
                    j_change=True #similar steps
                    word=word+" "+ letter
                    print(word)
                    right+=1
        else:           #if two words are not consecutive
            print("Ball") #similar steps
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
    #as the word which is formed with last element in the noun list is left we will use similar steps for it
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
    #if user is want to check max or min value of something
    if('The most' in trans):
        trans[trans.index('The most')]='max'
        keywordings[keywordings.index('The most')]='max'
    if('All time low' in trans):
        trans[trans.index('All time low')]='min'
        keywordings[keywordings.index('All time low')]='min'
    print("trans",trans)
    #if clientName is to be searched
    if(clientNameSearch==True):
        if(len(col)==0 and len(col1)==0 and len(col2)==0):  #when user will give his/her name nothing else is asked or given
            if(len(trans)==1): # just his/her name is given in the query nothing else is asked or given
                tofindcol=globaltofind # we will check what user had asked previously
                it=globalfromfind # initializing our it list which is used to store given info along with its corresponding column
                clientName=trans[0] # using client's name
                #now we have user's name and things to find so nothing else is required so making them clear
                trans=[]
                keywordings=[]
                queryfun=[]
                it.append('memberName')         #user's name corresponds to memberName column
                it.append(clientName)
                globaltofind=[]
                globalfromfind=[]
                clientNameSearch=False          #now no need to search for client's name
                fromfindappend=True             #will be discussed later
                for i in (tofindcol):           
                    if(i in book):              
                        bookTable=True          #if the column to find belongs book Table
                    elif(i in bookcopy):
                        bookcopyTable=True      #or bookcopy table    
                    else:
                        memberTable=True        #or member table
                for i in range(len(it)):        #as it list stores column's name and then its info so  column's name will be at even indices
                    if(i%2==0):
                        if(i in book):          #similar steps
                            bookTable=True
                        elif(i in bookcopy):
                            bookcopyTable=True
                        else:
                            memberTable=True
    print("col",col)
    print("col1",col1)
    print("col2",col2)
    i=0
    # if words like 'kitna', 'kitne' etc. which tells 'count(*)' statement to be used comes with some particular columns such as 'kitne pages hai'. in this kind of query we have to just give pages. there's no need of count(*) so will we solve this in this loop
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
    #in some queries we have 'kitni kitabein hai' here we just have to count there no significance of 'kitaabein' so we will remove
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
        elif(keywordings[i] == 'नाम'):# some queries comes with 'ka naam bataiye' now it is obvious we have to tell title or author's name or member's name so we will pop these words 
            k=i
            if(keywordings[k-1] in kalist):
                i=i-1
                keywordings.pop(i)
                keywordings.pop(i)
            else:
                i+=1
        elif(keywordings[i] in tofindvarlist):# for queries like 'j.k. rowling ne jo kitaab likhi hai uska price kitna hai'. here 'jo kitab likhi' tells 'j.k. rowing' is author and we have gather info for the book written by her.
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
    #now we will classify each column into whether it is the columnn which we have to find or its the one whose information is also given
    netcol.extend(col)
    netcol.extend(col1)
    netcol.extend(col2)
    for i in netcol:
        visited_change=True
        print(i,tofindcol)
        k=keywordings.index(i)
        #first we will check for the columns belonging to book Table
        if(i in col):
            bookTable=True
            while(k in visited):
                k=keywordings[k+1:].index(i)
            if(keywordings[k+1] in trans or keywordings[k-1] in trans): #if it is a given info column(10 page wali kitab, here 10 is in trans and page will correspond to collation column)
                fromfindcol.append(i)
            elif(keywordings[k+1] in tofind or keywordings[k-1] in tofind):#if it is the column which we have to find
                tofindcol.append(i)
                if(i=='noofCopy'):# for example 'advance biology ki kitni copy available hai' here copy copy corresponds to noofCopy column but its of no significance
                    if(keywordings[k+1]=='reservedYes' or keywordings[k+1]=='reservedNo' or keywordings[k+1]=='c.status'):
                        tofindcol.pop(-1)
                        keywordings.pop(k)
                        visited_change=False
        # we will check in bookcopy Table
        elif(i in col1):
            bookcopyTable=True
            while(k in visited):
                k=keywordings[k+1:].index(i)
            if(keywordings[k-1] in tofind or keywordings[k+1] in tofind):
                if(i=='edition'):   #if the column belongs to edition column
                    if(keywordings[k-1] in count):      #if the user wants to know how many different editions of the same book is available
                        keywordings[k]='count(distinct year)'
                        tofindcol.append('count(distinct year)')
                    else:
                        keywordings[k]='distinct edition,year'  #if the user wants to know all different editions
                        tofindcol.append('distinct edition,year')
                elif(i=='price'):  #if the column belongs to price
                    keywordings[k]='distinct cast(price as double)'
                    tofindcol.append('distinct cast(price as double)')
                elif(i=='reservedYes' or i=='reservedNo'):  #if the user wants to know whether a book is reserved or not
                    if(i == 'reservedYes'):
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')        #count how many books are reserved
                        fromvar = 'reserved'
                        fromvarvalue = '1'   
                    else:
                        keywordings[k]='count(*)'
                        tofindcol.append('count(*)')        #count how many books are not reserved
                        fromvar = 'reserved'
                        fromvarvalue= '0'
                elif(i=='c.status'):                        #if the user wants to know about the status of the book
                    if(statusval[0]!='status'):             #user can directly ask about status of the book or he/she can ask whether that book is available or not . now available is a value from the status column.
                        keywordings[k]='count(*)'           #so when the user asks how many books are available then we have to count the no. of books available
                        tofindcol.append('count(*)')
                        fromstatusvar = 'c.status'
                    else:
                        tofindcol.append(statusval[0])      #but when the user asks about the status of the book, then we have to simply return the value from the status column of the bookcopy table 
                        
                else:
                    tofindcol.append(i)
            elif(keywordings[k+1] in trans or keywordings[k-1] in trans):
                if(i=='reservedYes' or i=='reservedNo'):        #similar steps
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
                    if(keywordings[k-1] == 'title'): #if the user asks 'meri kitni kitabeein dues hai' here kitni will tell to use count, kitaabein will tell about book table and dues about member table
                        fromfindvar2='c.status'      #the books which are due will have issued value in the status column of the bookcopy table
                        fromfindval2='Issued'
                if((i=='eMail' or i=='phoneNo') and keywordings[k+1]=='और'): # if the user asks something like 'unka phone no aur email id bta dijiye' here we have to find both phone no and email id
                    tofindcol.append(i)
        if(visited_change==True):
            visited.append(k)
    print('this time',tofindcol)    
    print('this',keywordings)
    for i in keywordings:#this loop is for queries like 'j.k. rowling ne jo kitaab likhi hai uska naam kya hai' here 'kya' comes in tofindlist and its not at the end nor starting and title because of kitaab will be stored in tofindvar
        if(i in tofindlist):
            k=keywordings.index(i)
            if((k!=0) and (k!=len(keywordings)-1)):  #if the word does not lies at the starting or at the end
                if(keywordings[k-1] not in tofindcol and keywordings[k+1] not in tofindcol):
                    if(tofindvar!=''):
                        tofindcol.append(tofindvar)
                        print('this time',tofindcol)
                        bookTable=True
    print(trans)
    for i in trans: #for queries in which names are used like 'rahul ka kitna dues hai ' or 'advance biology ke lekhak kaun hai' or 'j.k. rowling ne kaun si kitaab likhi hai' 
        k=keywordings.index(i)  #so task is to identify whether its book's title or author or member name
        count=0
        if(keywordings[k-1] not in book and keywordings[k+1] not in book and keywordings[k-1] not in member and keywordings[k+1] not in member):
            for j in keywordings:   #when the name is author's then there must be a word in the query like 'likha' or 'likhi' or something like that which lies in author list.
                if(j=='author'):
                    k=keywordings.index(j)
                    if(keywordings[k+1] not in tofindlist and keywordings[k-1] not in tofindlist):
                        fromfindcol.append('author')
                        count=1
                        bookTable=True
            if(keywordings[k+1]=='ने' or len(col2)!=0): #when in query users talks about column related to member table or there is a word 'ne' after the name then it must be the member's name
                print('yo')
                fromfindcol.append('memberName')
                memberTable=True
                count=1
            if(count==0):
                print('hero')
                fromfindcol.append('title')     #if nothing from the above suits then it is books title
                bookTable=True
    global globalvar
    global globalvarcol
    if(len(fromfindcol)==0 and memberappend==False and clientNameSearch==False and fromfindappend==False):
        if('count' not in queryfun):  #for queries like  'uski kitni kitaabein dues hai' or any query where indirect addressing is done then we have to check what user is talking about checking previously asked queries
            if(globalvarcol=='title'): #so we will find what user had given in the previous query using global variables
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
    if(fromvar=='reserved'): # now whether a book is reserved or not we have to check in the reserved column so we will use reserved column
        bookcopyTable=True
        fromfindcol.append('reserved')
        trans.append(fromvarvalue)
    if(fromstatusvar=='c.status'): # when user talks about availablibilty  of a book
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
    for i in range(len(fromfindcol)): #finally arranging given column and its info in 'it' list 
        it.append(fromfindcol[i])
        it.append(trans[i])
    print("it",it)
    
    if(clientName==None and clientNameSearch==True): #if the clientNameSearch is on then system will first ask user's name
        globaltofind=tofindcol
        globalfromfind=it
        z="आपका नाम क्या है"
        return z
    if(num!=None):
        k=keywordings.index('limnum')   #if user uses limiting number like 'physics se related 10 kitaabein ke naam bta dijiye' 10 will be replaced by limum and 10 will be in num
        if(keywordings[k+1]!='title'):
            num=None
    conn = sqlite3.connect('library.db')  #making connectivity with database
    c = conn.cursor()
    print(bookTable,bookcopyTable,memberTable)
    if(clientName!=None ):
        if(fromfindappend==True):        #when client asks something about himself then first system asks his name then it stores the info which user has given and what he has asked so after user answers his name using previously provided info answer is provided the columns which were given are also copied to fromfindcol
            for i in range(len(it)):
                if(i%2==0):
                    fromfindcol.append(it[i])
        elif(memberappend==True):      #also member name should be used in the query as user is asking about himself/herself
            fromfindcol.append('memberName')
            trans.append(clientName)
            it.append('memberName')
            it.append(clientName)
    if(('किसका' in keywordings or 'किसकी' in keywordings or 'किसके' in keywordings) and (len(set(member).intersection(keywordings))!=0) ):#if someone asks 'abc@xyz.com email id kiski hai' so we have to tell the users name
        tofindcol.append('memberName')
        memberTable=True
    #now just query is to left generate
    if((bookTable==True or bookcopyTable==True) and memberTable==True): #when member Table and any one of the other table is used
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
    elif(bookTable==True and bookcopyTable==True): #if member Table is not used
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
        z="अपनी क्वेरी की जांच करे"   #if there is some problem in the query
    else:
        print(len(ans))
        if(len(ans)==0):
            z="यह जानकारी उपलब्ध नहीं हैं"      #if there can be no answer found
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
            #now we have to store some info asked or given in this query which could be used later. basically in this code i have just used global variables so i can only store a single information so i made priority of what to be stored memberName>titleName>authorName and info in the ans > info in the query
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
