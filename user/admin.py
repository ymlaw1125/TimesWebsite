from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from magazines.models import Magazine
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # pass
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Other", {"fields": ("magazine_favorites",)})
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    filter_horizontal = (
        "groups",
        "user_permissions",
        "magazine_favorites",
    )


admin.site.register(CustomUser, CustomUserAdmin)
