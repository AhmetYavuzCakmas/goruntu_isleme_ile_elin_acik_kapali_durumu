import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#görüntüler için:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands = 2,
    min_detection_confidence=0.5
)as hands:
    for idx, file in enumerate(IMAGE_FILES):
        #bir görseli okuyup doğru kullanım için ters çevirme
        image= cv2.flip(cv2.imread(file),1)
        #resmi BGB den RGB ye aktarma
        results = hands.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))

        #El tercihini yazdırma ve görüntünün üzerine el işaretini çizim..
        print('Handedness: ',results.multi_handedness)
        if not results.multi_hand_landmarks:
            continue
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            print('hand_landmarks: ',hand_landmarks)
            print(
                f'Index finger tip coordinates:(',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width},'
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
            )
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        cv2.imwrite(
            '/tmp/annotated_image'+str(idx)+ '.png', cv2.flip(annotated_image,1))
        
#webcam açmak için:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence= 0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            #if loading a vieo, use 'break' instead of 'continue'.
            continue

        #daha sonraki bir özçekim görüntüsü için görüntüyü yatay olarak çevirme
        #BGR görüntüyü RGB ye aktarma.
        image = cv2.cvtColor(cv2.flip(image, 1),cv2.COLOR_BGR2RGB)
        #to improve performance , optionally mark the image as not writeable to
        #pass by reference
        image.flags.writeable= False
        results = hands.process(image)

        #el açılmalarını görüntünün üzerine yerleştiriyorum.
        image.flags.writeable  =True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
            

                #el açık  ve kapalı iken ekrana yazdırma
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
                x1, y1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

                font = cv2.FONT_HERSHEY_PLAIN

                if y1>y:
                    cv2.putText(image,"KAPALI",(10,50), font,4,(0,0,0),3)
                else:
                    cv2.putText(image,"ACIK",(10,50), font,4,(0,0,0),3)

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()