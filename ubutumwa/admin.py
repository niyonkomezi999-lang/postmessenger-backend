from django.contrib import admin
from .models import  MessagePublie, Follow 


class FollowAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_abonnement')
    search_fields = ['gagnant__username', 'abonne__username']
    list_filter = ('date_abonnement', 'gagnant', 'abonne',)
admin.site.register(Follow, FollowAdmin)


@admin.register(MessagePublie)
class MessagePublieAdmin(admin.ModelAdmin):
    list_display = ('poster', 'date_creation', 'contenu_court')
    list_filter = ('date_creation', 'poster')
    ordering = ['-date_creation']

    def contenu_court(self, obj):
        return obj.contenu[:50]
    contenu_court.short_description = 'Extrait du message'