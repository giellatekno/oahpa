from oahpa.drill.models import Log, Word, Semtype
from django.contrib import admin
from django.contrib.contenttypes import generic

class LogAdmin(admin.ModelAdmin):
    list_display = ('example','userinput','iscorrect','correct','game','date')
        
class WordAdmin(admin.ModelAdmin):

    list_display = ('lemma','wordid','pos','stem', 'diphthong','gradation','rime','soggi','valency')
    list_filter = ['pos','stem','semtype','source'] 
    search_fields = ['lemma', 'semtype__semtype']

admin.site.register(Word,WordAdmin)
admin.site.register(Log, LogAdmin)


