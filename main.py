from detection_part import detection_part
from projection_part import projection_part
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
    print("Step 1: Processing video with detection part...")
    detection_part(input_path, OUTLINED_VIDEO)

    # Step 2: Generate 2D projection and combine with original
    print("Step 2: Generating 2D projection with projection part...")
    projection_part(OUTLINED_VIDEO, FINAL_VIDEO)

    print("✅ Processing complete.")
    print(f"Final output video: {FINAL_VIDEO}")

if __name__ == "__main__":
    main(INPUT_VIDEO, FINAL_VIDEO)
