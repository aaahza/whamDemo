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
    input_video_path = 'examples/1.mp4'
    
    import ipdb; ipdb.set_trace()
    results, tracking_results, slam_results = wham_model(input_video_path)

    # Print types of the variables returned by WHAM model
    print("Type of results:", type(results))
    print("Type of tracking_results:", type(tracking_results))
    print("Type of slam_results:", type(slam_results))

if __name__ == "__main__":
    test_wham_analysis()