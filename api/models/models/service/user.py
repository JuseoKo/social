from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self, user_id, email, phone_number, nickname, password=None):
        if not user_id:
            raise ValueError("must have user email")
        if not email:
            raise ValueError("must have user email")
        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            nickname=nickname,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, nickname, phone_number, password):
        user = self.create_user(
            user_id=user_id,
            email=self.normalize_email(email),
            nickname=nickname,
            phone_number=phone_number,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.CharField(
        max_length=30, null=False, unique=True, verbose_name="아이디"
    )
    email = models.EmailField(
        max_length=255, null=True, unique=True, verbose_name="email"
    )
    nickname = models.CharField(
        max_length=255, null=False, unique=True, verbose_name="닉네임"
    )
    phone_number = models.CharField(max_length=11, null=True, verbose_name="전화 번호")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["email", "phone_number", "nickname"]
    objects = UserManager()

    class Meta:
        db_table = "users"

    # 권한 설정
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
