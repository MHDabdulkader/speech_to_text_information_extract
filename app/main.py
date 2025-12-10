from app.settings import settings
from fastapi import FastAPI, UploadFile, File, Query
import requests
import uuid
import os, json

app = FastAPI()
ASSEMBLYAI_APITOKEN = settings.ASSEMBLYAI_APITOKEN
assemblyai_baseurl = "https://api.assemblyai.com"
text_save_dir = "transcript"

os.makedirs(text_save_dir, exist_ok=True)


@app.post("/voice-to-text")
async def voice_to_text(file: UploadFile=File(...)):
    audio_filename = f"temp_{uuid.uuid4()}.wav"
    
    with open(audio_filename, "wb") as buffer:
        buffer.write(await file.read())
        
    upload_ai_url =  f"{assemblyai_baseurl}/v2/upload"
    headers = {"Authorization": ASSEMBLYAI_APITOKEN}
    
    
    with open(audio_filename, "rb") as audio_file:
        upload_ai_response = requests.post(upload_ai_url, headers=headers, data=audio_file)
    print(f"======== upload response from ai upload_ai_response ======== ", upload_ai_response)
    
    
    if upload_ai_response.status_code != 200:
        os.remove(audio_filename)
        return {"error": "Failed to uploaded to assembleAI"}
    
    
    audio_url = upload_ai_response.json()["upload_url"]
    
    transcript_url = assemblyai_baseurl + "/v2/transcript"
    json_data = {"audio_url": audio_url}
    
    transcript_response = requests.post(
        transcript_url,
        json=json_data,
        headers=headers
    )
    print(f"======== upload response from ai transcript_response ======== ", transcript_response)
    transcript_id = transcript_response.json()["id"]
    
    polling_url = f"{transcript_url}/{transcript_id}"
    
    import time 
    while True:
        status_response = requests.get(polling_url, headers=headers)
        status = status_response.json()["status"]
        print(f"================ status response polling url, status =============", status_response, " ====== ", status)
        if status == "completed":
            text = status_response.json()["text"]
            
            os.remove(audio_filename)
            
            txt_filename = f"{uuid.uuid4()}.txt"
            txt_path = os.path.join(text_save_dir, txt_filename)
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            return {
                "text": text,
                "saved_file": txt_path
            }
        elif status == "error":
            os.remove(audio_filename)
            return {
                "error": status_response.json()["error"]
            }
            
        time.sleep(1)
        

from google import genai

client = genai.Client(api_key=settings.GEMINI_APITOKEN)


# ? later as function inside the voice recognation api
@app.get("/extract-information")
async def extract_information_text(text: str = Query(..., description="Text from which to extract foods, reasons and symptoms")):
    
    prompt = f"""
    Extract the foods and reasons for symptoms from this text:
    "{text}"
    
    Return ONLY JSON with keys:
    {{
        "foods": [],
        "reasons": [],
        "symptoms": []
    }}
    """
    
    # model = client.GenerativeModel("models/gemini-1.5-flash")
    # response = model.generate_content(prompt)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    try: 
        extract_json = json.loads(response.text)
    except json.JSONDecodeError:
        cleaned = response.text.strip("```json").strip("```").strip()
        extract_json = json.loads(cleaned)
    
    
    txt = f"extract{uuid.uuid4()}.json"
    txt_path = os.path.join(text_save_dir, txt)
    
    with open(txt_path, "w", encoding="utf-8") as f:
        json.dump(extract_json, f, indent=2)
    return {
        "text": text,
        "extracted": extract_json,
        
    }
    
@app.get("/symptom-linker")
async def symptom_linker(text: str = Query(..., description="Text containing foods eaten with time and symptom with time")):
    prompt = f"""
    Analyze the following text and link each symptom to the food(s) that likely caused it.
    Return ONLY JSON with keys : "foods", "symptoms", "linked" (list of objects with food, symptom, time).
    
    Text:
    "{text}"
    
    Example output format:
    {{
        "foods" : ["chicken", "rice", "salad"],
        "symptoms": ["bloating"],
        "linked": [
            {{
                "food": "rice",
                "symptom": "bloating",
                "food_time": "12.45 PM",
                "symptom_time" : "3.00 PM"
            }}
        ] 
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    try: 
        extract_json = json.loads(response.text)
    except json.JSONDecodeError:
        cleaned = response.text.strip("```json").strip("```").strip()
        extract_json = json.loads(cleaned)
    
    
    txt = f"linked{uuid.uuid4()}.json"
    txt_path = os.path.join(text_save_dir, txt)
    
    with open(txt_path, "w", encoding="utf-8") as f:
        json.dump(extract_json, f, indent=2)
    return {
        "text": text,
        "linked": extract_json,
        
    }