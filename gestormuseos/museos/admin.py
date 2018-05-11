from django.contrib import admin

# Register your models here.
from .models import Usuario
from .models import Museo
from .models import Favorito
from .models import Comentario
admin.site.register(Usuario)
admin.site.register(Museo)
admin.site.register(Favorito)
admin.site.register(Comentario)