from myv_oahpa.myv_drill.models import Log, Word, Semtype, Source, Form, Tag, Feedbackmsg, Feedbacktext, Question, QElement, WordQElement, WordTranslation
from django.contrib import admin
from django.contrib.contenttypes import generic

class LogAdmin(admin.ModelAdmin):
	list_display = ('example','userinput','iscorrect','correct','game','date')


class FormInline(admin.TabularInline):
	model = Form

# TODO:
# class WordTranslationInline(admin.TabularInline):
# 	model = WordTranslation.word.through
# 	raw_id_fields = ('wordnob',)

class WordAdmin(admin.ModelAdmin):
	list_display = ('lemma','wordid','pos','stem', 'sem_types_admin', 'source_admin') #, 'soggi', 'valency')
	list_filter = ['pos','stem','semtype','source'] #, 'soggi'] 
	search_fields = ['lemma', 'semtype__semtype']
	inlines = [FormInline] # TODO: , WordTranslationInline]
	# raw_id_fields = ('wordtranslation_set', )
	# raw_id_fields = ['translations2nob']

class FormAdmin(admin.ModelAdmin):
	# list_display = ('fullform', 'tag',)
	# list_display = ('fullform', )
	# list_filter = list(list_display)
	search_fields = ['fullform']


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ['pos', 'stem', 'tense'] # commented out soggi


admin.site.register(Form, FormAdmin)
admin.site.register(Source)
admin.site.register(Tag)
admin.site.register(Semtype)
admin.site.register(Question)
admin.site.register(QElement)
admin.site.register(WordQElement)
admin.site.register(Feedbacktext)
admin.site.register(Feedbackmsg)
admin.site.register(Word, WordAdmin)
admin.site.register(Log, LogAdmin)

