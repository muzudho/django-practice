# 研究view

📖 [django-allauth/allauth/account/views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)  


def _ajax_response(request, response, form=None, data=None):


class RedirectAuthenticatedUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
    def get_authenticated_redirect_url(self):


class AjaxCapableProcessFormViewMixin(object):
    def get(self, request, *args, **kwargs):
    def post(self, request, *args, **kwargs):
    def get_form(self, form_class=None):
    def _get_ajax_data_if(self):
    def get_ajax_data(self):


class LogoutFunctionalityMixin(object):
    def logout(self):


class LoginView(RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, FormView):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):

    def get_form_kwargs(self):
    def get_form_class(self):
    def form_valid(self, form):
    def get_success_url(self):
    def get_context_data(self, **kwargs):


(2)
login = LoginView.as_view()


class CloseableSignupMixin(object):
    def dispatch(self, request, *args, **kwargs):
    def is_open(self):
    def closed(self):


@method_decorator(rate_limit(action="signup"), name="dispatch")
class SignupView(
    RedirectAuthenticatedUserMixin,
    CloseableSignupMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
    def get_form_class(self):
    def get_success_url(self):
    def form_valid(self, form):
    def get_context_data(self, **kwargs):


(1)
signup = SignupView.as_view()


class ConfirmEmailView(TemplateResponseMixin, LogoutFunctionalityMixin, View):
    def get(self, *args, **kwargs):
    def post(self, *args, **kwargs):
    def login_on_confirm(self, confirmation):
    def get_object(self, queryset=None):
    def get_queryset(self):
    def get_context_data(self, **kwargs):
    def get_redirect_url(self):


(9)
confirm_email = ConfirmEmailView.as_view()


@method_decorator(rate_limit(action="manage_email"), name="dispatch")
class EmailView(AjaxCapableProcessFormViewMixin, FormView):
    def get_form_class(self):
    def dispatch(self, request, *args, **kwargs):
    def get_form_kwargs(self):
    def form_valid(self, form):
    def post(self, request, *args, **kwargs):
    def _get_email_address(self, request):
    def _action_send(self, request, *args, **kwargs):
    def _action_remove(self, request, *args, **kwargs):
    def _action_primary(self, request, *args, **kwargs):
    def get_context_data(self, **kwargs):
    def get_ajax_data(self):


(7)
email = login_required(EmailView.as_view())


@method_decorator(rate_limit(action="change_password"), name="dispatch")
class PasswordChangeView(AjaxCapableProcessFormViewMixin, FormView):
    def get_form_class(self):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):

    #

    def render_to_response(self, context, **response_kwargs):
    def get_form_kwargs(self):
    def form_valid(self, form):
    def get_context_data(self, **kwargs):


(4)
password_change = login_required(PasswordChangeView.as_view())


@method_decorator(
    # NOTE: 'change_password' (iso 'set_') is intentional, there is no need to
    # differentiate between set and change.
    rate_limit(action="change_password"),
    name="dispatch",
)
class PasswordSetView(AjaxCapableProcessFormViewMixin, FormView):

    def get_form_class(self):

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):

    #

    def render_to_response(self, context, **response_kwargs):
    def get_form_kwargs(self):
    def form_valid(self, form):
    def get_context_data(self, **kwargs):


(5)
password_set = login_required(PasswordSetView.as_view())


@method_decorator(rate_limit(action="reset_password"), name="dispatch")
class PasswordResetView(AjaxCapableProcessFormViewMixin, FormView):
    def get_form_class(self):
    def form_valid(self, form):
    def get_context_data(self, **kwargs):


(10)
password_reset = PasswordResetView.as_view()


class PasswordResetDoneView(TemplateView):
    template_name = "account/password_reset_done." + app_settings.TEMPLATE_EXTENSION


(11)
password_reset_done = PasswordResetDoneView.as_view()


@method_decorator(rate_limit(action="reset_password_from_key"), name="dispatch")
class PasswordResetFromKeyView(
    AjaxCapableProcessFormViewMixin, LogoutFunctionalityMixin, FormView
):
    def get_form_class(self):
    def dispatch(self, request, uidb36, key, **kwargs):
    def get_context_data(self, **kwargs):
    def get_form_kwargs(self):
    def form_valid(self, form):


(12)
password_reset_from_key = PasswordResetFromKeyView.as_view()


class PasswordResetFromKeyDoneView(TemplateView):


(13)
password_reset_from_key_done = PasswordResetFromKeyDoneView.as_view()


class LogoutView(TemplateResponseMixin, LogoutFunctionalityMixin, View):
    def get(self, *args, **kwargs):
    def post(self, *args, **kwargs):
    def get_context_data(self, **kwargs):
    def get_redirect_url(self):


(3)
logout = LogoutView.as_view()


class AccountInactiveView(TemplateView):


(6)
account_inactive = AccountInactiveView.as_view()


class EmailVerificationSentView(TemplateView):


(8)
email_verification_sent = EmailVerificationSentView.as_view()
