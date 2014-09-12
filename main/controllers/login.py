from main.controllers import * 

class LoginView(BaseView):
    template = 'login.html'

    def doGet(self, request):
        return {'confirmed': request.GET.get('confirmed')}
    
    def post(self, request):
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'status': 'notActive'})
        else:
            return render(request, 'login.html', {'status': 'failed'})

class LogoutView(BaseView):

    def get(self, request):
        logout(request)
        return redirect('/')