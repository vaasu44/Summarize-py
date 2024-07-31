from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import JSONResponse
import tensorflow as tf 
import numpy as np 
import os 
from pydantic import BaseModel
from transformers import BartTokenizer, BartForConditionalGeneration
from PyPDF2 import PdfReader
import docx

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

app = FastAPI()

class input_model(BaseModel) : 
    data : str

origins =  ['http://localhost:3000', "*"]
app.add_middleware(
    CORSMiddleware , 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

UPLOAD_DIR = "uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text



@app.post('/predict/') 
def predict(data :dict) : 
    input = dict(data)
    article = input['text']
    inputs = tokenizer([article], max_length=1024, return_tensors="pt")
    summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=10000)
    return tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".pdf", ".doc", ".docx", ".txt"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Extract text from the file based on its type
    if file_extension == ".pdf":
        file_contents = read_pdf(file_path)
    elif file_extension in [".doc", ".docx"]:
        file_contents = read_docx(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            file_contents = file_handle.read()

    return JSONResponse(content={"filename": file.filename, "filepath": file_path, "contents": file_contents}, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)