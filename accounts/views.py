from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CustomUser
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse_lazy, reverse
from .forms import RegisterForm, VerifyForm, CodeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .utils import send_sms
from decouple import config
from .forms import UserLoginForm
import pymssql
from portal.tasks import unactivated_user_timeout
from axes.utils import reset_request

SQL_PASSWORD = config('SQL_PASSWORD')
SQL_PROD_HOST = config('SQL_PROD_HOST')
SQL_USER = config('SQL_USER')

def index(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'registration/index.html', {'messages':messages_to_display})

@login_required
def profile(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'registration/profile.html', {'messages':messages_to_display})

def auth_view(request):
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST, request=request)

        if form.is_valid():
            print('valid')
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request=request, 
                username=username, 
                password=password,
                )

            if user is not None:
                request.session['pk'] = user.pk
                return redirect('validate')
            
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
            

    return render(request, 'registration/login.html', {'form':form})

def validate(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.code}"
        if not request.POST:
            send_sms(code_user, user.phone)
            print(code_user)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                return redirect('login-view')
    return render(request, 'registration/validate.html', {'form':form})

def verify_user(request):
    messages_to_display = messages.get_messages(request)

    print('connecting...')
    conn = pymssql.connect(
        host=SQL_PROD_HOST,
        tds_version=r'7.0',
        user=SQL_USER,
        password=SQL_PASSWORD,
        database='Member'
    )
    
    cursor = conn.cursor(as_dict=True)
    cursor.execute(''' SELECT Chapters.chp_id
                ,Chapters.chp_code
                ,Chapters.Chp_Name_Short
                ,Chapters.PrimaryChapter
                ,Schools.sch_ConversationalName
                ,Schools.sch_school
                FROM Chapters
                INNER JOIN Schools
                ON Chapters.chp_id = Schools.sch_id
                where chp_name_greek != ''
                and PrimaryChapter = 'Y'
                and sch_ConversationalName != '' ''')
    chapters = cursor.fetchall()
    
    chap_list = []
    for c in chapters:
        chap_list.append((str(c['chp_code']),c['sch_school'] + "   (" + c['Chp_Name_Short'].strip() + ")"))
    form = VerifyForm(chap_list)

    if request.method == 'POST':
       
        form_data = request.POST.dict()
        email = form_data.get('email')
        grad_year = form_data.get('grad_year')
        chapter = form_data.get('chapter')


        print('connecting...')
        conn = pymssql.connect(
            host=SQL_PROD_HOST,
            tds_version=r'7.0',
            user=SQL_USER,
            password=SQL_PASSWORD,
            database='Member'
        )
        print('success connecting to ms sqlserver')
        cursor = conn.cursor(as_dict=True)

        try:
            validate_email(email)
        except ValidationError as e:
            print("bad email, details:", e)
        else:
            clean_email = email
  
            cursor.execute(''' SELECT Memblist.mem_id
                                ,Memblist.mem_classy
                                ,Memblist.mem_lname
                                ,Memblist.mem_fname
                                ,Memblist.mem_mname
                                ,Memblist.PreferredName  
                                ,Memblist.mem_chpcd  
                                ,Chapters.chp_name
                                ,Chapters.Chp_Name_Short
                                ,Chapters.chp_code
                                ,Chapters.PrimaryChapter
                                ,Address.add_memid
                                ,Address.add_email
                                ,Address.add_email_alt
                                FROM Memblist
                                INNER JOIN Chapters
                                ON Memblist.mem_chpcd = Chapters.chp_code
                                INNER JOIN Address
                                ON Address.add_memid = Memblist.mem_id
                                WHERE Memblist.mem_classy = %s 
                                AND Memblist.mem_chpcd = %s 
                                AND add_email = %s OR add_email_alt = %s ''', [grad_year, chapter, clean_email, clean_email])
            users = cursor.fetchall()


            if len(users) > 0:
                first_name = users[0]['mem_fname']
                last_name = users[0]['mem_lname']
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                messages.success(request, 'Welcome ' + first_name +  ' ' + last_name + ', please create your account within the Tau Beta Pi Portal.')
                return redirect('register')
            else:
                messages.error(request, 'No member with the specified details exists within the Tau Beta Pi database. Please try again or contact member.update@tbp.org.')
                return redirect('verify')

    return render(request, 'registration/verify.html', {'form':form, 'messages':messages_to_display})


def register_user(request):
    messages_to_display = messages.get_messages(request)
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            unactivated_user_timeout()
            email.send()
            messages.success(request, 'Please check your email to compete registration.')
            return redirect('index')
        
    return render(request, 'registration/register.html', {'form':form, 'messages':messages_to_display})

def activate(request, uidb64, token):
    User = get_user_model()

    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account has been successfully activated.')
        return redirect(reverse('login'))
    else:
        messages.error(request, 'Activation link is invalid or expired. Please create your account again and check your email for account verification.')
        return redirect('index')

    
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

