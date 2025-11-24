from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager


# ---------------------------------------------------------
# User Manager
# ---------------------------------------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", 1)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        # extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("role")==1:
            raise ValueError("Superuser must have role=1.")

        return self.create_user(email, password, **extra_fields)


# ---------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------
class User(AbstractBaseUser):

    # ---------- Core ----------
    id = models.BigAutoField(primary_key=True)

    role = models.CharField(
        max_length=50,
        choices=[
            ("superadmin", "1"),
            ("admin", "2"),
            ("consumer", "3"),
            ("provider", "4"),
            ("service_person", "5"),
        ],
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # ---------- Authentication Fields ----------
    user_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verify = models.BooleanField(default=False)

    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    mobile_verify = models.BooleanField(default=False)

    mobile_number_2 = models.CharField(max_length=20, blank=True, null=True)

    password = models.CharField(max_length=255)

    # ---------- Personal Info ----------
    about = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    gender = models.CharField(
        max_length=20,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        blank=True,
        null=True,
    )

    # ---------- Address ----------
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)

    pincode = models.CharField(max_length=20, blank=True, null=True)
    isd_code = models.CharField(max_length=10, blank=True, null=True)

    location_id = models.CharField(max_length=100, blank=True, null=True)

    # ---------- Geo ----------
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    auto_city = models.CharField(max_length=150, blank=True, null=True)
    auto_state = models.CharField(max_length=150, blank=True, null=True)
    auto_country = models.CharField(max_length=150, blank=True, null=True)
    auto_ip = models.GenericIPAddressField(blank=True, null=True)

    # ---------- Media ----------
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)

    identity_proof_type = models.CharField(max_length=50, blank=True, null=True)
    identity_proof_doc = models.FileField(upload_to="identity_docs/", blank=True, null=True)

    # ---------- External Auth ----------
    google_status = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    # ---------- Device ----------
    device_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[("android", "Android"), ("ios", "iOS"), ("web", "Web")],
    )

    # ---------- Other ----------
    website_url = models.URLField(blank=True, null=True)
    referal_code = models.CharField(max_length=50, blank=True, null=True)

    # ---------- Timestamps ----------
    last_login = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    objects = UserManager()

    class Meta:
        # managed = False
        db_table = "task_buddy_users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["mobile_number"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.role

    def has_module_perms(self, app_label):
        return self.role




## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++# End of File
## ++++++++++++++++++++++ Below model is for ideation ++++++++++++++++++++++++++++++++++++

from django.db import models
from django.conf import settings
from django.utils import timezone


# Optional: shared timestamp base
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ============================
# Address
# ============================
class Address(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    label = models.CharField(max_length=50, blank=True, null=True)  # e.g. home, work
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, blank=True, null=True)
    line_3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_default"]),
            models.Index(fields=["city", "state"]),
        ]

    def __str__(self):
        return f"{self.line_1}, {self.city or ''}".strip(", ")


# ============================
# Service Provider
# ============================
class ServiceProvider(TimeStampedModel):
    """
    Company/organization that provides services.
    Linked 1:1 to a User with role='provider'.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile",
        limit_choices_to={"role": "provider"},
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    # provider-level admins (users who can manage this provider)
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProviderAdmin",
        related_name="admin_of_providers",
        blank=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class ProviderAdmin(models.Model):
    """
    Many-to-many join between ServiceProvider and User for provider-level admins.
    """
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role_at_provider = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("provider", "user")
        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user} admin for {self.provider}"


# ============================
# Service Person
# ============================
class ServicePerson(TimeStampedModel):
    STATUS_ACTIVE = "active"
    STATUS_SUSPENDED = "suspended"
    STATUS_INACTIVE = "inactive"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_person_profile",
        limit_choices_to={"role": "service_person"},
    )
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_persons",
        help_text="If null, this service person is independent.",
    )
    job_title = models.CharField(max_length=120, blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)  # e.g. ["plumbing", "cleaning"]
    phone = models.CharField(max_length=30, blank=True, null=True)
    license_number = models.CharField(max_length=128, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=30,
        choices=[
            (STATUS_ACTIVE, "Active"),
            (STATUS_SUSPENDED, "Suspended"),
            (STATUS_INACTIVE, "Inactive"),
        ],
        default=STATUS_ACTIVE,
    )
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["is_available", "status"]),
        ]

    def __str__(self):
        return self.user.user_name or self.user.email

    def belongs_to_provider(self) -> bool:
        return self.provider_id is not None


# ============================
# Consumer
# ============================
class Consumer(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consumer_profile",
        limit_choices_to={"role": "consumer"},
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    default_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    preferences = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return self.user.user_name or self.user.email


# ============================
# Device
# ============================
class Device(TimeStampedModel):
    DEVICE_ANDROID = "android"
    DEVICE_IOS = "ios"
    DEVICE_WEB = "web"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices",
    )
    device_type = models.CharField(
        max_length=20,
        choices=[
            (DEVICE_ANDROID, "Android"),
            (DEVICE_IOS, "iOS"),
            (DEVICE_WEB, "Web"),
        ],
    )
    device_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Push token or device identifier",
    )
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["user", "device_type"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.device_type}"


# ============================
# Service catalog
# ============================
class ServiceCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
    )
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # which providers offer this service
    providers = models.ManyToManyField(
        ServiceProvider,
        related_name="services",
        blank=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return self.title


# ============================
# Booking (Jobs)
# ============================
class Booking(TimeStampedModel):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    consumer = models.ForeignKey(
        Consumer,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings",
    )
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bookings",
    )
    service_person = models.ForeignKey(
        ServicePerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )

    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=30,
        choices=[
            (STATUS_PENDING, "Pending"),
            (STATUS_ACCEPTED, "Accepted"),
            (STATUS_IN_PROGRESS, "In progress"),
            (STATUS_COMPLETED, "Completed"),
            (STATUS_CANCELLED, "Cancelled"),
        ],
        default=STATUS_PENDING,
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["consumer"]),
            models.Index(fields=["provider"]),
            models.Index(fields=["status"]),
            models.Index(fields=["scheduled_at"]),
        ]

    def __str__(self):
        return f"Booking #{self.id} - {self.service or ''}".strip(" -")
