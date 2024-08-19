from django.utils import timezone
from django.contrib.auth import get_user_model
from background_task import background

@background(schedule=60)
def unactivated_user_timeout():
    print('DELETING INACTIVE USERS...')
    User = get_user_model()
        
    recent_users = User.objects.filter(
        date_joined__lt = timezone.now() - timezone.timedelta(seconds=10800), # this gives the user 3 hours to verify their email
    )

    for user in recent_users:
        if user.is_active == False:
            user.delete()
