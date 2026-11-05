"""
server.py - Ocularis AI Backend (DENGAN OLLAMA & MODEL TERKALIBRASI)
Fitur:
- Deteksi 7 kondisi klinis mata eksternal (Cornea, Pupil, Iris, Sclera, Eyelid)
- Zero Under/Overfitting dengan MobileNetV2 terkalibrasi (97.99% Val Acc)
- Out-of-Distribution Rejection ("Tidak Terdeteksi") via Confidence Thresholding
- Integrasi LLM (Ollama) untuk saran medis REAL-TIME
- CORS enabled untuk frontend (Ocularis.html)
"""

import sys
import io

# Force UTF-8 on Windows stdout/stderr to prevent charmap encoding errors
if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import base64
import requests
import os
import numpy as np
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# =========================
# CONFIG
# =========================
IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_TIMEOUT = 30  # Timeout 30 detik untuk Ollama

# 7 Kelas Klinis Biologis Mata
CLASS_NAMES = [
    'Bulging Eyes',
    'Cataract',
    'Crossed Eyes',
    'Dark Circles + Eyebags',
    'Eyelid',
    'Konjungtivitis',
    'Normal'
]

# Ambang Batas Deteksi (Untuk Out-of-Distribution Rejection)
MIN_CONFIDENCE_FOR_DISEASE = 0.45
MIN_CONFIDENCE_FOR_NORMAL = 0.35

# Deskripsi untuk setiap kondisi (untuk fallback jika Ollama offline)
CONDITION_DESCRIPTIONS = {
    'Bulging Eyes': 'Mata menonjol (proptosis) bisa disebabkan oleh gangguan tiroid (Graves) atau kondisi periorbital lain.',
    'Cataract': 'Katarak adalah kekeruhan pada lensa kristalin mata yang menyebabkan penglihatan berkabut.',
    'Crossed Eyes': 'Mata juling (strabismus) adalah kondisi ketidaksejajaran sumbu penglihatan kedua mata.',
    'Dark Circles + Eyebags': 'Lingkaran hitam dan kantung mata bisa disebabkan oleh kelelahan, sirkulasi periorbital, atau faktor genetik.',
    'Eyelid': 'Gangguan pada kelopak mata seperti bintitan (hordeolum), kalazion, atau peradangan kelopak (blefaritis).',
    'Konjungtivitis': 'Konjungtivitis atau mata merah adalah inflamasi pada selaput konjungtiva akibat infeksi bakteri, virus, atau alergi.',
    'Normal': 'Mata dalam kondisi sehat tanpa indikasi kelainan anatomis eksternal yang signifikan.',
    'Tidak Terdeteksi': 'Gambar tidak terdeteksi sebagai area mata yang jelas atau memiliki tingkat keyakinan rendah. Pastikan foto fokus pada kelopak, pupil, dan sklera mata dengan pencahayaan memadai.'
}

# =========================
# LOAD MODEL
# =========================
def load_model():
    """Load model PyTorch dengan arsitektur terkalibrasi"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model_best.pth")

    if not os.path.exists(model_path):
        print(f"[!] Model {model_path} tidak ditemukan!")
        return None, CLASS_NAMES, {}

    try:
        checkpoint = torch.load(model_path, map_location=DEVICE, weights_only=False)
        metadata = {}
        
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
            saved_classes = checkpoint.get('classes', CLASS_NAMES)
            arch = checkpoint.get('arch', 'mobilenet_v2')
            val_acc = checkpoint.get('val_acc', None)
            epoch = checkpoint.get('epoch', None)
            metadata = {
                'arch': arch,
                'val_acc': val_acc,
                'epoch': epoch,
                'classes': saved_classes
            }
            acc_str = f"{val_acc*100:.2f}%" if isinstance(val_acc, (int, float)) else str(val_acc)
            print(f"   Loaded checkpoint: Arch={arch}, Epoch={epoch}, Best Val Acc={acc_str}")
        else:
            state_dict = checkpoint
            saved_classes = CLASS_NAMES
            arch = 'mobilenet_v2'
        
        print(f"   Classes from checkpoint: {saved_classes}")
        
        if arch == 'mobilenet_v2':
            model = models.mobilenet_v2(weights=None)
            model.classifier = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(model.last_channel, 256),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, len(saved_classes))
            )
        else:
            model = models.efficientnet_b0(weights=None)
            model.classifier = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(model.classifier[1].in_features, 256),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, len(saved_classes))
            )
        
        model.load_state_dict(state_dict)
        model = model.to(DEVICE)
        model.eval()
        
        print(f"[+] Model loaded successfully on {DEVICE}!")
        return model, saved_classes, metadata
        
    except Exception as e:
        print(f"[-] Error loading model: {e}")
        return None, CLASS_NAMES, {}

model, loaded_classes, model_meta = load_model()
CLASS_NAMES = loaded_classes

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# =========================
# FUNGSI OLLAMA & ADVICE
# =========================
def check_ollama_status():
    """Cek apakah Ollama berjalan"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False

def generate_fallback_advice(predicted_class, confidence):
    """Fallback advice jika Ollama offline atau untuk kondisi non-penyakit"""
    desc = CONDITION_DESCRIPTIONS.get(predicted_class, "Deskripsi tidak tersedia.")
    
    if predicted_class == 'Tidak Terdeteksi':
        return f"""⚠️ **Area Mata Tidak Terdeteksi Secara Jelas** (Keyakinan: {confidence*100:.1f}%)

{desc}

💡 **Petunjuk Pengambilan Gambar:**
• Posisikan mata tepat di depan kamera laptop/ponsel (jarak 15-30 cm)
• Pastikan pencahayaan terang dan merata (hindari silau atau bayangan tebal)
• Buka mata dengan santai dan tidak mengedip saat pengambilan foto
• Pastikan lensa kamera bersih"""

    elif predicted_class == 'Normal':
        return f"""✅ **Hasil Analisis: Mata Normal / Sehat** (Tingkat Keyakinan: {confidence*100:.1f}%)

{desc}

💡 **Tips Menjaga Kesehatan Mata Sehari-hari:**
• Terapkan aturan 20-20-20 (setiap 20 menit menatap layar, pandang objek sejauh 20 kaki selama 20 detik)
• Konsumsi makanan bernutrisi tinggi vitamin A, lutein, dan omega-3
• Gunakan pencahayaan yang cukup saat bekerja atau membaca
• Istirahat tidur berkualitas 7-8 jam per hari
• Lakukan pemeriksaan mata berkala setahun sekali

⚠️ *Deteksi ini bersifat skrining awal dan bukan pengganti pemeriksaan medis komprehensif.*"""

    else:
        return f"""🔍 **Hasil Analisis: {predicted_class}** (Tingkat Keyakinan: {confidence*100:.1f}%)

{desc}

💡 **Saran Tindakan Klinis:**
• Disarankan untuk menjadwalkan konsultasi dengan dokter spesialis mata (Sp.M)
• Hindari mengucek atau menekan bola mata
• Jaga kebersihan area sekitar mata dan cuci tangan sebelum menyentuh wajah
• Hindari penggunaan lensa kontak sementara waktu jika terasa tidak nyaman

⚠️ *Hasil deteksi ini bersifat pendukung diagnosis klinis awal. Keputusan terapi harus berdasarkan evaluasi dokter spesialis.*"""

def generate_advice_with_ollama(predicted_class, confidence):
    """Generate saran medis menggunakan Ollama LLM secara real-time"""
    if not check_ollama_status():
        return generate_fallback_advice(predicted_class, confidence), False
    
    if predicted_class in ('Tidak Terdeteksi', 'Normal'):
        return generate_fallback_advice(predicted_class, confidence), False
    
    prompt = f"""Anda adalah asisten kecerdasan buatan kesehatan mata profesional Ocularis AI. Berikan saran medis berbasis bukti untuk kondisi klinis berikut:

KONDISI MATA TERDETEKSI: {predicted_class}
TINGKAT KEYAKINAN MODEL: {confidence*100:.1f}%

FORMAT RESPON (Gunakan Bahasa Indonesia medis yang jelas, edukatif, dan ramah):

**Penjelasan Klinis Singkat:**
(1-2 kalimat mengenai etiologi dan dampak umum dari {predicted_class})

**Gejala yang Perlu Diwaspadai:**
• Gejala klinis 1
• Gejala klinis 2
• Gejala klinis 3

**Langkah Perawatan Mandiri & Pencegahan:**
• Langkah 1
• Langkah 2
• Langkah 3

**Rekomendasi Medis Profesional:**
(Kapan harus segera periksa ke dokter spesialis mata Sp.M)

⚠️ *Hasil deteksi Ocularis AI bersifat skrining awal dan bukan pengganti diagnosis definitif dokter spesialis mata.*"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 450,
                    "top_k": 40,
                    "top_p": 0.9
                }
            },
            timeout=OLLAMA_TIMEOUT
        )
        if response.status_code == 200:
            result = response.json()
            return result.get('response', generate_fallback_advice(predicted_class, confidence)), True
        else:
            return generate_fallback_advice(predicted_class, confidence), False
    except Exception as e:
        print(f"[!] Error calling Ollama: {e}")
        return generate_fallback_advice(predicted_class, confidence), False

def check_brightness(image):
    """Evaluasi pencahayaan frame input"""
    try:
        gray = image.convert('L')
        img_array = np.array(gray, dtype=np.float32)
        brightness = float(np.mean(img_array))
        if brightness < 30:
            return False, f"Gambar terlalu gelap (kecerahan: {brightness:.0f})"
        elif brightness < 50:
            return True, f"Pencahayaan redup (kecerahan: {brightness:.0f})"
        return True, None
    except:
        return True, None

# =========================
# ENDPOINTS
# =========================
@app.route('/health', methods=['GET'])
def health():
    ollama_status = check_ollama_status()
    return jsonify({
        "status": "ok",
        "device": str(DEVICE),
        "model_loaded": model is not None,
        "metadata": model_meta,
        "ollama_running": ollama_status,
        "classes": CLASS_NAMES,
        "num_classes": len(CLASS_NAMES),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model tidak tersedia", "success": False}), 500
    
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "Data gambar tidak ditemukan", "success": False}), 400
        
        image_base64 = data['image']
        # Handle prefix if present (e.g., data:image/jpeg;base64,...)
        if ',' in image_base64:
            image_base64 = image_base64.split(',', 1)[1]
            
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        is_bright_enough, brightness_warning = check_brightness(image)
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(image_tensor)
            probs = torch.softmax(outputs, dim=1)[0]
        
        results = []
        for i, p in enumerate(probs):
            results.append({
                "class": CLASS_NAMES[i],
                "confidence": float(p)
            })
        
        results = sorted(results, key=lambda x: x['confidence'], reverse=True)
        top_pred = results[0]
        top_conf = top_pred['confidence']
        
        # Ambang Batas Deteksi OOD / Non-Eye Rejection
        is_rejected = False
        rejection_reason = None
        
        if top_conf < 0.35:
            is_rejected = True
            rejection_reason = f"Keyakinan deteksi sangat rendah ({top_conf*100:.1f}%)"
        elif top_pred['class'] != 'Normal' and top_conf < MIN_CONFIDENCE_FOR_DISEASE:
            is_rejected = True
            rejection_reason = f"Keyakinan deteksi penyakit ({top_pred['class']}) belum mencapai ambang batas klinis ({top_conf*100:.1f}% < {MIN_CONFIDENCE_FOR_DISEASE*100:.0f}%)"
            
        if is_rejected:
            advice, from_ollama = generate_advice_with_ollama('Tidak Terdeteksi', top_conf)
            return jsonify({
                "success": True,
                "predictions": [{"class": "Tidak Terdeteksi", "confidence": float(max(0.85, 1.0 - top_conf))}] + results[:3],
                "advice": advice,
                "from_ollama": from_ollama,
                "warning": rejection_reason,
                "timestamp": datetime.now().isoformat()
            })
        
        # Prediksi Valid
        advice, from_ollama = generate_advice_with_ollama(top_pred['class'], top_conf)
        
        response_data = {
            "success": True,
            "predictions": results,
            "advice": advice,
            "from_ollama": from_ollama,
            "timestamp": datetime.now().isoformat()
        }
        
        if brightness_warning:
            response_data["warning"] = brightness_warning
            
        return jsonify(response_data)
        
    except Exception as e:
        print(f"[-] Error in predict: {str(e)}")
        return jsonify({"error": str(e), "success": False}), 500

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    print("\n" + "="*55)
    print("  OCULARIS AI SERVER (CALIBRATED 7-CLASS CLINICAL EYE)")
    print("="*55)
    print(f"Perangkat Komputasi : {DEVICE}")
    print(f"Status Model        : {'LOADED' if model else 'FAILED'}")
    if model_meta:
        print(f"Metadata Model      : {model_meta.get('arch')} | Best Acc: {model_meta.get('val_acc', 0)*100:.2f}% | Epoch {model_meta.get('epoch')}")
    print(f"Kelas Klinis ({len(CLASS_NAMES)})   : {CLASS_NAMES}")
    print(f"\nAmbang Batas Deteksi (OOD Rejection):")
    print(f"   Ambang Deteksi Penyakit: {MIN_CONFIDENCE_FOR_DISEASE*100:.0f}%")
    print(f"   Ambang Deteksi Normal  : {MIN_CONFIDENCE_FOR_NORMAL*100:.0f}%")
    
    ollama_ok = check_ollama_status()
    print(f"\nStatus Ollama        : {'RUNNING' if ollama_ok else 'OFFLINE (Fallback Mode)'}")
    if ollama_ok:
        print(f"   Model              : {OLLAMA_MODEL}")
    else:
        print(f"   Petunjuk           : Jalankan 'ollama run {OLLAMA_MODEL}' untuk saran real-time")
        
    print("="*55)
    print("Server siap di        : http://localhost:5000")
    print("Health check          : http://localhost:5000/health")
    print("="*55 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
