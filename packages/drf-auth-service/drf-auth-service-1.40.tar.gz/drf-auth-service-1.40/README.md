# Django Rest Framework Authorization Service


## Overview :lock:

**An authentication service** orchestrates single sign-on (SSO) between multiple apps.
If the user has already signed on to one app, the login page will not be shown again and the user will be logged in via this service.

**Single sign-on (SSO)** is an authentication scheme that allows a user to log in with
a single ID and password to any of several related, yet independent, software systems.

### Features :zap:
- [X] Register and login by different register_types: email, phone_number, phone_number_code and nickname
- [X] Register with confirmation flow managed by a **RegisterBackend**
- [X] Reset Password with multiple options **phone/email** managed by register_type of user
- [X] Social authentication **~~Apple~~/Facebook/Google**
- [X] **Service** model approach for login and register
- [X] User **edit/block/unblock/set-password/resend-confirmation/delete** feature based on a Secret Token
- [X] Customizable


## Integration workflow

### Registration with confirmation

![Register](./docs/register.jpeg)

### Login

![Register](./docs/login.jpeg)

### Restore password

![Register](./docs/restore.jpeg)

### Refresh expired access token

![Register](./docs/refresh.jpeg)


## Installation

Install using `pip`...

    pip install drf-auth-service

Add `'drf_auth_service'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = [
        ...
        'drf_auth_service',
    ]

Add package urls to your application `urls.py` file.

    urlpatterns = [
        path("", include("drf_auth_service.urls"))
    ]

Before project start run migrate of database...


    ./manage.py migrate


## Configuration

Configuration for DRF Auth Service is all namespaced inside a single Django setting, named DRF_AUTH_SERVICE.

For example your project's settings.py file might include something like this:

    DRF_AUTH_SERVICE = {
        'WORK_MODE': 'standalone',
        'REGISTER_TYPES': [],
        'SEND_CONFIRMATION': True
    }


## Available Settings :mag_right:

| Key | Description | Default
| ---     | --- | --- |
|`WORK_MODE` | Mode of service | `standalone`
|`REGISTER_TYPES` | Available register types | `['email', 'phone_number', 'phone_number_code', 'nickname']`
|`SEND_CONFIRMATION` | Boolean if you want to send confirmation on register | `True`
|`DOMAIN_ADDRESS` | Common domain address used in Single Sign On authentication | `None` 
|`RESET_PASSWORD_EXPIRE` | Token expiration hours for reset password and confirmation token | `24`
|`SEND_RESET_PASSWORD_URL` | Base url where is append token | `https://example.com/reset-password/`
|`SEND_CONFIRMATION_URL` | Base url where is append token | `https://example.com/confirm-email`
|`SMS_CONFIRMATION_MESSAGE` | Sms message on confirmation | `Confirmation code {{ code }}`
|`SMS_RESET_PASSWORD_MESSAGE` | Sms message on reset password | `Reset password code {{ code }}`
|`HTML_DEFAULT_FROM_EMAIL` | From address in sending emails | EMAIL_USERNAME value
|`HTML_RESET_PASSWORD_SUBJECT` | Subject on reset password email | `Reset password`
|`HTML_CONFIRMATION_SUBJECT` | Subject on confirmation email | `Confirm account`
|`HTML_EMAIL_RESET_TEMPLATE` | Path to reset password template if no one is defined, default is used | internal template
|`HTML_EMAIL_CONFIRM_TEMPLATE` | Path to confirmation template if no one is defined, default is used | internal template
|`SENDINBLUE_RESET_PASS_TEMPLATE` | Template ID for reset password from sendinblue service | `None` 
|`SENDINBLUE_CONFIRMATION_TEMPLATE` | Template ID for confirmation from sendinblue service | `None` 
|`SENDINBLUE_API_KEY` | SendInBlue API_KEY | `None` 
|`MAILCHIMP_RESET_PASS_TEMPLATE` | Template ID for reset password from Mailchimp service | `None` 
|`MAILCHIMP_CONFIRMATION_TEMPLATE` | Template ID for confirmation from Mailchimp service | `None` 
|`MAILCHIMP_USERNAME` | Mailchimp Username | `None` 
|`MAILCHIMP_SECRET_KEY` | Mailchimp SECRET_KEY | `None` 
|`TWILIO_ACCOUNT_SID` | Twilio SID | `None` 
|`TWILIO_AUTH_TOKEN` | Twilio TOKEN | `None` 
|`TWILIO_FROM_NUMBER` | Twilio from phone number | `None`
|`EMAIL_HOST` | Email SMTP host | Django EMAIL_HOST value
|`EMAIL_PORT` | Email SMTP port | Django EMAIL_HOST value
|`EMAIL_USERNAME` | Email SMTP username | Django EMAIL_HOST_USER value
|`EMAIL_PASSWORD` | Email SMTP password | Django EMAIL_HOST_PASSWORD value
|`EMAIL_USE_TLS` | Email SMTP TLS use | Django EMAIL_USE_TLS value
|`SERIALIZERS` | Here is a Dict of serializers that you can override
|`VIEWS` | Here is a Dict of views that you can override
|`PERMISSIONS` | Here is a Dict of permissions that you can override
|`BACKENDS` | Here is a Dict of backends that you can override
|`ENUMS` | Here is a Dict of enums that you can override

## Customization

### Change User model :family:

User model is based on swappable settings from Django model and to config your own model
of user you just have to give model to `AUTH_USER_MODEL = 'my_application.CustomUser'`

```python
from drf_auth_service.models import AbstractSSOUser

# Add phone number to user table
class CustomUser(AbstractSSOUser):
    phone_number = models.CharField(max_length=120)
```

### Create a new registration backend :package:

In case you want to use your own backends you will have to override 

```python
from drf_auth_service.common.backends import BaseBackend
from drf_auth_service.common.managers import PhoneManager

class CustomRegisterBackend(BaseBackend):
    name = 'email'
    manager = PhoneManager

    # This method will be called on register
    def register_user(self):
        user = get_user_model().objects.create(
            service=self.request.service,
            register_type=self.name,
            username=self.request.data['username'],
            
            # insert with new field value
            phone_number=self.request.data['phone_number']
        )
    
        # return created user
        return user
```

In order to work with **RegisterBacked** it's a must to inherit **BaseBackend** from sso package:
- name: register_type name, based on this name received in register body will identify what register backend to use
- manager: What manager **(PhoneManager/EmailManager)** to use for sending confirmation in case you have this functionality 


Change Register Backend in setting.py:

```python
DRF_AUTH_SERVICE = {
    'BACKENDS': {
        'REGISTER_BACKENDS': ['my_application.backends.CustomRegisterBackend']
    }
}
```
 
### Create a new SMS backend :envelope:

At the moment we have only **TwilioBackend** which can be easily change with

```python
from drf_auth_service.common.sms_backends import TwilioBackend

class CustomPhoneProvider(TwilioBackend):

    def send(self, to_phone, message, from_phone=None):
        response = requests.post('http://anothersmsprovider.com/send', data={
            to_phone_number=f"+{to_phone}",
            from_phone_number=from_phone,
            body=message
        })
    
        if not response.is_ok:
            raise ValidationError(dict(details=response.json()))

```

Change SMS Backend in setting.py:

```python
DRF_AUTH_SERVICE = {
    'BACKENDS': {
        'SMS_BACKEND': ['my_application.backends.CustomPhoneProvider']
    }
}
```

### Change the Email Backend :mailbox_closed:

We have 3 options for email backends **(MailchimpBackend/SendInBlueBackend/HtmlTemplateBackend)** 
with default **HtmlTemplateBackend**, in order to change or add new backend just add to sso settings

```python
DRF_AUTH_SERVICE = {
    'BACKENDS': {
        'EMAIL_BACKEND': ['drf_auth_service.common.email_backends.SendInBlueBackend']
    }
}
```

### Change Views/Serializers/Permissions

Every view/serializer/permission can be change from package settings and a good example how to do this:

1. Create new serializer

```python
class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    username = serializers.EmailField(required=True)
    register_type = serializers.HiddenField(default=RegisterType.EMAIL)

    def validate(self, attrs):
        user_exists = get_user_model().objects.filter(
            username=attrs['username'], 
            service=self.context['request'].service
        ).exists()

        if user_exists:
            raise ValidationError({'username': f"User '{attrs['username']}' already exists"})

        return attrs
``` 

2. Change Serializer in setting.py:

```python
DRF_AUTH_SERVICE = {
    'SERIALIZERS': {
        'REGISTER_SERIALIZER': "apps.authentication.serializers.RegisterSerializer"
    }
}
```