# 🎾 Tennis Analysis System

A comprehensive and modular tennis match analysis system built with Flask and Python, powered by the [`uv`](https://pypi.org/project/uv/) runtime. This system performs full video-based tennis analytics, including ball tracking, player movement, stroke recognition, and real-time visualizations.

## 🚀 Features

- Ball detection and tracking using deep learning
- Player detection, tracking, and pose estimation
- Court line detection and coordinate transformation
- Stroke recognition using Inception + LSTM
- Real-time visualization pipeline
- Flask-based backend for extensibility
- One-command setup using `uv`

## 📦 Setup Instructions

### 🛠️ Prerequisites
Before you begin, ensure the following are installed on your system:

#### 1. Python
Make sure Python 3.7+ is installed. You can verify with:

```bash
python --version
```

#### 2. pip
Ensure pip is installed:

```bash
pip --version
```

If it's not installed, follow these instructions.

#### 3. uv
Install the uv tool if it's not already installed:

```bash
pip install uv
```

📦 Project Setup
Once all prerequisites are installed, follow these steps:

#### 1. Clone the repository

```bash
git clone https://github.com/Adarsh-Agrahari/FYP

cd FYP
```
#### 2. Run the application
With uv, everything is automatic:

```bash
uv run app.py
```

This command will:

Automatically resolve and install all Python dependencies listed in requirements.txt or pyproject.toml

Launch the Flask application

## System Overview
A comprehensive tennis match analysis system that performs:
- Ball detection and tracking
- Player detection and tracking
- Court detection
- Stroke recognition
- Player movement analysis

## File-by-File Breakdown

### 1. `ball_detection.py`
**Purpose**: Detects and tracks the tennis ball in video frames  

**Key Components**:
- `BallDetector` class managing ball tracking
- Utilizes `BallTrackerNet` model
- Processes sequences of 3 frames (current + 2 previous)
- Implements distance-based outlier rejection
- Visualizes ball trajectory

**Models Used**: Custom BallTrackerNet CNN

**Necessity**:
- Fundamental for rally analysis
- Enables bounce detection and speed calculation
- Provides player-ball interaction data

### 2. `ball_tracker_net.py`
**Purpose**: Deep learning model for ball detection  

**Model Architecture**:
- Encoder-decoder CNN
- Input: 3 consecutive frames (9 channels - RGB×3)
- Output: Ball location heatmap (2 classes)
- Uses Hough Circle Transform for precise detection

**Necessity**:
- Robust ball detection capability
- Handles occlusion and fast movements
- Superior to traditional CV for small fast objects

### 3. `court_detection.py`
**Purpose**: Detects and tracks tennis court lines  

**Key Components**:
- Hough Transform line detection
- Court homography calculation
- Reference court configuration matching
- Important line identification

**Necessity**:
- Establishes court coordinate system
- Enables position normalization
- Provides tactical context

### 4. `court_reference.py`
**Purpose**: Stores court template and configurations  

**Key Components**:
- Predefined court line coordinates
- Multiple court configurations
- Court dimension constants
- Area mask generation

**Necessity**:
- Ground truth for court detection
- Accurate homography calculation
- Standardized court representation

### 5. `detection.py`
**Purpose**: Player detection and tracking  

**Key Components**:
- Faster R-CNN for player detection
- SORT algorithm for tracking
- Two-player distinction
- Court position calculation

**Models Used**: Faster R-CNN (torchvision)

**Necessity**:
- Player identification and tracking
- Enables player-specific analysis
- Supports stroke attribution

### 6. `pose.py`
**Purpose**: Player pose estimation  

**Key Components**:
- Keypoint R-CNN detection
- 17 body keypoints (COCO format)
- Skeletal connections tracking

**Models Used**: Keypoint R-CNN (torchvision)

**Necessity**:
- Enables stroke recognition
- Provides stance analysis
- Supports movement efficiency study

### 7. `smooth.py`
**Purpose**: Data smoothing and outlier handling  

**Key Components**:
- Savitzky-Golay filter
- Hampel outlier detection
- Data imputation
- Side-swapping correction

**Necessity**:
- Improves noisy detection data
- Makes trajectories physically plausible
- Handles temporary occlusions

### 8. `stroke_recognition.py`
**Purpose**: Classifies player strokes  

**Model Architecture**:
- Feature extraction: Inception v3
- Temporal modeling: LSTM
- Classes: forehand, backhand, service/smash

**Models Used**: Inception v3 + LSTM

**Necessity**:
- Automates stroke identification
- Enables stroke-specific stats
- Supports technique assessment

### 9. `main.py`
**Purpose**: Main processing pipeline  

**Key Components**:
- Coordinates all components
- Manages frame processing
- Generates visualizations
- Calculates statistics

**Necessity**:
- System integration core
- Maintains temporal consistency
- Produces final outputs

## System Workflow

    A[Video Input] --> B[Court Detection]
    A --> C[Player Detection]
    A --> D[Ball Detection]
    B --> E[Court Coordinates]
    C --> F[Player Tracking]
    D --> G[Ball Tracking]
    E --> H[Position Analysis]
    F --> H
    G --> H
    H --> I[Stroke Detection]
    H --> J[Bounce Detection]
    I --> K[Stroke Classification]
    J --> L[Trajectory Analysis]
    K --> M[Statistics]
    L --> M
    M --> N[Visualization]
    N --> O[Output]

# Ball Miss Prediction Logic

## Core Components

### Trajectory Prediction
- Uses simplified physics model with:
  - Constant downward gravity (0.5 pixels/frame²)
  - Air resistance factor (0.98 damping per frame)
- Predicts ball positions for next 15 frames (~0.5s at 30fps)
- Linear projection after accounting for deceleration

### Player Reach Analysis
Calculates maximum reach distance by:
1. Measuring arm length from shoulder→elbow→wrist keypoints
2. Adding 50% buffer for racket length
3. Defaults to 150px if pose detection fails
4. Creates a dynamic "reach zone" around player

### Impact Zone Detection
- Identifies when ball enters reachable area:
  - 20% safety buffer beyond calculated reach
  - First crossing point determines time-to-impact
- Aborts prediction if ball never enters reach zone

### Movement Capability Check
Compares:
- **Required speed**: Distance-to-ball / time-to-impact  
- **Player limits**:
  - Max speed: 800 pixels/second (empirical)
  - Minimum reaction time: 0.15 seconds
- Predicts miss if either threshold is exceeded

## Visualization
- **Warning**: Red "MISS PREDICTED!" text
- **Guidance**:
  - Green circle at ideal contact point  
  - Line connecting player to ideal position

## Key Assumptions

| Physical Factor       | Implementation          | Real-World Variance          |
|-----------------------|-------------------------|------------------------------|
| Ball spin             | Not modeled             | Affects trajectory curvature |
| Court surface         | Uniform friction        | Different materials affect bounce |
| Player stance         | Static reach            | Stretching/jumping not considered |
| Shot preparation      | Constant reaction time  | Anticipation reduces delay   |

## Accuracy Considerations
- **Best for**: Moderate-paced baseline rallies
- **Challenges**:
  - Fast serves (>180 km/h)
  - Sharp-angled volleys
  - Unpredictable bounces

## Potential Enhancements
1. **Dynamic Environment Factors**
   - Court-position aware friction
   - Net cord detection
   - Surface material adjustments

2. **Player Adaptations**
   - Individual speed profiles
   - Fatigue modeling
   - Playing style adjustments

3. **Advanced Physics**
   - Ball spin calculations
   - Elastic collision modeling
   - Aerodynamic drag coefficients