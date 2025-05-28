from rest_framework import permissions


class IsPatientOwner(permissions.BasePermission):
    """
    Allows access only if the requesting user is the owner of the health record.
    Intended for use on objects that contain a `patient` field.
    """

    def has_object_permission(self, request, view, obj):
        return (
            hasattr(request.user, "patient_profile")
            and obj.patient == request.user.patient_profile
        )


class IsDoctorAssignedToPatient(permissions.BasePermission):
    """
    Allows access only if the doctor is assigned to the patient associated with the object.
    Intended for use on objects that contain a `patient` field.
    """

    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, "doctor_profile") and obj.patient in [
            a.patient for a in request.user.doctor_profile.assigned_patients.all()
        ]
