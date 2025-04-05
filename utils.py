import torch
import spacy
from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

nlp = spacy.load("en_core_web_sm")

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

EBAY_APP_ID = "pushkara-intelunn-SBX-4b0115f02-e8bf393d"
EBAY_ENDPOINT = "https://svcs.sandbox.ebay.com/services/search/FindingService/v1"

def generate_description(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt").to(device)
    caption = caption_model.generate(**inputs)
    return processor.decode(caption[0], skip_special_tokens=True)

def extract_product_name(description):
    doc = nlp(description)
    for ent in doc.ents:
        if ent.label_ in ["PRODUCT", "ORG", "WORK_OF_ART", "GPE"]:
            return ent.text
    stopwords = {"background", "close up", "photo", "image", "picture", "scene", "view"}
    words = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in stopwords]
    return " ".join(words[:2]) if words else description

def search_ebay(query, max_results=10):
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "keywords": query,
        "paginationInput.entriesPerPage": max_results,
    }
    response = requests.get(EBAY_ENDPOINT, params=params)
    data = response.json()
    items = data.get("findItemsByKeywordsResponse", [{}])[0].get("searchResult", [{}])[0].get("item", [])
    results = []
    for item in items:
        product_info = {
            "title": item.get("title", "No Title"),
            "price": item.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("__value__", "N/A"),
            "currency": item.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("@currencyId", "N/A"),
            "link": item.get("viewItemURL", "No URL")
        }
        results.append(product_info)
    return results
