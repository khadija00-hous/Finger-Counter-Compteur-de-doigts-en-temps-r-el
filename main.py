import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        count = fingers.count(1)

        print(count)

        cv2.putText(img, str(count), (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (255, 0, 0), 5)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break