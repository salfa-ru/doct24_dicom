from rest_framework.permissions import SAFE_METHODS, BasePermission
from api_consultation_app.models import Consultation
from api_patient_app.models import Patient
from api_doctor_app.models import Doctor
from django.shortcuts import get_object_or_404


class IsPatientAuthorOrReadOnly(BasePermission):
    """Авторизованный пациент является владельцем объекта,
    либо используется метод GET для любых пользователей."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.patient.user == request.user
                )
            )
        )


class IsDoctorOwnerOrReadOnly(BasePermission):
    """Авторизованный доктор является владельцем объекта
    либо чтение для любых пользователей."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.doctor.user == request.user
                )
            )
        )


class PatientOwnerOrHisDoctorReadOnly(BasePermission):
    """Доступно только авторизованному пациенту и 
    доктору, к которому этот пациент хоть раз записывался
    на консультацию. ТОЛЬКО ЧТЕНИЕ."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            and (
                request.user.is_authenticated
                and (
                    obj.user == request.user
                    or Consultation.objects.filter(doctor__user=request.user, patient=obj).exists()
                )
            )
        )


class PatientOwnerOrHisDoctorReadAndWrite(BasePermission):
    """Для метода update консультаций. Доступ
    у авторизованного пациента и доктора конкретного
    объекта консультаций."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.patient.user == request.user
                    or obj.doctor.user == request.user
                )
            )
        )


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and Patient.objects.filter(user=request.user).exists()
        )


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and Doctor.objects.filter(user=request.user).exists()
        )


class IsDoctorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and Doctor.objects.filter(user=request.user).exists()
            )
        )


class FilesForConsultation(BasePermission):
    """Для создания файлов ТОЛЬКО в своих консультациях."""

    def has_permission(self, request, view):
        consultation = get_object_or_404(Consultation, pk=view.kwargs.get('consultation_id'))
        return (
            request.user.is_authenticated
            and request.user in (consultation.patient.user, consultation.doctor.user)
        )


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator