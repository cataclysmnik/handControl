import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(model_complexity=1)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

index_x, index_y = 0, 0  
smooth_index_x, smooth_index_y = 0, 0 
smooth_factor = 0.4  
scroll_active = False 
scrollup_active = False

tracked_hand_type = "Right"

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)

    if output.multi_handedness and output.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(output.multi_hand_landmarks, output.multi_handedness):
            hand_label = hand_handedness.classification[0].label
            
            if hand_label == tracked_hand_type:
                drawing_utils.draw_landmarks(frame, hand_landmarks)
                landmarks = hand_landmarks.landmark
                
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)

                    if id == 8:  # Index finger tip
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        
                        index_x = screen_width / frame_width * x
                        index_y = screen_height / frame_height * y
                        
                        smooth_index_x = smooth_index_x + smooth_factor * (index_x - smooth_index_x)
                        smooth_index_y = smooth_index_y + smooth_factor * (index_y - smooth_index_y)

                        pyautogui.moveTo(smooth_index_x, smooth_index_y)

                    if id == 4:  # Thumb tip
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        thumb_x = screen_width / frame_width * x
                        thumb_y = screen_height / frame_height * y

                        if abs(smooth_index_x - thumb_x) < 20:
                            pyautogui.click()
                            pyautogui.sleep(1)

                    if id == 10:  # Middle finger base
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))
                        mid_x = screen_width / frame_width * x
                        mid_y = screen_height / frame_height * y

                    if id == 12:  # Middle finger tip
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))
                        middle_x = screen_width / frame_width * x
                        middle_y = screen_height / frame_height * y
                        if middle_y > mid_y:
                            scroll_active = True
                        else:
                            scroll_active = False 

                    if id == 14:  # Ring finger base
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))
                        mid_x = screen_width / frame_width * x
                        mid_y = screen_height / frame_height * y

                    if id == 16:  # Ring finger tip
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))
                        middle_x = screen_width / frame_width * x
                        middle_y = screen_height / frame_height * y
                        if middle_y > mid_y:
                            scrollup_active = True
                        else:
                            scrollup_active = False

                break

    # Srolling if active
    if scroll_active:
        pyautogui.scroll(-80)
    if scrollup_active:
        pyautogui.scroll(80)

    cv2.imshow('Virtual Mouse with Continuous Down Scroll', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
