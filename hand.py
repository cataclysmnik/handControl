import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Initialize index finger coordinates
index_x, index_y = 0, 0  
smooth_index_x, smooth_index_y = 0, 0  # Smoothed coordinates
smooth_factor = 0.4  # Adjust this value for smoother or more responsive movements
scroll_active = False  # Track if scrolling is active
scrollup_active = False

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Index finger (id == 8)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Map the index finger's position to the screen coordinates
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    
                    # Apply smoothing using exponential moving average (EMA)
                    smooth_index_x = smooth_index_x + smooth_factor * (index_x - smooth_index_x)
                    smooth_index_y = smooth_index_y + smooth_factor * (index_y - smooth_index_y)
                    
                    # Move mouse cursor to the smoothed position
                    pyautogui.moveTo(smooth_index_x, smooth_index_y)

                # Thumb (id == 4)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Check if the thumb is close enough to the index finger for a click
                    if abs(smooth_index_x - thumb_x) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)

                # Middle finger lower joint (id == 10)
                if id == 10:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))  # Mark middle finger joint
                    mid_x = screen_width / frame_width * x
                    mid_y = screen_height / frame_height * y

                # Middle finger (id == 12) for scrolling
                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))  # Mark middle finger tip
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y
                    # Scroll down continuously when middle finger is brought down
                    if middle_y > mid_y:
                        scroll_active = True  # Start scrolling down
                    else:
                        scroll_active = False  # Stop scrolling when finger is raised

                if id == 14:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))  # Mark middle finger joint
                    mid_x = screen_width / frame_width * x
                    mid_y = screen_height / frame_height * y

                if id == 16:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))  # Mark middle finger tip
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y
                    # Scroll down continuously when middle finger is brought down
                    if middle_y > mid_y:
                        scrollup_active = True  # Start scrolling down
                    else:
                        scrollup_active = False  # Stop scrolling when finger is raised

    # Continuous scrolling if active
    if scroll_active:
        pyautogui.scroll(-80)   # Scroll down continuously at a fixed rate
    if scrollup_active:
        pyautogui.scroll(80)

    cv2.imshow('Virtual Mouse with Continuous Down Scroll', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing the ESC key
        break

cap.release()
cv2.destroyAllWindows()
