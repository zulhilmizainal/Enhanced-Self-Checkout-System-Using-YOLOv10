# ui/virtual_keyboard.py
import cv2
import mediapipe as mp
import time
from datetime import datetime
from utils.sales_db import insert_sale
from utils.cart import get_cart, clear_cart
from ui.receipt import open_receipt_window
import winsound

# Layout
key_layout = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Clear", "Enter", "Delete"]
]

key_positions = {}
DEBOUNCE_DELAY = 1.5
last_pressed = {}
final_text = ""
total_price = 0
keyboard_parent = None
keyboard_root = None

def draw_keys(frame, hovered_key=None):
    h, w, _ = frame.shape
    key_height = 80
    spacing = 8
    key_positions.clear()

    # Row 1 — Numbers
    number_keys = key_layout[0]
    key_width = int((w - 120 - spacing * (len(number_keys) - 1)) / 10)
    start_x = 40
    start_y = 100

    for j, key in enumerate(number_keys):
        x1 = start_x + j * (key_width + spacing)
        y1 = start_y
        x2 = x1 + key_width
        y2 = y1 + key_height
        key_positions[key] = (x1, y1, x2, y2)

        bg = (180, 255, 180) if hovered_key == key else (255, 255, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), bg, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), 2)
        text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = x1 + (key_width - text_size[0]) // 2
        text_y = y1 + (key_height + text_size[1]) // 2
        cv2.putText(frame, key, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Row 2 — Clear, Enter, Delete
    btn_width = 130
    y1 = int(h * 0.50)
    y2 = y1 + key_height

    # Clear (left)
    key = "Clear"
    x1 = 40
    x2 = x1 + btn_width
    key_positions[key] = (x1, y1, x2, y2)
    bg = (180, 255, 180) if hovered_key == key else (255, 255, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), bg, -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), 2)
    cv2.putText(frame, key, (x1 + 20, y1 + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Enter (centered)
    key = "Enter"
    x1 = (w - btn_width) // 2
    x2 = x1 + btn_width
    key_positions[key] = (x1, y1, x2, y2)
    bg = (180, 255, 180) if hovered_key == key else (255, 255, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), bg, -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), 2)
    cv2.putText(frame, key, (x1 + 20, y1 + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Delete (right)
    key = "Delete"
    x1 = w - btn_width - 40
    x2 = x1 + btn_width
    key_positions[key] = (x1, y1, x2, y2)
    bg = (180, 255, 180) if hovered_key == key else (255, 255, 255)
    cv2.rectangle(frame, (x1, y1), (x2, y2), bg, -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), 2)
    cv2.putText(frame, key, (x1 + 10, y1 + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

def handle_key_press(key):
    global final_text
    print("Key Pressed:", key)
    winsound.Beep(600, 100)  # Click sound

    if key == "Delete":
        final_text = final_text[:-1]
    elif key == "Clear":
        final_text = ""
    elif key == "Enter":
        if final_text:
            handle_payment(final_text)
        else:
            final_text = "Please enter card number"
    else:
        final_text += key

def handle_payment(card_number):
    global total_price, final_text

    today = datetime.now().strftime("%Y-%m-%d")
    for item in get_cart():
        insert_sale(today, item["name"], item["qty"], item["price"], item["amount"])

    print("Paid in Full with card", card_number)

    if keyboard_parent:
        keyboard_parent.destroy()
    open_receipt_window(card_number, root=keyboard_root)

    clear_cart()
    final_text = ""

def open_virtual_keyboard(total, parent=None, root=None):
    global total_price, final_text, keyboard_parent, keyboard_root
    total_price = total
    final_text = ""
    keyboard_parent = parent
    keyboard_root = root

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7)
    cap = cv2.VideoCapture(1) # Use the webcam camera

    # Set camera resolution to 1280x720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Virtual Keyboard", cv2.WND_PROP_AUTOSIZE, 1)
    cv2.resizeWindow("Virtual Keyboard", 1280, 720)

    hovered_key = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        hovered_key = None

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                index_tip = hand.landmark[8]
                cx, cy = int(index_tip.x * w), int(index_tip.y * h)
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                for key, (x1, y1, x2, y2) in key_positions.items():
                    if x1 < cx < x2 and y1 < cy < y2:
                        hovered_key = key
                        now = time.time()
                        if key not in last_pressed or now - last_pressed[key] > DEBOUNCE_DELAY:
                            last_pressed[key] = now
                            handle_key_press(key)

                            if key == "Enter":
                                cap.release()
                                cv2.destroyAllWindows()
                                hands.close()
                                return
                        break

        draw_keys(frame, hovered_key)

        # Instruction label shown in red at the top of the screen
        cv2.putText(
            frame,
            "Enter Credit/Debit Card Number",
            (50, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            2,
        )

        # Display the numbers entered so far
        cv2.putText(
            frame,
            final_text,
            (50, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.4,
            (0, 0, 255),
            3,
        )

        cv2.imshow("Virtual Keyboard", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()
