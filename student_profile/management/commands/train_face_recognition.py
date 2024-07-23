from django.core.management.base import BaseCommand
from student_profile.models import StudentProfile
import face_recognition
import cv2
import numpy as np


class Command(BaseCommand):
    help = "Train face recognition model using profile pictures of students"

    def handle(self, *args, **kwargs):
        students = StudentProfile.objects.exclude(profile_picture="")
        for student in students:
            if student.profile_picture:
                image_path = student.profile_picture.path
                try:
                    # Read the image using OpenCV
                    image = cv2.imread(image_path)
                    if image is None:
                        self.stdout.write(
                            self.style.ERROR(f"Failed to load image: {image_path}")
                        )
                        continue

                    # Log image properties
                    self.stdout.write(
                        self.style.HTTP_INFO(f"Processing image: {image_path}")
                    )
                    self.stdout.write(
                        self.style.HTTP_INFO(f"Original image shape: {image.shape}")
                    )
                    self.stdout.write(
                        self.style.HTTP_INFO(f"Original image dtype: {image.dtype}")
                    )

                    # Convert image from BGR (OpenCV default) to RGB
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Log properties of converted image
                    self.stdout.write(
                        self.style.HTTP_INFO(
                            f"Converted image shape: {rgb_image.shape}"
                        )
                    )
                    self.stdout.write(
                        self.style.HTTP_INFO(
                            f"Converted image dtype: {rgb_image.dtype}"
                        )
                    )

                    # Ensure the image is of type uint8
                    if rgb_image.dtype != np.uint8:
                        rgb_image = rgb_image.astype(np.uint8)

                    # Perform face encoding
                    face_encodings = face_recognition.face_encodings(
                        rgb_image.astype("uint8"), model="large"
                    )

                    if face_encodings:
                        student.save_encoding(face_encodings[0])
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"No face found in the image of {student.full_name}"
                            )
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing image {image_path}: {e}")
                    )

        self.stdout.write(
            self.style.SUCCESS("Face recognition model trained successfully")
        )
