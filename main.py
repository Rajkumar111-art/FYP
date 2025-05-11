from main1 import main1
from main2 import main2
import os

# Define input and output paths
INPUT_VIDEO = "input_videos/input_video-0.mp4"
OUTLINED_VIDEO = "output/detection_output.mp4"
FINAL_VIDEO = "output/final_output.mp4"

def ensure_directories():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

def main(input_path, output_path):
    print("🎾 Starting Tennis Analysis Pipeline")

    ensure_directories()

    # Step 1: Outline players, ball, and court
    # print("Step 1: Processing video with main1.py...")
    # main1(input_path, OUTLINED_VIDEO)

    # Step 2: Generate 2D projection and combine with original
    print("Step 2: Generating 2D projection with main2.py...")
    main2(OUTLINED_VIDEO, FINAL_VIDEO)

    print("✅ Processing complete.")
    print(f"Final output video: {FINAL_VIDEO}")

if __name__ == "__main__":
    main()
