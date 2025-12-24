# AI Service Availability Test Script

This document provides the Python script and instructions for manually testing the availability and functionality of all seven AI service APIs in your application's backend.

The script simulates a client request to each API endpoint, verifying that the backend is running, the endpoint is accessible, and the underlying AI model is responding correctly.

## Prerequisites

1.  **Python 3.x** must be installed.
2.  The `requests` library must be installed:
    ```bash
    pip install requests
    ```
3.  Your **backend service** must be running and accessible at `http://localhost:8000`.

## Files Provided

The following files have been created in the root of your cloned repository (`/home/ubuntu/mix`):

| File Name | Description |
| :--- | :--- |
| `test_api_availability.py` | The main Python script to run all API tests. |
| `test_image.png` | A dummy image file for Image-to-Video and Image Editing tests. |
| `test_mask.png` | A dummy mask file for Image Editing (Inpainting) tests. |
| `test_audio.wav` | A dummy audio file for Speech-to-Text tests. |

## Usage Instructions

### Step 1: Ensure Backend is Running

Before running the script, start your backend service (assuming you are in the `/home/ubuntu/mix/backend` directory):

```bash
# Navigate to the backend directory
cd /path/to/mix/backend

# Activate your virtual environment (if applicable)
source venv/bin/activate

# Start the server (e.g., using uvicorn)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 2: Run the Test Script

Open a **new terminal window** (or ensure the server is running in the background) and run the test script from the root of the `mix` repository:

```bash
# Navigate to the repository root
cd /path/to/mix

# Run the test script
python3 test_api_availability.py
```

### Step 3: Analyze the Results

The script will print a status for each of the seven services:

| Service | Endpoint | Test Description |
| :--- | :--- | :--- |
| **LLM** | `/api/llm` | Sends a simple question and checks for a text response. |
| **TTS** | `/api/tts` | Sends text and checks for a binary audio response. |
| **STT** | `/api/stt` | Sends the dummy audio file and checks for a text transcription. |
| **Image Gen** | `/api/image/generate` | Sends a text prompt and checks for a binary image response. |
| **Image Edit** | `/api/image/edit` | Sends the dummy image, mask, and a prompt, checking for a binary image response. |
| **T2V** | `/api/video/t2v` | Sends a text prompt and checks for a binary video response. |
| **I2V** | `/api/video/i2v` | Sends the dummy image and a prompt, checking for a binary video response. |

**Expected Output:**

A successful run will look like this:

```
--- Starting AI Service Availability Test ---
Target URL: http://localhost:8000
Working Directory: /home/ubuntu/mix

--- Testing LLM Service ---
[✅ SUCCESS] LLM (/api/llm): Status 200. Response received in 5.12s.

--- Testing TTS Service ---
[✅ SUCCESS] TTS (/api/tts): Status 200. Binary data received (123456 bytes) in 3.45s.

... (All services should show SUCCESS) ...

--- Final Summary ---
Total Tests: 7
Passed: 7
Failed: 0

All services passed the availability test.
```

**Troubleshooting Failures (❌ FAILURE):**

If a test fails, check the following:

1.  **Connection Error:** If the script reports a `Connection Error`, ensure your backend server is running and accessible at `http://localhost:8000`.
2.  **HTTP Error 404:** The endpoint URL is incorrect or the backend is not configured properly.
3.  **HTTP Error 500:** The backend is running, but the underlying AI model failed to generate a response (e.g., model not found, API key issue, or model is down). This is the most common failure when an AI model is unavailable.
4.  **Timeout Error:** The model is taking too long to load or respond. You may need to increase the `TIMEOUT` variable in the script.

This script provides a quick and reliable way to verify the health of your AI services after any model or configuration changes.
