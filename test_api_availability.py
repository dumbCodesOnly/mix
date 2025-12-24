import requests
import json
import os
import time
from typing import Optional

# --- Configuration ---
# Updated to use the Render deployment URL
BASE_URL = "https://mix-7elg.onrender.com"
TIMEOUT = 120  # Increased timeout for potentially slow AI model loading/inference

# Public URLs for test files (uploaded from sandbox)
TEST_FILE_URLS = {
    "image": "https://files.manuscdn.com/user_upload_by_module/session_file/310519663261659853/ONodHDbdqiHpDdWk.png",
    "mask": "https://files.manuscdn.com/user_upload_by_module/session_file/310519663261659853/XDbTacuMSJLbwVGX.png",
    "audio": "https://files.manuscdn.com/user_upload_by_module/session_file/310519663261659853/dUWfammpgShReWPx.wav"
}

# --- Helper Functions ---

def print_status(service: str, endpoint: str, success: bool, message: str):
    """Prints a formatted status message."""
    status = "✅ SUCCESS" if success else "❌ FAILURE"
    print(f"[{status}] {service} ({endpoint}): {message}")

def test_endpoint(
    service: str,
    endpoint: str,
    method: str = "POST",
    data: Optional[dict] = None,
    files: Optional[dict] = None,
    json_data: Optional[dict] = None
) -> bool:
    """Generic function to test an API endpoint."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        start_time = time.time()
        
        if method == "POST":
            response = requests.post(url, data=data, files=files, json=json_data, timeout=TIMEOUT)
        elif method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        else:
            print_status(service, endpoint, False, f"Unsupported method: {method}")
            return False

        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            # Check for valid JSON response (most endpoints return JSON)
            try:
                response_json = response.json()
                if "error" in response_json or "detail" in response_json:
                    print_status(service, endpoint, False, f"API returned error in response body: {response_json.get('error') or response_json.get('detail')}")
                    return False
                
                # Check for expected data in response (e.g., generated text, image URL)
                if service == "LLM" and "generated_text" not in response_json:
                    print_status(service, endpoint, False, "Missing 'generated_text' in response.")
                    return False
                
                print_status(service, endpoint, True, f"Status 200. Response received in {duration:.2f}s.")
                return True
            except json.JSONDecodeError:
                # Some endpoints (like TTS/Video) might return raw binary data
                if len(response.content) > 100:
                    print_status(service, endpoint, True, f"Status 200. Binary data received ({len(response.content)} bytes) in {duration:.2f}s.")
                    return True
                else:
                    print_status(service, endpoint, False, f"Status 200, but response is not valid JSON or binary data: {response.text[:50]}...")
                    return False
        else:
            try:
                error_detail = response.json().get("detail", response.text)
            except:
                error_detail = response.text
            print_status(service, endpoint, False, f"HTTP Error {response.status_code}. Detail: {error_detail}")
            return False

    except requests.exceptions.Timeout:
        print_status(service, endpoint, False, f"Request timed out after {TIMEOUT}s.")
        return False
    except requests.exceptions.ConnectionError:
        print_status(service, endpoint, False, f"Connection Error. Is the backend running at {BASE_URL}?")
        return False
    except Exception as e:
        print_status(service, endpoint, False, f"An unexpected error occurred: {e}")
        return False

# --- Test Functions for Each Service ---

def test_llm():
    """Tests the Large Language Model API."""
    print("\n--- Testing LLM Service ---")
    return test_endpoint(
        service="LLM",
        endpoint="/api/llm",
        json_data={
            "messages": [{"role": "user", "content": "What is the capital of France?"}],
            "model": "meta-llama/Llama-3.1-8B-Instruct" # Explicitly set a working model
        }
    )

def test_tts():
    """Tests the Text-to-Speech API."""
    print("\n--- Testing TTS Service ---")
    return test_endpoint(
        service="TTS",
        endpoint="/api/tts",
        json_data={"text": "This is a test sentence for the text to speech service."}
    )

def test_stt():
    """Tests the Speech-to-Text API."""
    print("\n--- Testing STT Service ---")
    audio_url = TEST_FILE_URLS["audio"]
    
    # STT endpoint expects a file upload, so we need to download the file first
    try:
        audio_response = requests.get(audio_url, timeout=30)
        audio_response.raise_for_status()
        audio_file = audio_response.content
    except Exception as e:
        print_status("STT", "/api/stt", False, f"Failed to download test audio: {e}")
        return False
        
    # Create a file-like object for requests.post
    files = {"audio_file": ("test_audio.wav", audio_file, "audio/wav")}
    
    return test_endpoint(
        service="STT",
        endpoint="/api/stt",
        files=files
    )

def test_image_generate():
    """Tests the Image Generation API."""
    print("\n--- Testing Image Generation Service ---")
    return test_endpoint(
        service="Image Gen",
        endpoint="/api/image/generate",
        json_data={"prompt": "A simple test image of a red square"}
    )

def test_image_edit():
    """Tests the Image Editing (Inpainting) API."""
    print("\n--- Testing Image Editing Service ---")
    image_url = TEST_FILE_URLS["image"]
    mask_url = TEST_FILE_URLS["mask"]
    
    # Download image and mask
    try:
        image_response = requests.get(image_url, timeout=30)
        mask_response = requests.get(mask_url, timeout=30)
        image_response.raise_for_status()
        mask_response.raise_for_status()
        image_file = image_response.content
        mask_file = mask_response.content
    except Exception as e:
        print_status("Image Edit", "/api/image/edit", False, f"Failed to download test files: {e}")
        return False
        
    files = {
        "image_file": ("test_image.png", image_file, "image/png"),
        "mask_file": ("test_mask.png", mask_file, "image/png")
    }
    data = {"prompt": "Change the black square to a blue circle"}
    
    return test_endpoint(
        service="Image Edit",
        endpoint="/api/image/edit",
        data=data,
        files=files
    )

def test_video_t2v():
    """Tests the Text-to-Video API."""
    print("\n--- Testing Text-to-Video Service ---")
    return test_endpoint(
        service="T2V",
        endpoint="/api/video/t2v",
        json_data={"prompt": "A short video of a cat walking on the moon"}
    )

def test_video_i2v():
    """Tests the Image-to-Video API."""
    print("\n--- Testing Image-to-Video Service ---")
    image_url = TEST_FILE_URLS["image"]
    
    # Download image
    try:
        image_response = requests.get(image_url, timeout=30)
        image_response.raise_for_status()
        image_file = image_response.content
    except Exception as e:
        print_status("I2V", "/api/video/i2v", False, f"Failed to download test image: {e}")
        return False
        
    files = {"image_file": ("test_image.png", image_file, "image/png")}
    data = {"prompt": "Make the image slowly zoom in"}
    
    return test_endpoint(
        service="I2V",
        endpoint="/api/video/i2v",
        data=data,
        files=files
    )

def main():
    """Runs all API tests."""
    print(f"--- Starting AI Service Availability Test ---")
    print(f"Target URL: {BASE_URL}")
    
    results = {
        "LLM": test_llm(),
        "TTS": test_tts(),
        "STT": test_stt(),
        "Image Gen": test_image_generate(),
        "Image Edit": test_image_edit(),
        "T2V": test_video_t2v(),
        "I2V": test_video_i2v(),
    }
    
    print("\n--- Final Summary ---")
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if failed_tests > 0:
        print("\nATTENTION: Some services failed. Check the logs above for details.")
        return 1
    else:
        print("\nAll services passed the availability test.")
        return 0

if __name__ == "__main__":
    main()
