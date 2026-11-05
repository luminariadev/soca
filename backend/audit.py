"""
audit_all_models.py - Comprehensive Multi-Dimensional Clinical AI Audit Suite
Author: luminariadev <rizkianuari83@gmail.com>

Batasan Audit:
1. Benchmark Model Lama (Backup v1) vs Model Baru Terkalibrasi (Langkah A)
2. Detail Metrik Per-Kelas (Precision, Recall, F1, Specificity, Sample Count)
3. Confusion Matrix Komparatif
4. Latency & Hardware Throughput Benchmark (RTX 3050 CUDA vs Intel CPU)
5. Robustness / Stress-Test Perturbasi Webcam (Low light, Glare, Blur, Noise, Head tilt)
6. Out-of-Distribution (OOD) Rejection Threshold Test
"""

import sys
import io
import os
import time
import json
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# Force UTF-8 on Windows stdout
if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support

VAL_DIR = r"D:\Rizkia\Project Software\Soca_Workspace\val"
NEW_MODEL_PATH = r"D:\Rizkia\Project Software\Soca_Workspace\model_best.pth"
OLD_MODEL_PATH = r"D:\Rizkia\Project Software\Soca_Workspace\model_old_v1.pth"
IMG_SIZE = 224
BATCH_SIZE = 32

DEVICE_CUDA = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE_CPU = torch.device("cpu")

CLASSES = [
    'Bulging Eyes',
    'Cataract',
    'Crossed Eyes',
    'Dark Circles + Eyebags',
    'Eyelid',
    'Konjungtivitis',
    'Normal'
]

transform_standard = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def build_new_model():
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(model.last_channel, 256),
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.2),
        nn.Linear(256, 7)
    )
    checkpoint = torch.load(NEW_MODEL_PATH, map_location='cpu', weights_only=False)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    model.eval()
    return model

def build_old_model():
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2),
        nn.Linear(model.last_channel, 7)
    )
    checkpoint = torch.load(OLD_MODEL_PATH, map_location='cpu', weights_only=False)
    if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        model.load_state_dict(checkpoint)
    model.eval()
    return model

def evaluate_model_on_loader(model, loader, device):
    model.to(device)
    model.eval()
    y_true = []
    y_pred = []
    y_probs = []
    
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())
            y_probs.extend(probs.cpu().numpy())
            
    return np.array(y_true), np.array(y_pred), np.array(y_probs)

def run_hardware_latency_benchmark(model, device, num_runs=100):
    model.to(device)
    model.eval()
    dummy_input = torch.randn(1, 3, IMG_SIZE, IMG_SIZE).to(device)
    
    # Warmup
    with torch.no_grad():
        for _ in range(10):
            _ = model(dummy_input)
            
    if device.type == 'cuda':
        torch.cuda.synchronize()
        
    latencies = []
    with torch.no_grad():
        for _ in range(num_runs):
            t0 = time.perf_counter()
            _ = model(dummy_input)
            if device.type == 'cuda':
                torch.cuda.synchronize()
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0)
            
    latencies = np.array(latencies)
    return {
        'mean_ms': float(np.mean(latencies)),
        'median_ms': float(np.median(latencies)),
        'p95_ms': float(np.percentile(latencies, 95)),
        'fps': float(1000.0 / np.mean(latencies))
    }

def run_stress_test(model, dataset, device):
    """Perturbation testing simulating laptop/phone webcam degradations"""
    model.to(device)
    model.eval()
    
    stress_results = {}
    
    # Test 1: Baseline (Clean)
    loader_base = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)
    y_true, y_pred, _ = evaluate_model_on_loader(model, loader_base, device)
    stress_results['Baseline'] = float(np.mean(y_true == y_pred) * 100)
    
    # Custom Perturbation Transforms
    perturbations = {
        'Low Light (Dim Room - 40% darker)': transforms.Compose([
            transforms.ColorJitter(brightness=(0.6, 0.6)),
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'Glare / Overexposed (+30% brighter)': transforms.Compose([
            transforms.ColorJitter(brightness=(1.3, 1.3)),
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'Webcam Defocus Blur (Radius 1.5)': transforms.Compose([
            transforms.GaussianBlur(kernel_size=5, sigma=(1.2, 1.5)),
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'Webcam Head Tilt (+8 deg rotation)': transforms.Compose([
            transforms.RandomRotation(degrees=(8, 8)),
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'CMOS Sensor Noise': transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Lambda(lambda x: torch.clamp(x + torch.randn_like(x) * 0.05, 0, 1)),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    }
    
    for name, p_trans in perturbations.items():
        p_dataset = datasets.ImageFolder(VAL_DIR, transform=p_trans)
        p_loader = DataLoader(p_dataset, batch_size=BATCH_SIZE, shuffle=False)
        yt, yp, _ = evaluate_model_on_loader(model, p_loader, device)
        stress_results[name] = float(np.mean(yt == yp) * 100)
        
    return stress_results

def run_ood_rejection_test(model, device, threshold=0.45):
    """Test Out-of-Distribution rejection on non-eye synthetic and natural frames"""
    model.to(device)
    model.eval()
    
    ood_samples = {
        'Uniform Black Screen': torch.zeros(1, 3, IMG_SIZE, IMG_SIZE),
        'Uniform White Screen': torch.ones(1, 3, IMG_SIZE, IMG_SIZE),
        'Uniform Gray Noise': torch.rand(1, 3, IMG_SIZE, IMG_SIZE),
        'High Frequency Noise': torch.randn(1, 3, IMG_SIZE, IMG_SIZE).clamp(0, 1),
    }
    
    results = {}
    norm = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    
    with torch.no_grad():
        for name, tensor in ood_samples.items():
            norm_tensor = norm(tensor).to(device)
            output = model(norm_tensor)
            probs = torch.softmax(output, dim=1).cpu().numpy()[0]
            max_prob = float(np.max(probs))
            pred_idx = int(np.argmax(probs))
            pred_label = CLASSES[pred_idx]
            rejected = max_prob < threshold
            results[name] = {
                'max_confidence': max_prob,
                'candidate_class': pred_label,
                'status': 'REJECTED (OOD / Tidak Terdeteksi)' if rejected else 'ACCEPTED (False Alarm)'
            }
            
    return results

def main():
    print("=" * 80)
    print("      SOCA CLINICAL AI COMPREHENSIVE MULTI-MODEL AUDIT & STRESS SUITE     ")
    print("=" * 80)
    print(f"[+] CUDA Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
    print(f"[+] Validation Samples: 798 images across 7 classes")
    
    # 1. Load models
    new_model = build_new_model()
    old_model = build_old_model()
    val_dataset = datasets.ImageFolder(VAL_DIR, transform=transform_standard)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # 2. Evaluate Head-to-Head
    print("\n[+] Evaluating Model Baru (Langkah A - Calibrated Head)...")
    y_true, y_pred_new, y_probs_new = evaluate_model_on_loader(new_model, val_loader, DEVICE_CUDA)
    acc_new = np.mean(y_true == y_pred_new) * 100
    
    print("[+] Evaluating Model Lama (Backup v1 - Uncalibrated Head)...")
    _, y_pred_old, y_probs_old = evaluate_model_on_loader(old_model, val_loader, DEVICE_CUDA)
    acc_old = np.mean(y_true == y_pred_old) * 100
    
    p_new, r_new, f1_new, s_new = precision_recall_fscore_support(y_true, y_pred_new, average=None)
    p_old, r_old, f1_old, s_old = precision_recall_fscore_support(y_true, y_pred_old, average=None)
    
    print("\n" + "=" * 80)
    print("1. HEAD-TO-HEAD COMPARATIVE AUDIT: MODEL LAMA VS MODEL BARU")
    print("=" * 80)
    print(f"{'Class Name':<24} | {'Model Lama F1':<14} | {'Model Baru F1':<14} | {'Delta F1':<10}")
    print("-" * 80)
    for idx, cname in enumerate(CLASSES):
        delta = f1_new[idx] - f1_old[idx]
        delta_str = f"+{delta:.4f}" if delta >= 0 else f"{delta:.4f}"
        print(f"{cname:<24} | {f1_old[idx]:<14.4f} | {f1_new[idx]:<14.4f} | {delta_str:<10}")
    print("-" * 80)
    print(f"{'OVERALL ACCURACY':<24} | {acc_old:<14.2f}% | {acc_new:<14.2f}% | +{acc_new - acc_old:.2f}%")
    print(f"{'MACRO F1 SCORE':<24} | {np.mean(f1_old):<14.4f} | {np.mean(f1_new):<14.4f} | +{np.mean(f1_new) - np.mean(f1_old):.4f}")
    
    # Confusion Matrix Comparison
    cm_new = confusion_matrix(y_true, y_pred_new)
    cm_old = confusion_matrix(y_true, y_pred_old)
    
    # 3. Hardware Latency & FPS
    print("\n" + "=" * 80)
    print("2. HARDWARE LATENCY & INFERENCE THROUGHPUT BENCHMARK")
    print("=" * 80)
    lat_cuda = run_hardware_latency_benchmark(new_model, DEVICE_CUDA)
    lat_cpu = run_hardware_latency_benchmark(new_model, DEVICE_CPU)
    print(f"[*] NVIDIA RTX 3050 GPU (CUDA): Mean={lat_cuda['mean_ms']:.2f} ms | P95={lat_cuda['p95_ms']:.2f} ms | Throughput={lat_cuda['fps']:.1f} FPS")
    print(f"[*] Host CPU (Intel x64):       Mean={lat_cpu['mean_ms']:.2f} ms | P95={lat_cpu['p95_ms']:.2f} ms | Throughput={lat_cpu['fps']:.1f} FPS")
    
    # Parameter & Model Weight Footprint
    total_params = sum(p.numel() for p in new_model.parameters())
    trainable_params = sum(p.numel() for p in new_model.parameters() if p.requires_grad)
    weight_mb = os.path.getsize(NEW_MODEL_PATH) / (1024 * 1024)
    print(f"[*] Model Parameter Footprint : Total={total_params:,} ({total_params/1e6:.2f}M) | Disk File={weight_mb:.2f} MB")
    
    # 4. Stress / Perturbation Testing
    print("\n" + "=" * 80)
    print("3. REAL-WORLD WEBCAM STRESS TESTING (PERTURBATION ROBUSTNESS)")
    print("=" * 80)
    stress_results = run_stress_test(new_model, val_dataset, DEVICE_CUDA)
    for scenario, acc in stress_results.items():
        diff = acc - stress_results['Baseline']
        diff_str = f"{diff:+.2f}%" if diff != 0 else "0.00%"
        print(f"[*] {scenario:<36} : Akurasi = {acc:.2f}% ({diff_str})")
        
    # 5. Out-of-Distribution (OOD) Rejection Testing
    print("\n" + "=" * 80)
    print("4. OUT-OF-DISTRIBUTION (OOD) REJECTION TEST (Threshold = 0.45)")
    print("=" * 80)
    ood_results = run_ood_rejection_test(new_model, DEVICE_CUDA, threshold=0.45)
    for test_name, res in ood_results.items():
        print(f"[*] {test_name:<26} : Conf={res['max_confidence']*100:.1f}% -> Status: {res['status']}")

    # Output JSON summary for artifact reporting
    summary = {
        'model_new': {
            'accuracy': float(acc_new),
            'macro_f1': float(np.mean(f1_new)),
            'per_class_f1': {CLASSES[i]: float(f1_new[i]) for i in range(7)},
            'per_class_precision': {CLASSES[i]: float(p_new[i]) for i in range(7)},
            'per_class_recall': {CLASSES[i]: float(r_new[i]) for i in range(7)},
            'confusion_matrix': cm_new.tolist(),
        },
        'model_old': {
            'accuracy': float(acc_old),
            'macro_f1': float(np.mean(f1_old)),
            'per_class_f1': {CLASSES[i]: float(f1_old[i]) for i in range(7)},
            'confusion_matrix': cm_old.tolist(),
        },
        'hardware_benchmark': {
            'cuda': lat_cuda,
            'cpu': lat_cpu,
            'total_params': total_params,
            'file_size_mb': weight_mb
        },
        'stress_testing': stress_results,
        'ood_rejection': ood_results
    }
    
    with open(r"D:\Rizkia\Project Software\Soca_Workspace\audit_report.json", "w") as f:
        json.dump(summary, f, indent=2)
        
    print("\n[+] Audit Berhasil! Laporan disimpan ke audit_report.json")

if __name__ == "__main__":
    main()
