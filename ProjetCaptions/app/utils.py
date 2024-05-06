from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer, pipeline
from PIL import Image

# Charger le modèle de description d'image
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Charger le modèle de traduction
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

def generate_description(image):
    image = Image.open(image)
    feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")
    inputs = feature_extractor(images=image, return_tensors="pt")
    pixel_values = inputs["pixel_values"]

    # Générer une description en anglais
    output_ids = model.generate(pixel_values)
    description = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Traduire la description en français
    translated_description = translator(description)[0]['translation_text']

    return translated_description
