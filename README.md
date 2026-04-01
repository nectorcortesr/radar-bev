# 🚜 Industrial BEV Radar for Mining Yards

[![Industrial Perception CI](https://github.com/nectorcortesr/radar-bev/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/radar-bev/actions/workflows/ci.yml)

A classical computer vision pipeline that transforms oblique security camera feeds into metric Bird's Eye View (BEV) systems in real-time, designed for collision monitoring and proximity alerts in open-pit mining operations.

![BEV Demo](output/demo.gif)

## 🚀 Features & Performance
- **Zero Deep Learning:** Relies entirely on HSV color segmentation, spatial moments, and pure projective geometry.
- **Ultra-Low Latency:** Core processing achieves >400 FPS on CPU (deterministically benchmarked via `cProfile`).
- **Interactive Calibration:** 4-point Direct Linear Transform (DLT) interactive tool with JSON state persistence.
- **Production-Ready Architecture:** Clean OOP architecture (SRP), Multi-stage Docker deployment, and automated CI/CD pipeline via GitHub Actions.

## ⚙️ Quick Start
The system runs 100% containerized to prevent dependency conflicts.

```bash
# Allow Docker to connect to the host's X11 socket for GUI rendering
xhost +local:docker

# Build and run the multi-stage container
docker-compose up --build