from apps.good_apply.models import Secretary


def is_secretary(username):
    if Secretary.objects.filter(username=username).exists():
        return True
    return False
