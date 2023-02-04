import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import requests
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


# Create your views here.
from blog.form import RegisterForm, UploadForm
from blog.models import Profile, UserBlog


def home(request):
    data = UserBlog.objects.all()
    if request.method == 'POST':
        topic = request.POST['search']
        if topic == "":
            return render(request,'dashboard.html',{"data":data})
        else:
            userdata = UserBlog.objects.filter(Topic__contains=topic)
            return render(request,'dashboard.html',{'userdata':userdata})
    return render(request,'dashboard.html',{"data":data})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(user_login)
    return render(request,'registration.html',{'form':form})

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passw']
        user = authenticate(username=username,password=passwd)
        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            return redirect(user_login)
    return render(request,'logg.html')


def user_logout(request):
    logout(request)
    return redirect(user_login)

def ViewProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = Profile.objects.get(user_id=current_user.id)
    date_join = data.date_joined
    return render(request, 'profile.html', {'data': data,"data1":data1,'date_join':date_join.date()})

def EditProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = Profile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['address']
        city = request.POST['city']

        User.objects.filter(id=current_user.id).update(first_name=first_name,last_name=last_name,email=email)
        Profile.objects.filter(user_id = current_user.id).update(phone=phone,DOB=dob,address=address,city=city)
        return redirect(ViewProfile)
    return render(request, 'editpro.html', {'data': data,'data1':data1})

def upload_image(request):
    if request.method == 'POST' and request.FILES['images']:
        upload = request.FILES['images']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        Profile.objects.filter(user_id=request.user.id).update(profile_pic=file_url)
        return redirect(ViewProfile)

    return render(request,'propic.html')

def Forgot_password(request):
    if request.method == 'POST':

        mobile = request.POST['phone']
        userdata = Profile.objects.get(phone=mobile)   # registered mobile number of user
        if userdata:
            url = "http://2factor.in/API/V1/482e2bfc-3db4-11ed-9c12-0200cd936042/SMS/{}/AUTOGEN".format(str(mobile))

            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=payload, headers=headers)
            data = response.json()

            r = data['Details']
            request.session['Details'] = r
            request.session['phone'] = mobile
            if data['Status'] == 'Success':
                return redirect(reset_password)
        else:
            return redirect(Forgot_password)
    return render(request, 'forgot.html')

def reset_password(request):
    if request.method == 'POST':
        otp = request.POST['OTP']
        passwd = request.POST['passw']
        cpasswd = request.POST['cpassw']
        details = request.session.get('Details')
        api = 'https://2factor.in/API/V1/482e2bfc-3db4-11ed-9c12-0200cd936042/SMS/VERIFY/{}/{}'.format(details, otp)
        res = requests.get(api).json()
        print(res)
        phone = request.session.get('phone')
        if res['Status'] == 'Success':
            if passwd == cpasswd:
                userdata = Profile.objects.get(phone=phone)
                data = User.objects.get(id=userdata.user_id)
                u = User.objects.get(username = data.username)
                u.set_password(passwd)
                u.save()

                return redirect(user_login)
    return render(request,'verify.html')

def Change_password(request):

    if request.method == 'POST':
        old_pass = request.POST['oldpass']
        new_pass = request.POST['newpass']
        cnf_pass = request.POST['cpass']
        data = check_password(old_pass,request.user.password )
        if data:
            if new_pass == cnf_pass:
                u = User.objects.get(username=request.user.username)
                u.set_password(new_pass)
                u.save()
                print("password change successfully")

            else:
                print('password is not matching')
                return redirect(Change_password)
        else:
            print('Enter the correct password')
            return redirect(Change_password)

    return render(request,'changepass.html')


def CreateProfile(requset):
    data = User.objects.get(id = requset.user.id)
    if requset.method == "POST":
        phone = requset.POST['phone']
        dob = requset.POST['dob']
        address = requset.POST['address']
        city = requset.POST['city']

        prof = Profile.objects.create(user_id = requset.user.id,phone=phone,DOB=dob,address=address,city=city)
        prof.save()
        return redirect(ViewProfile)
    return render(requset,'createpro.html',{"data":data})


def create_blog(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        title = request.POST['blogtitle']
        blogdata = request.POST['content']
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        create_blog = UserBlog.objects.create(user_id= request.user.id,Topic=topic,caption=title,image=file_url,blog_data=blogdata)
        create_blog.save()
        return redirect(viewblog)
    return render(request,'CREATEBLOG.html')

def viewblog(request):
    data = UserBlog.objects.filter(user_id = request.user.id)
    if data:
        return render(request,'viewblog.html',{"data":data})
    return render(request,'viewblog.html')

def View_details(requset,id):
    data = UserBlog.objects.get(id=id)
    return render(requset,"details.html",{"i":data})

def update_blog(request,id):
    data = UserBlog.objects.get(id=id)
    if request.method == 'POST':

        topic = request.POST['topic']
        title = request.POST['blogtitle']
        blogdata = request.POST['content']
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        UserBlog.objects.filter(id=id).update(Topic=topic, caption=title, image=file_url, blog_data=blogdata,updated_date=datetime.datetime.now())
        return redirect(viewblog)
    return render(request, "updateblog.html", {"i": data})

def delete_blog(request,id):
    data = UserBlog.objects.get(id=id)
    data.delete()
    return redirect(viewblog)



