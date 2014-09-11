from main.controllers import BaseView, SignupForm, Player_Confirmation, render, HttpResponse, Player, redirect, AccountConfirmationForm, binascii, os, User

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
                send_email(pc.email, pc.confirmation_token) 
            else:
                print pc.confirmation_token

            return render(request, 'signup_accepted.html', {'email': pc.email})
        else:
            return render(request, 'signup.html', {'form': form})

class ConfirmAccountView(BaseView):
    form_class = AccountConfirmationForm

    def get(self, request, token):
        pc = Player_Confirmation.objects.get(confirmation_token=token)
        form = self.form_class()
        model = {'token': token, 'player_confirmation': pc, 'form': form}
        self.addWeeksToModel(model)
        return render(request, 'confirm_account.html', model)

    def post(self, request, token):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                pc = Player_Confirmation.objects.get(confirmation_token=token)
            except Player_Confirmation.DoesNotExist:
                return HttpResponse(status=404)

            user = User.objects.create_user(pc.username, pc.email, form.cleaned_data['password'])
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
            pc.delete()
            return redirect('/login?confirmed=true')
        else:
            pc = Player_Confirmation.objects.get(confirmation_token=token)
            return render(request, 'confirm_account.html', {'token': token, 'player_confirmation': pc, 'form': form})