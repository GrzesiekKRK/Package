
def navbar_context(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)[:5]
        notifications_count = request.user.notifications.filter(is_read=False).count()
    else:
        notifications = []
        notifications_count = 0

    return {
        'notifications': notifications,
        'notifications_count': notifications_count,
    }
