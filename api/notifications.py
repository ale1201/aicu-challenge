from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import DoctorPatientAssignment


@receiver(post_save, sender=DoctorPatientAssignment)
def notify_doctor_assignment(sender, instance, created, **kwargs):
    """
    Sends an email notification to the doctor when a new patient is assigned to the doctor.

    Params:
        sender (Model): The model class.
        instance (DoctorPatientAssignment): The actual instance being saved.
        created (bool): Whether this is a new instance.
        **kwargs: Additional keyword arguments.
    """
    if created:
        doctor_user = instance.doctor.user
        patient_name = instance.patient.user.get_full_name()

        subject = "New patient assigned"
        message = (
            f"Patient {patient_name} has been assigned to you. "
            "Please log in to the application for more information."
        )

        # Send email using built-in User.email_user method
        doctor_user.email_user(subject, message, from_email=None)

        # Log to server output for debug
        print(
            f"📧 Email sent to {doctor_user.email} notifying assignment of patient '{patient_name}'."
        )
