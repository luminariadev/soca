import os
import sys
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report

BATCH_SIZE = 32
EPOCHS = 20
IMG_SIZE = 224
LEARNING_RATE = 0.0003
NUM_WORKERS = 0

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}", flush=True)
    if device.type == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)} (VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB)", flush=True)

    train_dir = r"D:\Rizkia\Project Software\Soca_Workspace\train"
    val_dir = r"D:\Rizkia\Project Software\Soca_Workspace\val"

    # Medically safe transforms (NO hue jitter, NO extreme rotation)
    train_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=(-5, 5)),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.0),
        transforms.RandomResizedCrop(IMG_SIZE, scale=(0.9, 1.0)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_data = datasets.ImageFolder(train_dir, transform=train_transform)
    val_data = datasets.ImageFolder(val_dir, transform=val_transform)

    print(f"Classes ({len(train_data.classes)}): {train_data.classes}", flush=True)
    print(f"Train samples: {len(train_data)}, Val samples: {len(val_data)}", flush=True)

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, pin_memory=(device.type == "cuda"))
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=(device.type == "cuda"))

    # MobileNetV2 architecture with calibrated classifier
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    # Freeze only the first layer
    for param in model.features[0].parameters():
        param.requires_grad = False

    # Balanced classifier: 1 dropout layer (0.3), NOT 0.6 + 0.4
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(model.last_channel, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, len(train_data.classes))
    )

    model = model.to(device)

    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)
    scaler = torch.amp.GradScaler('cuda', enabled=(device.type == "cuda"))

    best_acc = 0.0
    patience = 6
    patience_counter = 0

    print("\n" + "="*65, flush=True)
    print("STARTING LANGKAH A (Balanced 7-Class Dataset + MobileNetV2)", flush=True)
    print("="*65, flush=True)

    for epoch in range(EPOCHS):
        t0 = time.time()
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()

            with torch.amp.autocast('cuda', enabled=(device.type == "cuda")):
                outputs = model(images)
                loss = criterion(outputs, labels)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            train_loss += loss.item() * labels.size(0)
            _, predicted = torch.max(outputs, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()

        train_acc = train_correct / train_total
        avg_train_loss = train_loss / train_total

        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                with torch.amp.autocast('cuda', enabled=(device.type == "cuda")):
                    outputs = model(images)
                    loss = criterion(outputs, labels)

                val_loss += loss.item() * labels.size(0)
                _, predicted = torch.max(outputs, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
                all_preds.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        val_acc = val_correct / val_total
        avg_val_loss = val_loss / val_total
        elapsed = time.time() - t0

        scheduler.step()
        curr_lr = scheduler.get_last_lr()[0]

        print(f"Epoch {epoch+1:2d}/{EPOCHS} [{elapsed:4.1f}s] | Train Loss: {avg_train_loss:.4f} Acc: {train_acc*100:5.2f}% | Val Loss: {avg_val_loss:.4f} Acc: {val_acc*100:5.2f}% | LR: {curr_lr:.6f}", flush=True)

        # Checkpoint if best val accuracy
        if val_acc > best_acc:
            best_acc = val_acc
            patience_counter = 0
            save_path = r"D:\Rizkia\Project Software\Soca_Workspace\model_best.pth"
            torch.save({
                'model_state_dict': model.state_dict(),
                'classes': train_data.classes,
                'val_acc': val_acc,
                'val_loss': avg_val_loss,
                'epoch': epoch + 1,
                'arch': 'mobilenet_v2'
            }, save_path)
            print(f"   -> [BEST] Model saved with Val Acc: {val_acc*100:.2f}%", flush=True)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"\n[Early Stopping] No improvement for {patience} epochs. Stopping to prevent overfitting.", flush=True)
                break

    print("\n" + "="*65, flush=True)
    print(f"Langkah A Training Finished! Best Validation Accuracy: {best_acc*100:.2f}%", flush=True)
    print("="*65, flush=True)

if __name__ == '__main__':
    main()
