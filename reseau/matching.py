import cv2
import numpy as np
from picamera2 import Picamera2
import time
import sys

class Matching:
    def __init__(self):
        self.resultat = False
        self.color1_bgr = (29, 94, 100)
        self.color2_bgr = (29, 94, 100)
        self.hsv1 = self.convert_bgr_to_hsv(self.color1_bgr)
        self.hsv2 = self.convert_bgr_to_hsv(self.color2_bgr)

        self.reference_image = cv2.imread("./pato.png")
        if self.reference_image is None:
            print("Error: Could not load reference image.")
            sys.exit(1)

        self.reference_masked = self.detect_colors(self.reference_image, self.hsv1, self.hsv2)
        cv2.imwrite("reference_masked_binary.png", self.reference_masked)

        self.contours_reference, _ = cv2.findContours(self.reference_masked, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(self.contours_reference) == 0:
            print("Error: No contours found in reference image.")
            sys.exit(1)

        self.reference_contour = max(self.contours_reference, key=cv2.contourArea)
        self.reference_image_copy = self.reference_image.copy()
        cv2.drawContours(self.reference_image_copy, [self.reference_contour], -1, (0, 255, 0), 3)

        # ---------- CONFIGURATION CAMERA ----------
        self.picam2 = Picamera2()
        self.config = self.picam2.create_still_configuration(main={"format": "RGB888", "size": (640, 480)})
        self.picam2.configure(self.config)

        self.picam2.set_controls({
            "AwbMode": 1,
            "AeEnable": True
        })

        self.picam2.start()
        time.sleep(2)  # Laisse le temps à l’AWB et AE de se stabiliser
        

    def convert_bgr_to_hsv(self, bgr_color):
        color_bgr = np.uint8([[bgr_color]])
        color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)
        return color_hsv[0][0]

    def detect_colors(self, frame, hsv1, hsv2):  # hsv20 corrigé en hsv2
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        margin = 8
        hsv_ranges = [
            ([max(hsv1[0] - margin, 0), 50, 50], [min(hsv1[0] + margin, 179), 255, 255]),
            ([max(hsv2[0] - margin, 0), 50, 50], [min(hsv2[0] + margin, 179), 255, 255])
        ]
        mask = np.zeros_like(hsv[:, :, 0])
        for lower, upper in hsv_ranges:
            lower_bound = np.array(lower, dtype=np.uint8)
            upper_bound = np.array(upper, dtype=np.uint8)
            mask_part = cv2.inRange(hsv, lower_bound, upper_bound)
            mask = cv2.bitwise_or(mask, mask_part)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask

    def get_contour_center(self, contour):
        moments = cv2.moments(contour)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            return (cx, cy)
        return None

    def compare_contours(self, captured_contour, threshold=0.1):
        shape_match_score = cv2.matchShapes(captured_contour, self.reference_contour, 1, 0.0)
        print(f"Shape Match Score: {shape_match_score}")
        return shape_match_score < threshold

    def is_contour_centered(self, contour, frame_shape, margin=100):
        if not isinstance(contour, np.ndarray):
            raise ValueError("Le contour fourni n'est pas un tableau numpy valide.")

        if contour.ndim != 3 or contour.shape[1:] != (1, 2):
            raise ValueError(f"Format de contour invalide: shape {contour.shape}")

        x, y, w, h = cv2.boundingRect(contour)
        center_box = (x + w // 2, y + h // 2)

        height, width = frame_shape[:2]
        center_image = (width // 2, height // 2)

        dx = abs(center_box[0] - center_image[0])
        dy = abs(center_box[1] - center_image[1])

        return dx <= margin and dy <= margin

    def matching_check(self):
        self.resultat = False
        self.frame_rgb = self.picam2.capture_array()
        # self.frame_rgb = cv2.cvtColor(self.frame_rgb, cv2.COLOR_RGB2BGR)  # Corrigé
        # cv2.imshow("Original Image", self.frame_rgb)
        # -----------------------------------------------------
        print("Processing captured image...")
        combined_mask = self.detect_colors(self.frame_rgb, self.hsv1, self.hsv2)  # Corrigé
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            center = self.get_contour_center(largest_contour)
            if center:
                print(f"Largest Contour Center: {center}")
            frame_with_contour = self.frame_rgb.copy()
            cv2.drawContours(frame_with_contour, [largest_contour], -1, (0, 255, 0), 3)
            # height = min(frame_with_contour.shape[0], self.reference_image_copy.shape[0])
            # frame_resized = cv2.resize(frame_with_contour, (int(frame_with_contour.shape[1] * height / frame_with_contour.shape[0]), height))
            # reference_resized = cv2.resize(self.reference_image_copy, (int(self.reference_image_copy.shape[1] * height / self.reference_image_copy.shape[0]), height))
            # comparison_image = np.hstack((frame_resized, reference_resized))
            # cv2.imshow("Captured vs Reference", comparison_image)
            match_result = self.compare_contours(largest_contour, threshold=0.5)  # Corrigé (1 seul argument de forme)
            if match_result:
                print("Contours Match: ✅ YES")
                if self.is_contour_centered(largest_contour, self.frame_rgb.shape):
                    print("Contour centered ✅")
                    self.resultat = True
                else:
                    print("Contour NOT centered ❌")
                    self.resultat = False
            else:
                print("Contours Do Not Match: ❌ NO")
                self.resultat = False
        else:
            print("No contours detected in captured image.")

if __name__ == "__main__":
    cam = Matching()
    print("Press 'C' to capture and compare.")
    print("Press 'Q' to quit.")
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            cam.matching_check()
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    cam.picam2.stop()
