# 🚜 Radar BEV Industrial

> Transforming standard camera feeds into real-time Bird’s Eye View (BEV) intelligence for industrial environments.

---

## 🚀 Live Release

👉 **[v1.0 - Radar BEV Industrial MVP](https://github.com/nectorcortesr/radar-bev/releases/tag/v1.0)**

---

## 🎥 Demo

*(Add a GIF here showing input video → BEV output)*

---

## 🧠 What is this?

Radar BEV Industrial is a high-performance computer vision system that converts oblique camera feeds into metric Bird’s Eye View (BEV) representations.

It is designed for:

* Collision monitoring
* Proximity detection
* Spatial awareness in mining and industrial yards

---

## ✨ Key Features

* ⚡ **400+ FPS on CPU** (no GPU required)
* 🧮 **Zero Deep Learning** — pure geometry & classical CV
* 🎯 **Precise BEV transformation** using projective geometry
* 🐳 **Fully containerized** with Docker
* 🔄 **CI/CD pipeline** with GitHub Actions

---

## 🏗️ Architecture

*(Optional: add diagram here)*

* HSV segmentation
* Contour detection + spatial moments
* Homography (DLT) transformation
* BEV projection

---

## ⚙️ Quick Start

```bash
xhost +local:docker
docker-compose up --build
```

---

## 📦 Tech Stack

* Python
* OpenCV
* Docker / Docker Compose
* GitHub Actions (CI/CD)

---

## ⚠️ Status

MVP v1.0 released.
Currently evolving towards real-time analytics and AI integration.

---

## 🔜 Roadmap

* Real-time streaming
* Multi-object tracking
* AI-based prediction models
* Visualization dashboards
