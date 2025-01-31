import cv2
import numpy as np
import time
from threading import Thread
from queue import Queue
import datetime

class WebcamProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Could not open webcam")
        
        # Get webcam properties
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        # Initialize queues for frame processing
        self.raw_frames = Queue(maxsize=self.fps)
        self.processed_frames = Queue(maxsize=self.fps)
        
        # Initialize processing thread
        self.is_running = True
        self.processing_thread = Thread(target=self._process_frames)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def _process_frames(self):
        """Process frames in a separate thread."""
        while self.is_running:
            if not self.raw_frames.empty():
                frames = []
                # Collect 1 second worth of frames
                while len(frames) < self.fps and not self.raw_frames.empty():
                    frames.append(self.raw_frames.get())
                
                if frames:
                    # Process the frames
                    processed_frames = self._apply_processing(frames)
                    
                    # Store processed frames
                    for frame in processed_frames:
                        self.processed_frames.put(frame)

    def _apply_processing(self, frames):
        """
        Apply video processing to the frames.
        This is where you would normally call the WHAM API.
        Currently using a placeholder effect.
        """
        processed = []
        for frame in frames:
            # Placeholder processing - convert to grayscale and apply threshold
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, processed_frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
            processed.append(processed_frame)
            
            # WHAM API processing would go here:
            # from wham_api import WHAM_API
            # wham_model = WHAM_API()
            # results, tracking_results, slam_results = wham_model(frame)
            # processed_frame = ... # process results to create visual output
            
        return processed

    def run(self):
        """Main loop to capture and display frames."""
        start_time = time.time()
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Store raw frame
            if not self.raw_frames.full():
                self.raw_frames.put(frame)
            
            # Get processed frame if available
            processed_frame = None
            if not self.processed_frames.empty():
                processed_frame = self.processed_frames.get()
            
            # Display frames side by side
            if processed_frame is not None:
                # Ensure both frames have the same height
                h1, w1 = frame.shape[:2]
                h2, w2 = processed_frame.shape[:2]
                
                # Create side-by-side display
                display = np.zeros((max(h1, h2), w1 + w2, 3), dtype=np.uint8)
                display[:h1, :w1] = frame
                display[:h2, w1:w1+w2] = processed_frame
                
                # Add timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(display, timestamp, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                # Show the combined frame
                cv2.imshow('Webcam Feed (Original | Processed)', display)
            
            # Check for 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Update FPS counter
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"FPS: {fps:.2f}")

    def cleanup(self):
        """Clean up resources."""
        self.is_running = False
        if self.processing_thread.is_alive():
            self.processing_thread.join()
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        processor = WebcamProcessor()
        processor.run()
    finally:
        processor.cleanup()