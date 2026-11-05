import os
import sys
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

IMG_SIZE = 224
BATCH_SIZE = 32
NUM_WORKERS = 0

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}", flush=True)

    val_dir = r"D:\Rizkia\Project Software\Soca_Workspace\val"
    model_path = r"D:\Rizkia\Project Software\Soca_Workspace\model_best.pth"

    val_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_data = datasets.ImageFolder(val_dir, transform=val_transform)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    print(f"Validation samples: {len(val_data)} across {len(val_data.classes)} classes:", flush=True)
    for c in val_data.classes:
        count = len(os.listdir(os.path.join(val_dir, c)))
        print(f"  {c:25s}: {count:3d} images", flush=True)

    checkpoint = torch.load(model_path, map_location=device)
    saved_classes = checkpoint.get('classes', val_data.classes)
    epoch = checkpoint.get('epoch', 'N/A')
    val_acc_saved = checkpoint.get('val_acc', 'N/A')
    arch = checkpoint.get('arch', 'mobilenet_v2')

    print(f"\nModel metadata: Arch={arch}, Best Epoch={epoch}, Saved Acc={val_acc_saved}", flush=True)

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
        # Fallback / EfficientNet
        model = models.efficientnet_b0(weights=None)
        model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(model.classifier[1].in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, len(saved_classes))
        )

    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    all_preds = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_probs.extend(probs.cpu().numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    acc = accuracy_score(all_labels, all_preds)
    print("\n" + "="*65, flush=True)
    print(f"FINAL EVALUATION REPORT - OVERALL ACCURACY: {acc*100:.2f}%", flush=True)
    print("="*65, flush=True)

    print("\nClassification Report (Precision, Recall, F1-Score):", flush=True)
    print("-" * 65, flush=True)
    print(classification_report(all_labels, all_preds, target_names=val_data.classes, digits=4), flush=True)

    print("\nConfusion Matrix:", flush=True)
    print("-" * 65, flush=True)
    cm = confusion_matrix(all_labels, all_preds)
    header = "          " + "".join([f"{c[:6]:>8}" for c in val_data.classes])
    print(header, flush=True)
    for i, row in enumerate(cm):
        row_str = "".join([f"{val:>8}" for val in row])
        print(f"{val_data.classes[i][:9]:<10}{row_str}", flush=True)

    # Error analysis
    print("\nError Analysis (Top misclassifications):", flush=True)
    errors = []
    for i, (true, pred, prob) in enumerate(zip(all_labels, all_preds, all_probs)):
        if true != pred:
            errors.append((val_data.classes[true], val_data.classes[pred], float(max(prob))))

    print(f"  Total validation errors: {len(errors)}/{len(all_labels)} ({len(errors)/len(all_labels)*100:.2f}%)", flush=True)
    err_counts = {}
    for t, p, _ in errors:
        key = f"{t} -> {p}"
        err_counts[key] = err_counts.get(key, 0) + 1
    for k, v in sorted(err_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  Misclassified: {k} ({v} times)", flush=True)

if __name__ == '__main__':
    main()
