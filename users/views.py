from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from posts.models import Post
from .forms import SignUpForm, ProfileForm
from .models import CustomUser
from DjangoGramm import settings

User = get_user_model()


def profile_view(request, username):
    # Get the user whose profile we are visiting
    profile_user = get_object_or_404(User, username=username)
    # Get all posts by this user
    user_posts = Post.objects.filter(author=profile_user).order_by(
        '-created_at')

    return render(request, 'registration/profile.html', {
        'profile_user': profile_user,
        'posts': user_posts,
    })



class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email is confirmed
            user.save()

            # Generate token and link
            current_site = get_current_site(request)
            subject = 'Activate Your DjangoGramm Account'

            # Use 'https' if you have SSL, otherwise 'http'
            protocol = 'https' if request.is_secure() else 'http'

            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
            }

            message = render_to_string('registration/acc_active_email.html',
                                       context)

            # Send the real email
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error and perhaps show a message to the user
                print(f"Email failed: {e}")

            # message = render_to_string('registration/acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })

            #email sender
            # send_mail(
            #     subject,
            #     message,
            #     'admin@djangogramm.com',
            #     [user.email],
            #     fail_silently=False, # This will throw an error if the email fails
            # )

            # link is printed to terminal
            #user.email_user(subject, message)

            return render(request, 'registration/signup_done.html')
        return render(request, 'registration/signup.html', {'form': form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,
                                                                    token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('profile_setup')  # Redirect to step 2
        else:
            return render(request, 'registration/activation_invalid.html')


class ProfileSetupView(LoginRequiredMixin, View):
    def get(self, request):
        # The 'getattr' trick prevents a crash if the signal failed
        profile = getattr(request.user, 'profile', None)
        if not profile:
            from .models import Profile
            profile = Profile.objects.create(user=request.user)

        form = ProfileForm(instance=profile)
        return render(request, 'registration/profile_setup.html',
                      {'form': form})
        #form = ProfileForm(instance=request.user.profile)
        #return render(request, 'registration/profile_setup.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Finally enter the app
        return render(request, 'registration/profile_setup.html', {'form': form})