from django.core.exceptions import ValidationError

import requests
import re
import uuid

from .settings import MEDIA_ROOT

email_pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
def validate_email(value):
    if re.match(email_pattern, value):
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}-{1}/{2}'.format(instance.id, str(uuid.uuid4()),filename)

def upload_image_to_user_path(profile, image_url):
    try:
        response = requests.get(image_url)
        filepath = MEDIA_ROOT + user_directory_path(profile, filename= profile.email.split("@")[0])
        file = open(filepath, "wb")
        file.write(response.content)
        file.close()
        return filepath
    except:
        raise ValueError("Can not save profile image")