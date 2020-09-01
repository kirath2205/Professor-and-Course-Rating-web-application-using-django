from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse
from .models import Corse, Contact,Modules,CourseComment,Rating3
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from validate_email import validate_email
# Create your views here.
def index(request):
    homecourse=Modules.objects.all()
    print(homecourse)
    
    return render(request,'mainsite/index.html',{'homecourse':homecourse}) 

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request,'mainsite/contact.html') 
##
def courseview(request):
    homecourse=Modules.objects.all()
    for course in homecourse:
        print("id :",course.m_id)
    comments=CourseComment.objects.filter(homecourse=homecourse)
    return render(request,'mainsite/courses.html',{'homecourse':homecourse,'comments':comments}) 

##

def search_course(item,query):
    if(query in item.code or query in item.name or query in item.instructor_1 or query in item.instructor_2):
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    homecourse=Modules.objects.all()
    
    courses_list=[]
    for item in homecourse:
        if(search_course(item,query)):
            courses_list.append(item)

    if(len(courses_list)==0):
        msg='No such course found'
        params={'homecourse':courses_list,'message':msg}
        
    else:
        params={'homecourse':courses_list,'message':''}
    
    return render(request,'mainsite/search.html',params) 

def about(request):
    return render(request,'mainsite/about.html') 

#def viewcourse(request,id):
#    course=Modules.objects.filter(m_id=id)[0]
    
 #   return render(request,'mainsite/viewcourse.html',{'course':course})

def viewcourse(request,slug):
    course=Modules.objects.filter(slug=slug).first()
    
    comments=CourseComment.objects.filter(course=course)
    all_ratings=Rating3.objects.all()

    average_rating=0
    counter=0
    for rate in all_ratings:
       
        if(course != None):
            if(course.m_id==rate.course.m_id):
                print('ye he course ',course.m_id)
                average_rating=average_rating+rate.rating
                counter=counter+1
            
    print('Average rating ye he ',(average_rating/counter))
    average_rating=average_rating/counter
    context={'course':course,'comments':comments, 'user':request.user ,'average_rating':average_rating}
    return render(request,'mainsite/viewcourse.html',context)

def handle_signup(request):
    if(request.method=='POST'):
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if(not username.islower()):
            messages.warning(request,"Your username should be in lowercase")
            return redirect('/')
        if(len(username)>10):
            messages.warning(request, "Username must be under 10 characters")
            return redirect('/')
        if(not username.isalnum()):
            messages.warning(request,"Username should be alphanumeric and should not contain special characters")
            return redirect('/')
        is_valid=validate_email(email)
        if(not is_valid):
            messages.warning(request,'The email address does not exist. Please enter a valid email')
            return redirect('/')
        print("Validity :-  ",is_valid)
        if(pass1 != pass2):
            messages.warning(request,"Passwords do not match")
            return redirect('/')
        if(len(pass1)<8):
            messages.warning(request,"Your password should be atleast 8 characters long")
            return redirect('/')
        if('e.ntu.edu.sg' not in email):
            messages.warning(request,"The user is not authorised")
            return redirect('/')
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,'Your account has been successfully created')
        return redirect('/')
        
    else:
        return HttpResponse('404- Not Found')

def handle_login(request):
    if(request.method=='POST'):
        loginuser=request.POST['loginuser']
        password1=request.POST['password1']
        user=authenticate(username=loginuser,password=password1)
        if(user is not None):
            login(request,user)
            messages.success(request,'Successfully Logged in')
            return redirect('/')
        else:
            messages.warning(request,'Invalid credentials')
            return redirect('/')

    return HttpResponse('404- Not Found')

def handle_logout(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('/')

def postComment(request):
    if(request.method=='POST'):
        comment=request.POST.get('comment')
        user=request.user
        ##
        module_id=request.POST.get('module_id')
        #print("Module id   ",module_id )
        course=Modules.objects.get(m_id=module_id)
        #print("module.m_id   ",course.m_id)
        ##
        #parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
        from keras.models import load_model
        from random import shuffle
        import tensorflow as tf
        import numpy as np
        model=tf.keras.models.load_model('./mainsite/model.h5')
        import pandas as pd
        from tensorflow.keras.preprocessing.sequence import pad_sequences



        max_len = 40
        num_words = 10000
        import keras
        from keras.preprocessing.text import Tokenizer
        data=pd.read_csv("./mainsite/train.csv")
        toxic=data[data["toxic"]==1]["comment_text"]
        non_toxic=data[data["toxic"]==0]["comment_text"]
        toxic=list(toxic)
        non_toxic=list(non_toxic)
        shuffle(toxic)
        shuffle(non_toxic)
        toxic_train=toxic[:10700]
        non_toxic_train = non_toxic[:110000]
        toxic_test=toxic[10700:15294]
        non_toxic_test = non_toxic[110000:144277]
        x_train=toxic_train + non_toxic_train
        y_train=[0,]*len(toxic_train) + [1,]*len(non_toxic_train)
        x_test=toxic_test + non_toxic_test
        y_test=[0,]*len(toxic_test) + [1,]*len(non_toxic_test)
        len_vec = [len(elem) for elem in x_train] #[len(elem) for elem in x_test] + [len(elem) for elem in x_val] 

        from keras.preprocessing.text import Tokenizer
# Fit the tokenizer on the training data
        t = Tokenizer(num_words=num_words,  filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ')
        t.fit_on_texts(x_train+x_test)


        test_example=comment


        x_test_ex = t.texts_to_sequences([test_example])
        x_test_ex = pad_sequences(x_test_ex, maxlen=max_len, padding='post')
        preds = model.predict_proba(x_test_ex)
        list_prediction=np.array(preds)
        toxic_probability=list_prediction[0][0]
        non_toxic_probability=list_prediction[0][1]
        print(toxic_probability)
        if(toxic_probability>0.2):
            messages.warning(request,'Your comment has been classified as toxic, please forbid from making toxic comments')
            return redirect("http://127.0.0.1:8000")
        


        #parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
        comment=CourseComment(comment=comment,user=user,course=course)
        comment.save()
        messages.success(request,'Your comment has been posted')
        print('Slug : ',course.slug)
        k=course.slug
    return redirect("http://127.0.0.1:8000/courseview/"+course.slug)
    #course=Modules.objects.filter(slug=slug).first()
    #context={'course':course}

def postRating(request):
    params={}
    if(request.method=='POST'):
        rating=request.POST.get('rate')
        module_id=request.POST.get('module_id')
        course=Modules.objects.get(m_id=module_id)
        user=request.user
        rating=Rating3(rating=rating,user=user,course=course)
        rating.save()
        all_ratings=Rating3.objects.all()
        average_rating=0
        counter=0
        for rate in all_ratings:
            average_rating=average_rating+rate.rating
            counter=counter+1
            
        #print('Average rating ye he ',(average_rating/counter))
        
        messages.success(request,'Your rating has been posted')
   
    return redirect("http://127.0.0.1:8000/courseview/"+course.slug)
    