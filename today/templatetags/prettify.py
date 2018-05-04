# from django import template
#
# from today.views import SPECIAL_EXERCISES_JOIN_CHARACTER
#
# register = template.Library()
#
#
# @register.filter(name='prettify')
# def prettify(value: str):
#     exercises = value.split(SPECIAL_EXERCISES_JOIN_CHARACTER)
#     htmlmarkup = '<p>{}</p>'
#     all = []
#     for e in exercises:
#         all.append(htmlmarkup.format(e))
#     return "".join(all)
