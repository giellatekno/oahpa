from django import template

register = template.Library()

@register.filter(name='complete_for')
def complete_for(a, user):
    return a.user_completed(user)

@register.filter(name='goal_instances_for')
def goal_instances_for(instances, username):
    return instances.filter(user__username=username)

@register.filter(name='format_percent')
def format_percent(_float):
    _perc = "%s" % (_float*100).to_eng_string()
    return _perc + '%'

