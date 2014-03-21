class SecuredStaticFlask(Flask):
    def send_static_file(self, filename):
        protected_templates = ['partials/dashboard.html', 'partials/onboarding/stick.html']
        # Get user from session
        if current_user.is_authenticated() or filename not in protected_templates:
            return super(SecuredStaticFlask, self).send_static_file(filename)
        else:
            return redirect('/static/partials/login.html')
