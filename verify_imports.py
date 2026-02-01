try:
    from google import genai
    print("SUCCESS: google-genai imported")
except ImportError as e:
    print(f"FAILURE: {e}")

try:
    from backend import TranslationBackend
    print("SUCCESS: backend imported")
except ImportError as e:
    print(f"FAILURE: {e}")
