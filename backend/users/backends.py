from django.contrib.auth import get_user_model


User = get_user_model()


class EmailModelBackend:
    def authenticate(self, request, email=None, password=None):
        user = None

        if email is not None:
            try:
                user_ = User.objects.get(email=email)
                if user_.check_password(password):
                    user = user_
            except User.DoesNotExist:
                # waste time on purpose
                User().set_password(password)

        return user
