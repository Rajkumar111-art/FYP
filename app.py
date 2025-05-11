from flask import Flask, render_template, request, send_from_directory
import os
from main import main as analyze_video

app = Flask(__name__)

# Define folders for uploads and output
UPLOAD_FOLDER = "input_videos"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Set the upload folder for the Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        if video:
            output_filename='final_output.mp4'
            input_path = os.path.join(UPLOAD_FOLDER, video.filename)
            output_path = os.path.join(OUTPUT_FOLDER, 'final_output.mp4')  # Adjust output filename as necessary
            video.save(input_path)
            
            # Call your analysis function
            analyze_video(input_path, output_path)
            
            # Render the result page with the output path
            return render_template('index.html',output_filename=output_filename)
    return render_template('index.html', output_path=None)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
