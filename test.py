import os
import sys

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from wham_api import WHAM_API
def test_wham_analysis():
    # Initialize WHAM API
    wham_model = WHAM_API()
    
    # Set input video path
    input_video_path = '../examples/1.mp4'
    
    # Process video
    try:
        import ipdb; ipdb.set_trace()
        results, tracking_results, slam_results = wham_model(input_video_path)
        
        # Print results summary
        print("Main Results:", type(results))
        if results:
            print("Results keys:", results.keys())
            
        print("\nTracking Results:", type(tracking_results))
        if tracking_results:
            print("Tracking shape/size:", len(tracking_results))
            
        print("\nSLAM Results:", type(slam_results))
        if slam_results:
            print("SLAM shape/size:", len(slam_results))
            
    except Exception as e:
        print(f"Error processing video: {str(e)}")

if __name__ == "__main__":
    test_wham_analysis()