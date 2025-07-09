# this script is just to help identify all the camera ports available
# to not make mistake when setting the camera index that should be used
import cv2
from pygrabber.dshow_graph import FilterGraph

def get_camera_names():
    graph = FilterGraph()
    return graph.get_input_devices()

def identify_camera(index, name_guess):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"❌ Camera index {index} ({name_guess}) failed to open")
        return

    ret, frame = cap.read()
    if not ret:
        print(f"❌ Camera index {index} ({name_guess}) failed to capture frame")
        cap.release()
        return

    height, width = frame.shape[:2]
    cap.release()

    print(f"✅ Camera index {index} ({name_guess}) works — Resolution: {width}x{height}")

def main():
    camera_names = get_camera_names()

    print("📝 Detected Cameras (in order):")
    for i, name in enumerate(camera_names):
        print(f"  Index {i}: {name}")

    print("\n🎥 Testing each camera index with OpenCV...")
    for i, name in enumerate(camera_names):
        identify_camera(i, name)

if __name__ == "__main__":
    main()
