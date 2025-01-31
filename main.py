import cv2
import numpy as np
import time
from wham_api import WHAM_API
import tempfile
import os

class WebcamProcessor:
    def __init__(self, fps=30):
        self.fps = fps
        self.frames_per_clip = fps  # 1 second of frames
        self.cap = cv2.VideoCapture(0)
        self.wham = WHAM_API()
        
        # Set webcam properties
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def capture_clip(self):
        frames = []
        for _ in range(self.frames_per_clip):
            ret, frame = self.cap.read()
            if not ret:
                raise RuntimeError("Failed to capture frame")
            frames.append(frame)
        return frames

    def save_temp_clip(self, frames):
        temp_file = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
        out = cv2.VideoWriter(
            temp_file.name,
            cv2.VideoWriter_fourcc(*'XVID'),
            self.fps,
            (self.frame_width, self.frame_height)
        )
        for frame in frames:
            out.write(frame)
        out.release()
        return temp_file.name

    def process_clip(self, clip_path):
        
        return self.wham.process_video(clip_path)

    def display_side_by_side(self, original_frame, processed_frame):
        combined = np.hstack((original_frame, processed_frame))
        cv2.imshow('Original vs Processed', combined)
        return cv2.waitKey(1) & 0xFF

    def run(self):
        try:
            while True:
                # Capture 1-second clip
                frames = self.capture_clip()
                
                # Save to temporary file
                temp_path = self.save_temp_clip(frames)
                
                # Process with WHAM
                processed_frames = self.process_clip(temp_path)
                
                # Display each frame pair
                for orig, proc in zip(frames, processed_frames):
                    if self.display_side_by_side(orig, proc) == ord('q'):
                        return
                
                # Cleanup
                os.unlink(temp_path)
                
        finally:
            self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = WebcamProcessor()
    processor.run()