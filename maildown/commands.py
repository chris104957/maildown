from cleo.commands import Command
from maildown import utilities


class InitCommand(Command):
    """
    Configures Maildown for use

    init
        {access-key? : Your AWS Access Key ID}
        {secret-key? : Your AWS Secret key}
        {region? : AWS region to use (defaults to "us-east-1")}
        {aws-config-file? : Path to your AWS config file (defaults to ~/.aws/credentials}
    """

    def handle(self):
        kwargs = dict()
        access_key = self.argument("access-key")
        secret_key = self.argument("secret-key")
        region = self.argument("region")
        aws_config_file = self.argument("aws-config-file")

        if access_key:
            kwargs["access_key"] = access_key

        if secret_key:
            kwargs["secret_key"] = secret_key

        if region:
            kwargs["region"] = region

        if aws_config_file:
            kwargs["aws_config_file"] = aws_config_file

        utilities.login(**kwargs)
        self.info("Successfully set AWS credentials")


class VerifyCommand(Command):
    """
    Verifies your ownership of an email address. Must be done prior to sending any messages

    verify
        {email-address : The email address that you want to verify}
    """

    def handle(self):
        email = self.argument("email-address")
        verified = utilities.verify_address(email)

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
        {--f|file-path=? : A path to a file containing content to send}
        {--t|theme=? : A path to a css file to be applied to the email}
        {recipients?* : A list of email addresses to send the mail to}
    """

    def handle(self):
        sender = self.argument("sender")
        subject = self.argument("subject")

        content = self.option("content")
        file_path = self.option("file-path")
        theme = self.option("theme")
        recipients = self.argument("recipients")

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
        )
        if theme:
            kwargs["theme"] = theme

        utilities.send_message(**kwargs)
        self.info("Messages added to queue")
