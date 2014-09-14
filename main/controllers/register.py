from main.controllers import *

class SignupView(BaseView):
    form_class = SignupForm
    template = 'signup.html'

    def doGet(self, request):
        form = self.form_class()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pc = Player_Confirmation()
            pc.username = form.cleaned_data['username'].lower()
            pc.email = form.cleaned_data['email'].lower()
            pc.confirmation_token = binascii.hexlify(os.urandom(16))
            pc.save()

            if 'USE_LOCAL_DB' not in os.environ:
                self.send_email(pc.email, pc.confirmation_token) 
            else:
                print pc.confirmation_token

            return render(request, 'signup_accepted.html', {'email': pc.email})
        else:
            return render(request, 'signup.html', {'form': form})

    def send_email(self, email, token):
        import os
        import smtplib

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')

        msg['Subject'] = "Welcome to the Columbia Pinball League."
        msg['From']    = "Como Pinball League <como.pinball.league@gmail.com>" # Your from name and email address
        msg['To']      = email

        html = '<p>Thank you for signing up for the Columbia Pinball League.  <p><a href="http://como-pinball-league.herokuapp.com/confirmAccount/%s">Click here</a> to finish creating your account.' % token
        part2 = MIMEText(html, 'html')

        username = os.environ['MANDRILL_USERNAME']
        password = os.environ['MANDRILL_APIKEY']

        msg.attach(part2)

        s = smtplib.SMTP('smtp.mandrillapp.com', 587)

        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())

        s.quit()
        return HttpResponse(status=200)

def create_player(username, email, form):
    user = User.objects.create_user(username, email, form.cleaned_data['password'])
    user.first_name = form.cleaned_data['first_name'].lower()
    user.last_name = form.cleaned_data['last_name'].lower()
    user.save()
    
    player = Player()
    player.first_name = user.first_name
    player.last_name = user.last_name
    player.signature = form.cleaned_data['signature'].upper()
    player.ifpa_id = form.cleaned_data['ifpa_id']
    player.user = user
    player.save()
    return player

class ConfirmAccountView(BaseView):
    form_class = AccountConfirmationForm
    template = 'confirm_account.html'

    def get(self, request, token):
        pc = Player_Confirmation.objects.get(confirmation_token=token)
        form = self.form_class()
        model = {'token': token, 'player_confirmation': pc, 'form': form, 'action': '/confirmAccount/%s' % (token)}
        self.addWeeksToModel(model)
        return render(request, self.template, model)

    def post(self, request, token):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                pc = Player_Confirmation.objects.get(confirmation_token=token)
            except Player_Confirmation.DoesNotExist:
                return HttpResponse(status=404)
            create_player(pc.username, pc.email, form)
            pc.delete()
            return redirect('/login?confirmed=true')
        else:
            pc = Player_Confirmation.objects.get(confirmation_token=token)
            return render(request, self.template, {'token': token, 'player_confirmation': pc, 'form': form})

class AddPlayerView(BaseView):
    form_class = AddPlayerForm
    template = 'confirm_account.html'
    action = 'addPlayer'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form, 'action': self.action})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            player = create_player(form.cleaned_data['username'], form.cleaned_data['password'], form)
            return render(request, 'player_added.html', {'player': player})
        else:
            return render(request, self.template, {'form': form, 'action': self.action})
