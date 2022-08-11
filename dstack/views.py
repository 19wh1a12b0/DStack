import json
from multiprocessing import context
from django.shortcuts import render,redirect
from dstack.models import *
import os
from API_KEYS.keys import keys
from utility.nftstorage import NftStorage
from config.settings import BASE_DIR
from pathlib2 import Path as Path2_
from pathlib import Path
import requests
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

base_uri = "https://ipfs.io/ipfs/"
NFTSTORAGE_API_KEY = keys['NFTSTORAGE']
PINATA_JWT = keys['PINATA']

# Create your views here.
def Home(req):

    return render(req,'home.html')


def Login(request):
    request.session['WalletAddress'] = "xxx"
    if request.POST:
        WalletAddress = request.POST.get('WalletAddress')
        request.session['WalletAddress'] = WalletAddress
        obj = User.objects.get_or_create(WalletAddress=WalletAddress)

        return redirect('userpage')
    else:
        return redirect('home')


def UserPage(request):
    WalletAddress = request.session['WalletAddress']
    user = User.objects.get(WalletAddress=WalletAddress)
    allQuestions=QuestionM.objects.all().order_by('-price')
    allQuestionsData=[]
    for i in allQuestions:
        temp=[]
        r = requests.get(i.hash).json()
        temp.append(r['title'])
        temp.append(r['description'])
        temp.append(i)
        allQuestionsData.append(temp)
        
    
    
    context = {'user':user,'allQuestionsData':allQuestionsData}
    

    
    
    return render(request,'userpage.html',context)

def Question(request):
    WalletAddress = request.session['WalletAddress']
    user = User.objects.get(WalletAddress=WalletAddress)
    PUBLIC_KEY=os.getenv('PUBLIC_KEY')

    context = {'user':user,'receiverWalletAddress':PUBLIC_KEY}
    
    return render(request,'question.html',context)

def questionAdd(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    price = request.POST.get('price')
    handleJsonAndUploadToIPFS(request,title,description,price)
    return redirect('userpage')

def handleJsonAndUploadToIPFS(request,title,description,price):
    WalletAddress = request.session['WalletAddress']
    user = User.objects.get(WalletAddress=WalletAddress)

    dictionary = {
    "title": title,
    "description": description,
    "price": price,
    }

    json_object = json.dumps(dictionary, indent=4)
    cleanUp()
    with open("data.json", "w") as outfile:
        outfile.write(json_object)

    c = NftStorage(NFTSTORAGE_API_KEY)
    meta_file_list = []
    file_ =Path(os.path.normpath( str(BASE_DIR) + '/data.json'))

    meta_file_list.append(file_)
    cid = c.upload(meta_file_list, 'application/json')
    hash=base_uri+cid+'/1'
    if float(price)==0:
        obj = QuestionM.objects.create(user=user,hash=hash,price=price,isActive=True,isFree=False)
    else:
        obj = QuestionM.objects.create(user=user,hash=hash,price=price,isActive=True,isFree=True)
    obj.save()
    cleanUp()


def cleanUp():

    try:
        os.system("del data.json")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


def getByQuestion(request,pkk):
    present_login_WalletAddress = request.session['WalletAddress']
    PRIVATE_KEY=os.getenv('PRIVATE_KEY')
    question = QuestionM.objects.get(id=pkk)

    r = requests.get(question.hash).json()

    comments=Comments.objects.filter(question=question)

    context={'present_login_WalletAddress':present_login_WalletAddress,'question':question,'title':r['title'],'description':r['description'],'price':r['price'],'comments':comments,'PRIVATE_KEY':PRIVATE_KEY }


    return render(request,'question_single.html',context)

def comment(request,pkk):
    WalletAddress = request.session['WalletAddress']
    user = User.objects.get(WalletAddress=WalletAddress)
    question = QuestionM.objects.get(id=pkk)
    data = request.POST.get('comment')
    obj=Comments.objects.create(user=user,question=question,data=data)
    obj.save()

    return redirect('questionId',pkk)


def finalDataSend(request):
    presentWalletId = request.POST.get('presentWalletId')
    commentId = request.POST.get('commentId')
    questionId = request.POST.get('questionId')
    Comments.objects.filter(id=commentId).update(won=True)
    ques = QuestionM.objects.get(id=questionId)
    Comments.objects.filter(question=ques).update(isActive=True)


    return redirect('questionId',questionId)
    


