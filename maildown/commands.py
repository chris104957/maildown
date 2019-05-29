from cleo.commands import Command
from maildown import backends


available_backends = dict(aws=backends.AwsBackend)


class InitCommand(Command):
    """
    Configures Maildown for use

    init
        {--backend=aws : The email backend to use. Defaults to AWS SES }
        {options?* : Arguments to pass to the backend's login methods, e.g. `access_key=1234`}

    """

    def handle(self):
        __backend = available_backends.get(self.option("backend"))
        if not __backend:
            return self.line(
                f'No backend called {self.option("backend")} exists', "error"
            )

        backend = __backend()
        kwargs = dict()
        for arg in self.argument("options"):
            key, val = arg.split("=")
            kwargs[key] = val

        backend.login(**kwargs)
        self.info("Initiated successfully")


class VerifyCommand(Command):
    """
    Verifies your ownership of an email address. Must be done prior to sending any messages

    verify
        {email-address : The email address that you want to verify}
        {--backend=aws : The email backend to use. Defaults to AWS SES }
    """

    def handle(self):
        email = self.argument("email-address")
        __backend = available_backends.get(self.option("backend"))
        if not __backend:
            return self.line(
                f'No backend called {self.option("backend")} exists', "error"
            )
        backend = __backend()

        verified = backend.verify_address(email)

        if verified:
            self.info("This email address has already been verified")

        else:
            self.info(
                f"Email sent to {email}. You must click the link in this email to verify ownership before "
                f"you can send any emails"
            )


class SendCommand(Command):
    """
    Send an email to a list of recipients

    send
        {sender : The source email address (you must have verified ownership)}
        {subject : The subject line of the email}
        {--c|content=? : The content of the email to send}
        {--backend=aws : The email backend to use. Defaults to AWS SES }
        {--f|file-path=? : A path to a file containing content to send}
        {--t|theme=? : A path to a css file to be applied to the email}
        {--e|variable=* : Context variables to pass to the email, e.g. `-e name=Chris`}
        {recipients?* : A list of email addresses to send the mail to}
    """

    def handle(self):
        __backend = available_backends.get(self.option("backend"))
        if not __backend:
            return self.line(
                f'No backend called {self.option("backend")} exists', "error"
            )
        backend = __backend()

        sender = self.argument("sender")
        subject = self.argument("subject")

        content = self.option("content")
        file_path = self.option("file-path")
        theme = self.option("theme")
        recipients = self.argument("recipients")

        variables = self.option("variable")
        environment = dict()
        for var in variables:
            key, val = var.split("=")
            environment[key] = val

        if not recipients:
            self.line("You must supply at least one recipient", "error")
            return

        if not any([content, file_path]) or all([content, file_path]):
            self.line(
                "You must provide either the content or file_path argument only",
                "error",
            )
            return

        kwargs = dict(
            sender=sender,
            subject=subject,
            content=content,
            file_path=file_path,
            to=recipients,
            context=environment,
        )
        if theme:
            kwargs["theme"] = theme

        backend.send(**kwargs)
        self.info("Messages added to queue")
