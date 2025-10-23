import cv2
import numpy as np

# Thank you Codsoft for giving me this opportunity

# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create the LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load training images
person_1 = cv2.imread(r"C:\Users\SHUBHAM SHARMA\Desktop\programming\python\project.py\gandi sakal\WhatsApp Image 2025-02-09 at 2.32.33 PM.jpeg")
person_2 = cv2.imread(r"C:\Users\SHUBHAM SHARMA\Desktop\programming\python\project.py\gandi sakal\WhatsApp Image 2025-02-09 at 2.32.32 PM.jpeg")

# Check if images loaded successfully
if person_1 is None or person_2 is None:
    print("Error: One or more images failed to load.")
    exit()

# Convert images to grayscale
gray_person_1 = cv2.cvtColor(person_1, cv2.COLOR_BGR2GRAY)
gray_person_2 = cv2.cvtColor(person_2, cv2.COLOR_BGR2GRAY)

# Function to detect and resize face
def detect_and_resize_face(gray_image):
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return None
    (x, y, w, h) = faces[0]
    face_roi = gray_image[y:y+h, x:x+w]
    resized_face = cv2.resize(face_roi, (200, 200))  # Standard size for recognizer
    return resized_face

# Detect and prepare training data
face1 = detect_and_resize_face(gray_person_1)
face2 = detect_and_resize_face(gray_person_2)

if face1 is None or face2 is None:
    print("Error: Could not detect faces in one or both training images.")
    exit()

faces = [face1, face2]
labels = [0, 1]

# Train the recognizer
recognizer.train(faces, np.array(labels))

# Label names
names = ["Krish Sharma", "Katapa"]

# Start video capture
video_capture = cv2.VideoCapture(0)

print("Face recognition started. Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame from webcam. Exiting...")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_detected = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces_detected:
        roi_gray = gray_frame[y:y+h, x:x+w]
        try:
            roi_resized = cv2.resize(roi_gray, (200, 200))
            label, confidence = recognizer.predict(roi_resized)

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display name and confidence
            text = f'{names[label]} ({round(confidence, 2)})'
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        except Exception as e:
            print(f"Prediction error: {e}")

    # Display the frame
    cv2.imshow('Video', frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
