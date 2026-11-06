"""Intelligent heuristic fallback generator for offline, test, and fallback execution.

Provides academically rigorous, domain-aware blueprint generation when a live
Gemini API key is unavailable, depleted, or in offline test environments.
"""
from typing import Any
import re
from ai_engine.schemas import (
    FeasibilityResult,
    ScopeResult,
    TechnologyResult,
    PlanningResult,
    PlannedPhase,
    WeeklyMilestone,
    RiskResult,
    ProjectRisk,
)


def _extract_topic(idea: str) -> str:
    cleaned = idea.strip()
    words = [w for w in re.findall(r"[A-Za-z0-9]+", cleaned) if len(w) > 2]
    return " ".join(words[:4]).title() if words else "Academic Software Project"


DOMAINS_CATALOG: dict[str, dict[str, Any]] = {
    "smart_waste": {
        "keywords": ["waste", "garbage", "trash", "recycle", "segregat", "bin", "dumpster", "clean city", "sanitation", "compost"],
        "title": "IoT-Enabled Smart Waste Segregation & Dynamic Route Optimization System",
        "problem_statement": (
            "Urban municipal waste management suffers from static collection schedules, overflowing dumpsters, and "
            "lack of waste segregation at source. Without real-time fill-level telemetry and dynamic route scheduling, "
            "collection trucks waste excessive fuel, emit unnecessary carbon, and miss overflowing bins, causing severe "
            "sanitation hazards and citizen dissatisfaction across municipal wards."
        ),
        "skills": [
            "Embedded C/C++ (ESP32/Arduino)",
            "Ultrasonic & Load Cell Sensor Calibration",
            "MQTT Telemetry Protocol (Mosquitto)",
            "Computer Vision (YOLOv8 & OpenCV)",
            "FastAPI & WebSockets",
            "PostgreSQL / PostGIS",
            "Leaflet.js GIS Mapping",
        ],
        "resources": [
            "ESP32 / Raspberry Pi edge development board with Wi-Fi / GSM module",
            "HC-SR04 ultrasonic distance sensors & HX711 load-cell amplifiers",
            "Kaggle Waste Classification / TACO benchmark dataset for visual segregation",
            "OpenStreetMap / Leaflet GIS routing service or Google OR-Tools",
        ],
        "challenges": [
            "Irregular waste accumulation geometry inside bins causing ultrasonic reflection noise",
            "Battery consumption optimization and intermittent outdoor cellular/Wi-Fi connectivity",
            "Accurate visual segregation under poor lighting or soiled material conditions",
            "Multi-vehicle dynamic traveling salesperson (VRP) computational scaling under live traffic",
        ],
        "recommendations": [
            "Implement rolling median filtering on ultrasonic sensor readings to discard erroneous spikes from uneven trash piles.",
            "Deploy a lightweight quantized YOLOv8-Nano model on edge hardware to maintain real-time inference under 250ms.",
            "Formulate the vehicle routing problem using Google OR-Tools with bin fill-level capacity constraints.",
            "Incorporate edge-side SQLite buffering to ensure zero telemetry data loss during network dropouts.",
        ],
        "assumptions": [
            "Municipal bins can be fitted with standardized waterproof sensor enclosures.",
            "Garbage collection drivers have access to smartphone screens for viewing optimized pickup turn-by-turn routes.",
            "City road network topology data is accessible via OpenStreetMap.",
        ],
        "target_users": [
            "Municipal sanitation workers and garbage collection truck drivers",
            "City ward waste management supervisors and route dispatchers",
            "Municipal urban planning administrators and environmental audit officers",
            "Local citizens reporting localized overflow or illegal dumping",
        ],
        "functional_requirements": [
            "Real-time ultrasonic & weight sensor telemetry ingestion with automated bin fill-percentage calculation and threshold alerting (>85% capacity)",
            "Dynamic vehicle route optimization engine calculating shortest pickup paths using Dijkstra/A* graph algorithms or Google OR-Tools",
            "Computer vision waste classification module segregating recyclable, organic, and hazardous waste categories using YOLOv8/CNN",
            "Municipal operations GIS map dashboard displaying color-coded bin statuses, collection vehicle locations, and historical fill patterns",
            "Citizen incident reporting portal supporting geolocated photo uploads, automated categorization, and dispatch status tracking",
            "Automated scheduled dispatch reports and fuel/time efficiency analytics generated for city sanitation supervisors",
        ],
        "non_functional_requirements": [
            "Real-time telemetry ingestion latency < 1000ms from sensor broadcast to dashboard update",
            "Edge camera waste classification inference time < 300ms per frame",
            "Route optimization re-computation executed within 3.0 seconds for up to 100 municipal collection points",
            "System availability >= 99.5% with offline edge SQLite telemetry buffering during network dropouts",
        ],
        "mvp_features": [
            "Working ultrasonic sensor prototype transmitting fill levels via MQTT to local backend broker",
            "YOLOv8 inference pipeline accurately identifying 3 waste classes on test images with >80% accuracy",
            "Interactive GIS map showing simulated bins with dynamic route visualization",
            "Automated threshold alert notifications triggered when bin fill reaches critical levels",
        ],
        "out_of_scope": [
            "Physical hydraulic bin-lifting mechanical truck retrofits",
            "Nationwide multi-city cellular roaming telecommunication infrastructure",
            "Commercial resident billing, payment gateways, and municipal tax penalty enforcement",
        ],
        "deliverables": [
            "Working sensor telemetry prototype and edge vision segregation model codebase",
            "Full-stack GIS route optimization dashboard with live MQTT telemetry feed",
            "Empirical performance report documenting route length reduction and model classification accuracy",
            "CapStone thesis document, architecture blueprints, and viva demonstration slides",
        ],
        "success_criteria": [
            ">= 85% waste segregation classification accuracy on held-out test dataset",
            "Demonstrated >= 15% reduction in simulated collection route travel distance compared to static routing",
            "Telemetry pipeline latency verified under 1000ms end-to-end",
            "Zero data loss during simulated 15-minute network disconnect using edge caching",
        ],
        "frontend": ["React.js", "Leaflet.js / MapLibre GL", "TailwindCSS", "Recharts (Sensor Analytics)", "Lucide Icons"],
        "backend": ["FastAPI (Python 3.12)", "Eclipse Mosquitto (MQTT Broker)", "asyncio & WebSockets", "Pydantic v2"],
        "database": ["PostgreSQL with PostGIS extension", "TimescaleDB (Sensor Time-Series)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["YOLOv8 (Ultralytics)", "OpenCV", "Google OR-Tools (Vehicle Routing)", "PyTorch", "NumPy & Pandas"],
        "deployment": ["Docker & Docker Compose", "Vercel / Netlify (Frontend)", "Render / Railway (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI", "PlatformIO / Arduino IDE"],
        "alternatives": [
            "HTTP Polling vs MQTT: MQTT selected because its 2-byte header and publish-subscribe model reduce bandwidth and battery draw by over 60% compared to periodic HTTP polling.",
            "PostGIS vs MongoDB GeoJSON: PostgreSQL with PostGIS selected for superior spatial indexing (R-Tree), ACID transaction guarantees, and complex relational joins with vehicle manifests.",
            "YOLOv8 vs Faster R-CNN: YOLOv8 selected for single-stage real-time edge inference suitable for low-power edge compute at 30+ FPS.",
        ],
        "rationale": (
            "The recommended stack bridges low-power IoT telemetry with high-performance spatial optimization and "
            "real-time computer vision. MQTT ensures efficient sensor message delivery over cellular/Wi-Fi networks, while "
            "FastAPI seamlessly exposes WebSocket feeds to a React + Leaflet GIS frontend. PostGIS enables sub-millisecond "
            "geographic spatial indexing, and YOLOv8 provides high-speed, lightweight classification for edge waste sorting."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. IoT Telemetry Layer: Mosquitto MQTT broker provides a lightweight pub/sub model essential for battery-powered bin microcontrollers.\n"
            "2. Service & Real-Time Tier: FastAPI handles incoming MQTT events asynchronously and broadcasts live updates to frontend clients over WebSockets.\n"
            "3. Spatial Persistence Tier: PostgreSQL with PostGIS extension natively supports R-tree spatial indexing and distance queries required for dynamic vehicle routing.\n"
            "4. Edge Vision Engine: YOLOv8 delivers high mean Average Precision (mAP) with sub-300ms inference times on resource-constrained hardware.\n"
            "5. Presentation Tier: React + Leaflet.js provides fluid, interactive map rendering of bin locations and color-coded fill statuses without proprietary map licensing costs."
        ),
        "limitations": [
            "Ultrasonic distance sensors require clean line-of-sight and may degrade if physical debris coats the sensor lens.",
            "GPS precision may fluctuate by +/- 5 meters in dense urban high-rise canyons.",
            "Edge computer vision requires dedicated local hardware acceleration (e.g. Coral TPU or Raspberry Pi 4/5) to achieve 20+ FPS.",
        ],
    },
    "face_attendance": {
        "keywords": ["attendance", "face", "facial", "biometric", "classroom", "proxy", "roll call", "student check"],
        "title": "AI-Powered Automated Classroom Attendance System via Multi-Face Recognition",
        "problem_statement": (
            "Traditional manual roll calls and contact biometric fingerprint scanners suffer from severe instructional "
            "time wastage (10 to 15 minutes per lecture), susceptibility to proxy attendance, physical congestion at entryways, "
            "and hygiene concerns in high-density educational environments. Educational institutions need a non-intrusive, "
            "real-time multi-face recognition system that autonomously registers student attendance from classroom camera feeds."
        ),
        "skills": [
            "Computer Vision & OpenCV",
            "Face Detection (RetinaFace / MTCNN)",
            "Deep Metric Learning (ArcFace / FaceNet)",
            "Vector Similarity Indexing (Faiss / pgvector)",
            "Anti-Spoofing & Liveness Detection",
            "FastAPI & WebSockets",
            "React.js & WebRTC Video Streaming",
        ],
        "resources": [
            "High-definition RTSP IP Camera or USB 1080p wide-angle camera",
            "Standard face benchmark datasets (LFW, CelebA, WiderFace) for validation",
            "CUDA-capable GPU workstation or cloud instance for face embedding extraction",
            "Student identity roster with enrolled baseline reference portraits",
        ],
        "challenges": [
            "Variations in ambient classroom illumination, side-angles, and motion blur",
            "Partial face occlusions caused by spectacles, facial masks, hair, or leaning postures",
            "Vulnerability to presentation attacks using printed photographs or smartphone screen replays",
            "Sub-second verification latency when comparing multiple faces simultaneously against hundreds of student embeddings",
        ],
        "recommendations": [
            "Employ RetinaFace for robust multi-scale face localization capable of detecting small or angled faces across classroom rows.",
            "Integrate ArcFace additive angular margin loss embeddings for superior discriminative feature separation.",
            "Deploy a lightweight passive liveness detector (eye-blink and texture frequency analysis) to eliminate photo/screen spoofing.",
            "Utilize Faiss or pgvector for sub-50ms nearest-neighbor vector similarity search across the student roster.",
        ],
        "assumptions": [
            "Classroom is equipped with a camera positioned with adequate frontal view coverage of student seating areas.",
            "Students participate in an initial one-time enrolment capture under standardized lighting conditions.",
            "Institution complies with local student biometric privacy and data protection policies.",
        ],
        "target_users": [
            "Course instructors and teaching assistants managing daily lectures",
            "Department academic coordinators and attendance compliance auditors",
            "Enrolled students tracking their real-time attendance percentages and absence records",
            "Institutional IT administrators configuring camera nodes and student rosters",
        ],
        "functional_requirements": [
            "Real-time multi-face detection and landmark alignment from live classroom RTSP/webcam video feeds using RetinaFace",
            "512-dimensional facial embedding extraction and cosine similarity verification against registered student database using ArcFace",
            "Anti-spoofing liveness detection (blink detection, micro-movement, and texture analysis) to prevent static photo and screen replay fraud",
            "Automated lecture attendance logging with timestamped entry/exit tracking and duplicate check-in suppression",
            "Instructor dashboard displaying live classroom head-count, recognized student cards, and manual attendance override controls",
            "Automated export of attendance compliance reports formatted for university ERP systems (CSV/Excel/PDF)",
        ],
        "non_functional_requirements": [
            "Multi-face detection and embedding matching latency < 350ms per video frame for up to 30 simultaneous faces",
            "Face verification accuracy >= 98.5% True Positive Rate under normal classroom illumination",
            "Presentation attack detection (anti-spoofing) error rate < 2.0%",
            "GDPR / FERPA compliant biometric security: facial embeddings stored as one-way vectors with raw face images encrypted at rest",
        ],
        "mvp_features": [
            "Webcam-based student enrollment module generating stored 512-d ArcFace embeddings",
            "Real-time multi-face detection and recognition loop recognizing enrolled students on live webcam stream",
            "Automated attendance check-in table updating dynamically upon successful facial verification",
            "Faculty lecture session management interface with attendance summary export",
        ],
        "out_of_scope": [
            "Campus-wide 24/7 continuous CCTV public surveillance tracking outside academic lecture halls",
            "Hardware manufacturing of proprietary biometric turnstiles or electromagnetic door lock actuators",
            "Off-campus student location tracking via mobile GPS",
        ],
        "deliverables": [
            "Complete face recognition pipeline source code with RetinaFace, ArcFace, and anti-spoofing modules",
            "Instructor React web dashboard with real-time video feed and attendance status tables",
            "Empirical evaluation report documenting recognition accuracy, latency, and spoof rejection benchmarks",
            "Final capstone documentation, architecture diagrams, and recorded live demo",
        ],
        "success_criteria": [
            "Achieve >= 98% recognition accuracy on enrolled student test cohort",
            "Maintain average processing latency below 400ms per frame on standard GPU compute",
            "100% rejection rate against static printed photo presentation attacks",
            "Eliminate 100% of proxy attendance during simulated lecture sessions",
        ],
        "frontend": ["React.js", "WebRTC / MediaDevices API", "TailwindCSS", "Canvas Video Overlay", "Lucide Icons"],
        "backend": ["FastAPI (Python 3.12)", "WebSockets (Live Roster Stream)", "asyncio", "Pydantic v2"],
        "database": ["PostgreSQL with pgvector extension", "SQLite (Local Cache)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["InsightFace (ArcFace + RetinaFace)", "OpenCV", "PyTorch", "Faiss (Vector Search)", "NumPy"],
        "deployment": ["Docker", "CUDA Runtime Container", "Vercel (Frontend)", "Self-Hosted / Cloud VM (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI", "Ruff / Black"],
        "alternatives": [
            "Haar Cascades vs RetinaFace: Haar cascades selected for historical simplicity but rejected due to poor accuracy on angled or partially occluded faces; RetinaFace chosen for state-of-the-art multi-scale face localization.",
            "Eigenfaces / LBPH vs ArcFace: Traditional LBPH was evaluated but fails under lighting variations; ArcFace chosen for deep angular margin loss achieving 99.8% LFW accuracy.",
            "FaceNet vs InsightFace: InsightFace selected for its integrated high-speed detection, 2D/3D alignment, and quantized ONNX runtime support.",
        ],
        "rationale": (
            "The architecture prioritizes sub-second inference latency, biometric security, and robustness against classroom "
            "environmental variables. InsightFace delivers deep metric embeddings that are searched via pgvector in milliseconds, "
            "while FastAPI and WebSockets provide high-throughput live feed telemetry directly to the instructor's browser interface."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. Vision Inference Pipeline: RetinaFace + ArcFace yields high discriminative capacity, separating enrolled faces even under moderate pose angles.\n"
            "2. Vector Indexing Tier: pgvector extension within PostgreSQL provides HNSW vector similarity search, eliminating the need for a separate vector database cluster.\n"
            "3. Streaming & Service Tier: FastAPI combined with WebSockets allows the backend to stream recognition bounding boxes and student IDs back to the React UI with sub-100ms transport overhead.\n"
            "4. Privacy & Biometrics: Facial embeddings are irreversible 512-dimensional floating-point vectors, fulfilling academic data protection standards."
        ),
        "limitations": [
            "Recognition accuracy degrades if classroom ambient lighting drops below 50 lux without auxiliary illumination.",
            "Extreme camera angles (>45 degrees yaw/pitch) may cause face detection dropouts.",
            "Running multi-stream RTSP decoding concurrently requires dedicated GPU VRAM (>= 4GB).",
        ],
    },
    "healthcare_prescription": {
        "keywords": ["prescription", "medicine", "drug", "pharmacy", "medical ocr", "doctor notes", "dosage", "clinical notes", "contraindication"],
        "title": "Deep Learning Medical Prescription OCR & Drug Interaction Screening System",
        "problem_statement": (
            "Handwritten clinical prescriptions remain a leading cause of medication dispensing errors, adverse drug interactions, "
            "and pharmacist burnout due to poor handwriting legibility, non-standard abbreviations, and absence of real-time automated "
            "drug contraindication cross-referencing in busy outpatient pharmacy workflows."
        ),
        "skills": [
            "Computer Vision & OCR (TrOCR / Tesseract)",
            "Clinical NLP & Named Entity Recognition (SpaCy / BioBERT)",
            "Drug Ontology Mapping (RxNorm / ATC Classification)",
            "FastAPI Microservice Architecture",
            "React.js High-Resolution Document Canvas",
            "PostgreSQL Relational Schema Design",
        ],
        "resources": [
            "Standard clinical prescription handwriting datasets (IAM / synthetic prescription images)",
            "OpenFDA and RxNorm pharmaceutical interaction database APIs",
            "GPU compute environment for fine-tuned Vision-Encoder-Decoder OCR inference",
            "Standard medical terminology dictionaries (SNOMED-CT / ICD-10)",
        ],
        "challenges": [
            "Severe cursive handwriting irregularities, variable ink pressure, and skewed camera angles",
            "Distinguishing between look-alike and sound-alike (LASA) pharmaceutical drug names",
            "Complex multi-drug regimen interaction combinatorial matrix evaluation",
            "Stringent patient health information (PHI) confidentiality and HIPAA compliance requirements",
        ],
        "recommendations": [
            "Utilize transformer-based TrOCR fine-tuned on cursive medical text to outperform traditional rule-based OCR engines.",
            "Implement Levenshtein distance and phonetic matching against the RxNorm drug catalog to rectify OCR character errors.",
            "Pre-cache common drug-drug interaction contraindication tables locally to enable sub-50ms pharmacist screening alerts.",
            "Enforce client-side image redaction of sensitive patient identifiers before cloud processing.",
        ],
        "assumptions": [
            "Input prescription images have sufficient resolution (>= 300 DPI) and minimal physical tearing.",
            "Clinical interaction rules follow standardized medical authority guidelines.",
            "System is operated as an assistive validation tool with mandatory licensed pharmacist sign-off.",
        ],
        "target_users": [
            "Licensed clinical and retail hospital pharmacists",
            "Outpatient dispensary staff and pharmacy technicians",
            "General physicians reviewing patient multi-medication histories",
            "Healthcare quality and patient safety audit officers",
        ],
        "functional_requirements": [
            "High-resolution prescription image ingestion, perspective correction, binarization, and noise reduction",
            "Handwritten text recognition (HTR) pipeline extracting medicine names, dosage frequencies, and duration using TrOCR / Tesseract",
            "Entity extraction and normalization mapping brand names to standardized generic RxNorm / ATC pharmacological codes",
            "Real-time drug-drug interaction (DDI) contraindication screening engine querying clinical pharmaceutical databases",
            "Pharmacist review portal highlighting detected medicines with confidence scores, extracted dosage tags, and red-flag interaction warnings",
            "Digital prescription validation audit trail and patient dosage summary PDF export",
        ],
        "non_functional_requirements": [
            "Prescription OCR and entity extraction response time < 2500ms per standard document page",
            "Drug-drug interaction screening evaluation latency < 100ms once entities are normalized",
            "Drug name character recognition accuracy >= 94% on legible handwriting benchmarks",
            "Zero persistence of unencrypted Protected Health Information (PHI) to non-volatile storage",
        ],
        "mvp_features": [
            "Prescription image upload portal with automated crop and contrast enhancement",
            "TrOCR inference pipeline identifying at least 3 distinct prescribed medicines with confidence metrics",
            "Interactive dosage and drug interaction validation table alerting user of high-risk drug pairs",
            "Exportable pharmacist review summary verification sheet",
        ],
        "out_of_scope": [
            "Direct automated dispensing robotics or physical pill-counting machinery hardware",
            "Automated electronic health insurance reimbursement billing workflows",
            "Full electronic health record (EHR) hospital system replacement",
        ],
        "deliverables": [
            "End-to-end prescription OCR and clinical entity extraction pipeline codebase",
            "Pharmacist validation web application with interactive bounding-box document viewer",
            "Empirical evaluation report documenting OCR character accuracy, entity recall, and interaction latency",
            "Complete academic thesis report, architecture specifications, and oral viva slides",
        ],
        "success_criteria": [
            ">= 92% Top-1 drug entity recognition accuracy on held-out test prescription set",
            "100% detection rate of known high-severity drug interaction pairs in benchmark test cases",
            "End-to-end document processing pipeline completed in under 3.0 seconds",
            "Validated against at least 100 real-world or synthetic handwritten prescription samples",
        ],
        "frontend": ["React.js", "PDF.js / Canvas Document Viewer", "TailwindCSS", "Lucide Icons", "Radix UI Primitives"],
        "backend": ["FastAPI (Python 3.12)", "Uvicorn ASGI Server", "Pydantic v2", "asyncio"],
        "database": ["PostgreSQL (Relational RxNorm schema)", "SQLite (Development)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["TrOCR (Hugging Face Transformers)", "SpaCy (Medical NER)", "OpenCV", "PyTorch", "RapidFuzz"],
        "deployment": ["Docker", "Vercel (Frontend)", "Railway / AWS EC2 with GPU (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI", "Black / Flake8"],
        "alternatives": [
            "Tesseract OCR vs TrOCR: Tesseract is fast on printed documents but fails on cursive medical handwriting (<55% accuracy); TrOCR leverages Vision Transformer architectures yielding >90% accuracy on handwritten text.",
            "Regex Rule Matching vs SpaCy BioBERT NER: Regex is brittle against spelling variations; SpaCy NER with fuzzy string distance provides robust pharmacological entity normalization.",
            "Live External API vs Local RxNorm Database: Local PostgreSQL RxNorm tables eliminate cloud API rate-limiting and ensure sub-50ms contraindication query latency.",
        ],
        "rationale": (
            "The selected stack combines state-of-the-art vision-transformer OCR with high-speed local pharmaceutical entity "
            "normalization. TrOCR handles handwriting variations, while FastAPI and PostgreSQL deliver instant clinical checks "
            "without cloud latency bottlenecks."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. OCR Modeling Tier: TrOCR combines an image transformer encoder with an autoregressive text decoder, ideal for sequential cursive medical handwriting.\n"
            "2. Clinical Normalization Tier: SpaCy and RapidFuzz resolve brand names to generic ATC/RxNorm identifiers to ensure deterministic rule lookups.\n"
            "3. Service Layer: FastAPI processes document payloads asynchronously, separating heavy ML inference from lightweight client communication.\n"
            "4. Presentation Tier: React with Canvas document overlay highlights detected medication text directly over the scanned prescription for rapid pharmacist verification."
        ),
        "limitations": [
            "Completely illegible or severely smudged handwriting requires mandatory human pharmacist clarification.",
            "TrOCR transformer inference requires dedicated GPU compute (or quantized ONNX CPU runtime with ~4s latency).",
            "Drug interaction engine coverage depends on completeness of the underlying RxNorm/OpenFDA open-source datasets.",
        ],
    },
    "disaster_assessment": {
        "keywords": ["disaster", "drone", "aerial", "flood", "earthquake", "damage assessment", "satellite", "rescue", "emergency map", "wildfire"],
        "title": "Real-Time Disaster Damage Assessment & Emergency Route Mapping via Aerial Imagery",
        "problem_statement": (
            "Post-disaster rescue and damage mitigation efforts are severely bottlenecked by delayed, manual field reconnaissance across "
            "widespread disaster zones. Emergency responders lack real-time aerial damage heatmaps, flooded road detection, and localized "
            "structural risk scoring to prioritize urgent life-saving interventions and equipment dispatch."
        ),
        "skills": [
            "Deep Learning Semantic Segmentation (U-Net / Mask R-CNN)",
            "Geospatial Image Processing (GDAL / Rasterio)",
            "Spatial Database Management (PostGIS)",
            "FastAPI Asynchronous Pipeline",
            "Leaflet / MapLibre Satellite GIS",
            "PyTorch & Torchvision",
        ],
        "resources": [
            "High-resolution aerial / drone orthomosaic imagery or xBD disaster benchmark dataset",
            "OpenStreetMap road network shapefiles",
            "CUDA GPU workstation for high-resolution tile segmentation",
            "Digital Elevation Models (DEM) for flood extent simulation",
        ],
        "challenges": [
            "Massive file sizes of gigapixel drone orthomosaics requiring rapid tile chunking",
            "Complex spectral overlap between standing flood water, muddy terrain, and building shadows",
            "Real-time route recalculation when primary arterial roads are partially submerged or obstructed",
            "Bandwidth constraints when operating in disaster zones with damaged telecom towers",
        ],
        "recommendations": [
            "Implement a spatial tiling pyramid pipeline to process orthomosaics in parallel 512x512 tile chunks.",
            "Train an ensemble U-Net model with pre-trained ResNet-50 backbones to segment damaged building footprints.",
            "Utilize PostGIS spatial graph shortest-path routing (pgRouting) with dynamic penalty weights on flooded corridors.",
            "Design the frontend to function with local offline tile caching for field operations without active internet.",
        ],
        "assumptions": [
            "Drone surveys provide orthorectified imagery with embedded GPS EXIF tags.",
            "Emergency personnel can access a ruggedized tablet or laptop with local map storage.",
            "Initial disaster reconnaissance captures target zones within 24 hours of event occurrence.",
        ],
        "target_users": [
            "Emergency search-and-rescue teams (NDRF / FEMA / Red Cross)",
            "Municipal civil defense coordinators and urban planners",
            "First responders navigating ambulance and supply transport corridors",
            "Disaster relief logistics coordinators",
        ],
        "functional_requirements": [
            "High-resolution aerial / drone orthomosaic imagery ingestion, georeferencing, and spatial tiling pipeline",
            "Deep learning semantic segmentation identifying structural building damage levels (undamaged, minor, major, destroyed)",
            "Flood water extent and road blockage obstacle detection using multispectral and RGB aerial feature maps",
            "Interactive emergency operations GIS map rendering damage severity heatmaps and affected population overlays",
            "Automated rescue route calculation identifying clear, unblocked transportation corridors for first responders",
            "Situation report generator aggregating damage statistics, critical facility status, and priority resource allocation manifests",
        ],
        "non_functional_requirements": [
            "Spatial tile processing and damage classification throughput > 10 tiles/second on GPU",
            "Emergency evacuation route re-calculation latency < 2.0 seconds across 50km road network",
            "Semantic segmentation mIoU (Mean Intersection over Union) >= 0.78 on disaster benchmark sets",
            "High reliability with offline PWA map caching when cellular backhaul is severed",
        ],
        "mvp_features": [
            "Drone image tile uploader with automatic geographic bounding box extraction",
            "Pre-trained segmentation model identifying collapsed structures and flood boundaries on test imagery",
            "Interactive GIS map highlighting damaged building footprints and color-coded road passability",
            "Automated emergency situation summary export listing total affected area and blocked roads",
        ],
        "out_of_scope": [
            "Direct autonomous drone flight hardware manufacturing or avionics autopilot firmware",
            "Satellite constellation tasking and orbital telecommunication infrastructure",
            "Long-term post-disaster insurance financial compensation appraisal",
        ],
        "deliverables": [
            "Complete geospatial aerial damage assessment and route optimization codebase",
            "Interactive emergency operations GIS dashboard with real-time hazard layers",
            "Empirical evaluation report documenting segmentation mIoU, inference latency, and routing accuracy",
            "Comprehensive capstone documentation, architecture blueprints, and viva slide deck",
        ],
        "success_criteria": [
            "Achieve >= 80% mIoU in structural damage classification on xBD test benchmark",
            "Demonstrate successful identification of blocked corridors in 100% of simulated disaster scenarios",
            "Complete situational report generation in under 5.0 seconds from image upload",
            "End-to-end verification during live simulated emergency viva demonstration",
        ],
        "frontend": ["React.js", "Leaflet.js / MapLibre GL", "TailwindCSS", "Recharts", "Lucide Icons"],
        "backend": ["FastAPI (Python 3.12)", "Celery / Background Tasks", "asyncio", "Pydantic v2"],
        "database": ["PostgreSQL with PostGIS & pgRouting extensions", "SQLite (Local Cache)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["PyTorch", "Torchvision (U-Net & DeepLabV3+)", "Rasterio / GDAL", "OpenCV", "NumPy"],
        "deployment": ["Docker", "Vercel (Frontend)", "Dedicated GPU Cloud VM / Local Edge Server (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI", "QGIS (Geospatial verification)"],
        "alternatives": [
            "Bounding Box Object Detection vs Semantic Segmentation: Object bounding boxes fail to capture irregular flood water contours; semantic segmentation provides precise pixel-level mask boundaries.",
            "Vanilla Dijkstra vs PostGIS pgRouting: pgRouting operates directly within the spatial database using R-Tree indices, handling large road topologies 10x faster than memory-bound Python scripts.",
            "Cloud Tile Servers vs Local Vector Tiles: Local vector tiles enable complete offline operations during disaster blackout conditions.",
        ],
        "rationale": (
            "The architecture balances high-throughput spatial image segmentation with rapid graph-based emergency routing. "
            "PostGIS provides enterprise spatial geometry operations, PyTorch delivers deep semantic segmentation, and "
            "React with Leaflet enables intuitive, offline-capable field map visualization."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. Geospatial Tile Pipeline: Rasterio slices large orthomosaics into GPU-friendly tiles with retained spatial coordinates.\n"
            "2. Vision Modeling Tier: DeepLabV3+ with atrous spatial pyramid pooling captures multi-scale damage features from collapsed roofs to wide water expanses.\n"
            "3. Routing & Persistence: PostgreSQL with PostGIS and pgRouting executes dynamic road network shortest-path queries with sub-second latency.\n"
            "4. Field Usability: Leaflet frontend provides zero-dependency offline map tile caching for field rescue teams."
        ),
        "limitations": [
            "Dense cloud cover or smoke over disaster zones limits optical RGB aerial visibility.",
            "Processing full city-scale gigapixel mosaics requires high GPU memory (>= 8GB VRAM).",
            "OpenStreetMap road data may not reflect freshly collapsed bridges without manual field annotations.",
        ],
    },
    "agriculture_crop": {
        "keywords": ["crop", "plant", "leaf", "disease", "irrigation", "soil", "agriculture", "farm", "fertilizer", "pest", "harvest"],
        "title": "IoT-Driven Smart Agriculture Crop Disease Diagnosis & Automated Irrigation System",
        "problem_statement": (
            "Smallholder farmers experience heavy harvest losses due to late diagnosis of foliar pests and fungal pathogens, "
            "alongside imprecise manual irrigation that exhausts local water tables and elevates fertilizer runoff. Absence of "
            "affordable, real-time localized soil-microclimate telemetry and automated crop image symptom classification leads to "
            "overuse of chemical agrochemicals and significant yield decline."
        ),
        "skills": [
            "Embedded C++ / MicroPython (ESP32)",
            "Soil Moisture & DHT22 Sensor Calibration",
            "Computer Vision & Deep Learning (ViT / ResNet-50)",
            "MQTT Telemetry Ingestion (paho-mqtt)",
            "FastAPI Backend API",
            "React Progressive Web App (PWA)",
            "PostgreSQL / TimescaleDB",
        ],
        "resources": [
            "PlantVillage benchmark crop leaf disease image dataset",
            "ESP32 microcontroller with capacitive soil moisture and ambient temperature/humidity sensors",
            "5V Relay module controlling simulated irrigation solenoid valve",
            "Open-Meteo local weather forecast API",
        ],
        "challenges": [
            "Complex natural outdoor lighting conditions, shadows, and soil background clutter in phone leaf captures",
            "Electrochemical degradation and calibration drift of soil moisture sensors over extended field deployment",
            "Intermittent cellular / LoRa network connectivity across remote agricultural plots",
            "Balancing computational complexity of Vision Transformers on mobile-friendly web interfaces",
        ],
        "recommendations": [
            "Utilize transfer learning on MobileNetV3 or lightweight Vision Transformers to maintain sub-200ms mobile diagnosis.",
            "Implement capacitive rather than resistive soil moisture probes to prevent electrolytic corrosion in damp soil.",
            "Integrate Penman-Monteith evapotranspiration calculations with 7-day weather forecasts to prevent over-irrigation before rain.",
            "Build offline caching into the React PWA allowing farmers to capture leaf photos offline for synchronized upload.",
        ],
        "assumptions": [
            "Farmers have access to basic Android smartphones with camera resolution >= 5 Megapixels.",
            "Agricultural field has localized Wi-Fi, LoRa, or cellular coverage at the sensor gateway node.",
            "Irrigation water supply is plumbed with controllable electric solenoid or pump switches.",
        ],
        "target_users": [
            "Smallholder farmers and commercial greenhouse agriculturalists",
            "Agricultural extension advisory officers and agronomists",
            "Horticultural researchers and farm cooperative managers",
            "Irrigation equipment technicians",
        ],
        "functional_requirements": [
            "Crop leaf image upload and automated multi-class disease diagnosis using fine-tuned Vision Transformer (ViT) or ResNet-50",
            "Disease severity estimation calculating lesion surface area percentage to recommend precise organic/chemical treatment dosages",
            "Real-time IoT soil moisture, ambient temperature, and humidity telemetry ingestion via LoRaWAN / ESP32",
            "Evapotranspiration-based automated smart irrigation scheduling algorithm activating simulated solenoid water valves",
            "Farmer advisory mobile-responsive web dashboard presenting crop health status, 7-day weather forecast, and localized treatment guides",
            "Historical crop yield and disease outbreak hotspot trend analytics for regional agricultural extension officers",
        ],
        "non_functional_requirements": [
            "Leaf disease image classification inference latency < 350ms per capture",
            "Soil telemetry sensor polling interval configurable from 10 seconds to 15 minutes",
            "Disease classification accuracy >= 94% Top-1 accuracy across 15 standard crop disease classes",
            "Low-power edge operation: ESP32 deep sleep consumption < 15uA enabling 6+ month battery lifespan",
        ],
        "mvp_features": [
            "Mobile-friendly leaf camera upload module identifying at least 3 common crop diseases with confidence ratings",
            "Working ESP32 soil moisture sensor broadcasting live moisture percentages via MQTT",
            "Automated irrigation trigger rule activating relay switch when soil moisture drops below 30%",
            "Farmer advisory screen displaying recommended organic/chemical remedies and local weather alerts",
        ],
        "out_of_scope": [
            "Physical autonomous robotic tractor harvesting or aerial pesticide spraying drone hardware",
            "Commercial fertilizer supply chain marketplace and credit lending payment gateways",
            "Genetic sequence modification or lab-grade biological pathogen culturing",
        ],
        "deliverables": [
            "Complete source code repository for deep learning crop disease model and IoT sensor firmware",
            "Farmer advisory React PWA dashboard with live MQTT telemetry and automated irrigation controls",
            "Empirical evaluation report documenting disease classification accuracy, water savings, and sensor accuracy",
            "CapStone project thesis document, system schematic diagrams, and live demonstration video",
        ],
        "success_criteria": [
            "Achieve >= 92% classification accuracy on PlantVillage test dataset",
            "Demonstrate >= 25% reduction in simulated irrigation water consumption compared to static timer irrigation",
            "Verify sensor telemetry transmission with < 1% packet loss over 48 hours continuous testing",
            "Flawless live execution during final academic capstone viva defense",
        ],
        "frontend": ["React.js (PWA)", "TailwindCSS", "Recharts (Soil & Weather Graphs)", "Lucide Icons", "Service Worker"],
        "backend": ["FastAPI (Python 3.12)", "Eclipse Mosquitto (MQTT)", "asyncio", "Pydantic v2"],
        "database": ["PostgreSQL with TimescaleDB extension", "SQLite (Local Cache)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["PyTorch", "Torchvision (MobileNetV3 / ViT)", "OpenCV (Leaf Masking)", "NumPy & Pandas"],
        "deployment": ["Docker", "Vercel (Frontend)", "Railway / Cloud VM (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI", "PlatformIO (ESP32)"],
        "alternatives": [
            "ResNet-101 vs MobileNetV3: ResNet-101 provides marginally higher accuracy (+1.2%) but is 6x larger and too slow for mobile inference; MobileNetV3 chosen for sub-100ms mobile inference.",
            "Timer-based Irrigation vs Telemetry Evapotranspiration: Fixed timers waste water during rainfall; sensor-driven evapotranspiration models reduce agricultural water consumption by over 30%.",
            "HTTP REST Telemetry vs MQTT: MQTT reduces cellular data consumption by over 70% compared to periodic HTTP POST payloads.",
        ],
        "rationale": (
            "The architecture merges ultra-low-power edge telemetry with accessible computer vision diagnosis. "
            "MQTT ensures resilient, battery-conserving sensor reporting, while MobileNetV3 and FastAPI provide "
            "instant agricultural guidance directly to the farmer's mobile browser."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. Edge Telemetry: ESP32 with deep-sleep cycling and MQTT enables multi-month standalone operation in remote plots.\n"
            "2. Agronomic Irrigation Engine: Evapotranspiration heuristics blend soil moisture with ambient humidity to trigger water relays only when biologically necessary.\n"
            "3. Computer Vision: MobileNetV3 with pre-trained ImageNet weights enables rapid leaf disease diagnosis on resource-constrained compute.\n"
            "4. Mobile Delivery: React PWA with service workers allows farmers to record field observations even during transient network dropouts."
        ),
        "limitations": [
            "Symptoms of nutritional deficiencies (e.g. nitrogen/potassium lack) may visually mimic fungal foliar lesions.",
            "Soil moisture readings vary by soil texture (clay vs sandy loam) and require initial calibration offsets.",
            "Cellular reception dropouts in remote agricultural valleys require local gateway buffering.",
        ],
    },
    "finance_fraud": {
        "keywords": ["fraud", "credit card", "transaction", "banking", "payment", "money laundering", "financial anomaly", "fintech"],
        "title": "Real-Time Financial Transaction Fraud Detection & Explainable Risk Scoring Engine",
        "problem_statement": (
            "Digital payment platforms and banking institutions face increasingly sophisticated card-not-present fraud, "
            "account takeover schemes, and synthetic identity anomalies that easily circumvent legacy static rule-based engines. "
            "Financial institutions require real-time, low-latency transaction risk scoring and anomaly detection models that maximize "
            "fraudulent pattern capture while maintaining minimal false-positive friction for legitimate cardholders."
        ),
        "skills": [
            "Machine Learning (XGBoost / LightGBM / Isolation Forest)",
            "Imbalanced Data Handling (SMOTE / Cost-Sensitive Learning)",
            "Model Explainability (SHAP / LIME)",
            "FastAPI & In-Memory Redis Caching",
            "PostgreSQL ACID Transaction Design",
            "React.js Financial Analytics Console",
        ],
        "resources": [
            "IEEE-CIS Fraud Detection benchmark dataset or Credit Card Fraud Detection dataset (Kaggle)",
            "Redis in-memory instance for sub-10ms cardholder spending velocity feature lookups",
            "Standard development workstation with Python 3.12 scientific compute libraries",
        ],
        "challenges": [
            "Extreme class imbalance where legitimate transactions outnumber fraudulent events by 1000 to 1",
            "Strict sub-50ms latency budget per transaction during live payment authorization gateways",
            "Concept drift as fraud syndicates continuously alter evasion patterns and transaction sizes",
            "Mandatory regulatory explainability requiring explicit justification for declined transactions",
        ],
        "recommendations": [
            "Employ cost-sensitive XGBoost and LightGBM models optimizing Area Under the Precision-Recall Curve (PR-AUC) rather than raw accuracy.",
            "Maintain rolling cardholder transaction velocity counters (10-minute, 1-hour, 24-hour windows) in Redis for real-time feature lookups.",
            "Integrate TreeSHAP to compute real-time feature attribution values explaining why high-risk transactions were flagged.",
            "Implement a dual-threshold decisioning pipeline: approve low-risk, step-up multi-factor authentication (MFA) for medium-risk, and block high-risk.",
        ],
        "assumptions": [
            "Incoming transactions conform to standardized ISO 8583 / JSON payment schemas.",
            "Cardholder historic baseline profiles are updated through daily batch aggregation jobs.",
            "Payment gateway allows a maximum 100ms round-trip latency window for risk scoring.",
        ],
        "target_users": [
            "Bank fraud risk analysts and financial crimes compliance investigators",
            "Payment gateway merchant operations managers",
            "Financial security audit officers reviewing fraud dispute chargebacks",
            "Cardholders receiving real-time verification SMS/push notifications",
        ],
        "functional_requirements": [
            "Real-time payment transaction streaming ingestion and immediate feature engineering (velocity, geographical distance, merchant risk)",
            "Dual-stage anomaly detection model combining Isolation Forests for novel fraud with XGBoost/LightGBM for supervised fraud classification",
            "Low-latency (<50ms) transaction decisioning engine outputting risk scores and automated actions (Approve, Step-up 2FA, Decline)",
            "SHAP/LIME explainability module detailing the exact transaction features contributing to high risk scores for compliance audits",
            "Fraud analyst investigation console displaying live flagged transaction feeds, geographical risk maps, and customer spending graphs",
            "Continuous model drift monitoring logging distribution shifts in transaction amounts and fraudulent behavior patterns",
        ],
        "non_functional_requirements": [
            "Transaction risk scoring inference latency < 45ms at 99th percentile (P99)",
            "Throughput capability >= 1,000 transactions/second under peak load simulation",
            "Model PR-AUC >= 0.88 on held-out imbalanced test dataset",
            "Complete audit trail: every transaction decision logged with model version and SHAP attribution vectors",
        ],
        "mvp_features": [
            "Synthetic transaction stream generator simulating normal and fraudulent card purchases",
            "Trained XGBoost fraud model evaluating transactions and outputting calibrated 0-100 risk scores",
            "Real-time fraud analyst dashboard highlighting flagged transactions with instant SHAP feature explanations",
            "Interactive decision threshold simulator demonstrating false-positive vs false-negative trade-offs",
        ],
        "out_of_scope": [
            "Live production SWIFT / VISA network interbank settlement gateway processing",
            "Physical debit/credit card plastic manufacturing and EMV chip firmware",
            "Consumer debt collection and court-admissible legal criminal prosecution management",
        ],
        "deliverables": [
            "Complete fraud detection and real-time risk scoring engine source code",
            "Fraud analyst React web console with live transaction streaming and SHAP explainability charts",
            "Comprehensive empirical evaluation report analyzing ROC-AUC, PR-AUC, and latency benchmarks",
            "Capstone project thesis report, architectural design documents, and viva presentation slides",
        ],
        "success_criteria": [
            "Achieve >= 85% Recall on fraudulent transactions with False Positive Rate < 1.0%",
            "Verify P99 inference latency under 50ms across 10,000 benchmark transaction payloads",
            "100% compliance in generating valid SHAP explainability summaries for every blocked transaction",
            "Successful live simulation during academic project viva evaluation",
        ],
        "frontend": ["React.js", "Recharts (Velocity & Risk Graphs)", "TailwindCSS", "Lucide Icons", "Radix UI Tables"],
        "backend": ["FastAPI (Python 3.12)", "Redis (In-Memory Feature Store)", "asyncio", "Pydantic v2"],
        "database": ["PostgreSQL (ACID Transaction Records)", "Redis (Rolling Velocity)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["XGBoost", "LightGBM", "Scikit-Learn", "SHAP (Model Explainability)", "Pandas & NumPy"],
        "deployment": ["Docker & Docker Compose", "Vercel (Frontend)", "Railway / AWS ECS (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Locust (Load & Latency Testing)", "Postman / Swagger OpenAPI"],
        "alternatives": [
            "Static Rules vs Machine Learning: Static IF-THEN rules fail to detect evolving multi-card fraud rings and create high customer friction; gradient boosted trees dynamically capture complex non-linear combinations.",
            "Deep Neural Networks vs XGBoost: Deep neural nets require extensive tuning and higher inference latency (>100ms); XGBoost achieves superior PR-AUC on tabular data in under 20ms.",
            "Black-box ML vs SHAP Explainability: Black-box models violate banking financial regulations; SHAP calculates exact marginal feature contributions ensuring regulatory compliance.",
        ],
        "rationale": (
            "The architecture prioritizes sub-50ms execution speed, high precision-recall balance on extreme class imbalances, "
            "and transparent explainability. Redis supplies instantaneous velocity metrics, XGBoost scores transactions with "
            "microsecond latency, and SHAP ensures every automated decision is auditable."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. Feature Store Tier: Redis in-memory cache maintains rolling velocity counters (e.g. number of transactions in last 5 minutes) without hitting disk storage.\n"
            "2. Inference Tier: XGBoost compiled model executes tabular classification in sub-15ms, easily fitting within payment authorization latency budgets.\n"
            "3. Explainability Tier: TreeSHAP generates local feature attributions explaining which variables (e.g. abnormal transaction amount + foreign IP) triggered the risk flag.\n"
            "4. Analyst Console: React frontend connects via WebSockets to stream incoming high-risk transactions directly to compliance reviewers."
        ),
        "limitations": [
            "Model requires periodic retraining to adapt to newly emerging fraudulent merchant categories and tactics.",
            "Initial transactions from brand-new cardholders lack historical velocity baselines (cold-start condition).",
            "Very high concurrent transaction spikes require horizontal scaling of the FastAPI worker pool.",
        ],
    },
    "cybersecurity_ids": {
        "keywords": ["cybersecurity", "intrusion", "malware", "network traffic", "pcap", "packet", "firewall", "ddos", "phish", "snort", "botnet"],
        "title": "AI-Powered Network Intrusion Detection & Automated Threat Mitigation System",
        "problem_statement": (
            "Enterprise networks encounter high volumes of automated cyber attacks, port scans, and zero-day malware intrusions that "
            "easily bypass static signature-based firewall rules and overwhelm human security operations center (SOC) analysts with "
            "thousands of unprioritized alerts every day. Organizations need an intelligent network intrusion detection system capable of "
            "analyzing packet flow telemetry in real time and automatically blocking malicious IP subnets."
        ),
        "skills": [
            "Network Packet Analysis (Scapy / Zeek / Wireshark)",
            "Machine Learning / Deep Learning (PyTorch / Scikit-Learn)",
            "Statistical Network Flow Feature Engineering",
            "FastAPI & Asynchronous WebSockets",
            "React.js Security Operations Center (SOC) Console",
            "Linux iptables / Firewall Automation Scripting",
        ],
        "resources": [
            "CIC-IDS2017 / UNSW-NB15 benchmark network intrusion datasets",
            "Live PCAP sample packet capture archives",
            "Development workstation capable of parallel packet parsing and ML inference",
        ],
        "challenges": [
            "High packet arrival rates during gigabit network spikes causing buffer packet drops",
            "High cost of false positives where blocking benign legitimate traffic disrupts business operations",
            "Adversarial traffic mutation techniques designed to obfuscate packet payloads and bypass ML classifiers",
            "Extracting bidirectional flow statistics in real time before connections terminate",
        ],
        "recommendations": [
            "Process traffic at the flow level rather than inspecting individual packets to dramatically reduce computational overhead.",
            "Train an ensemble Random Forest / 1D-CNN model on normalized statistical flow features (packet size distribution, inter-arrival times).",
            "Implement confidence thresholding requiring model certainty > 95% before triggering automated firewall IP block rules.",
            "Provide SOC analysts with an interactive timeline and packet payload inspection drawer for forensic verification.",
        ],
        "assumptions": [
            "Network tap or port mirror provides mirror copies of ingress/egress network flows.",
            "Target environment permits simulated automated Linux iptables rule manipulation.",
            "Benchmark datasets reflect representative modern enterprise cyber attack vectors.",
        ],
        "target_users": [
            "Security Operations Center (SOC) tier-1 and tier-2 analysts",
            "Network security administrators and firewall engineers",
            "Information security officers and threat hunting researchers",
            "IT compliance auditors verifying network security monitoring standards",
        ],
        "functional_requirements": [
            "Live network packet capture (PCAP) and NetFlow / IPFIX telemetry ingestion and protocol header parsing",
            "Statistical flow feature extraction (packet inter-arrival times, byte ratios, TCP flag distributions)",
            "Machine learning intrusion detection engine classifying traffic into benign, DoS/DDoS, brute-force, and port-scan attack categories",
            "Automated threat response dispatcher triggering simulated firewall iptables blocking rules for malicious IP subnets",
            "SOC analyst security dashboard rendering real-time network traffic graphs, attack origin world maps, and alert timelines",
            "Security incident forensic report generation detailing attack timelines, targeted ports, and MITRE ATT&CK framework alignments",
        ],
        "non_functional_requirements": [
            "Flow feature extraction and threat classification latency < 100ms per network flow",
            "Intrusion classification detection rate (Recall) >= 95% across major attack categories",
            "False positive rate strictly below 0.8% to avoid blocking legitimate user sessions",
            "Capable of ingesting and analyzing up to 5,000 network flows per second on standard hardware",
        ],
        "mvp_features": [
            "PCAP replay engine simulating live network traffic and attacks from benchmark dataset files",
            "Trained machine learning flow classifier detecting PortScan and DoS attacks in real time",
            "Live SOC alert console displaying attack category, source IP, targeted port, and confidence rating",
            "Automated simulated iptables rule generator displaying the generated firewall command to neutralize threats",
        ],
        "out_of_scope": [
            "Kernel-level eBPF / DPDK proprietary hardware network card driver development",
            "Deep packet inspection of end-to-end encrypted TLS 1.3 payloads requiring private key decryption",
            "Physical data center perimeter hardware barrier security",
        ],
        "deliverables": [
            "Complete network flow extraction and AI intrusion detection engine source code",
            "Full-stack SOC security analyst dashboard with real-time attack alerts and flow visualizers",
            "Empirical evaluation report documenting confusion matrices, detection latency, and false positive metrics",
            "Academic capstone thesis report, architecture specifications, and oral defense slides",
        ],
        "success_criteria": [
            "Achieve >= 96% overall accuracy on UNSW-NB15 / CIC-IDS benchmark test set",
            "Demonstrate automated threat detection and rule generation within 500ms of attack packet injection",
            "Maintain zero system crashes or memory leaks during 60-minute continuous traffic replay test",
            "Flawless live demonstration during final faculty project evaluation",
        ],
        "frontend": ["React.js", "TailwindCSS", "Recharts (Traffic & Attack Graphs)", "Lucide Icons", "Radix UI Modal"],
        "backend": ["FastAPI (Python 3.12)", "asyncio & WebSockets", "Pydantic v2", "Uvicorn ASGI"],
        "database": ["PostgreSQL (Security Incident Logs)", "TimescaleDB (Flow Metrics)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["Scikit-Learn (Random Forest & XGBoost)", "PyTorch (1D-CNN)", "Scapy", "Pandas & NumPy"],
        "deployment": ["Docker", "Vercel (Frontend)", "Local Linux VM / Cloud Instance (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Tcpreplay (PCAP Replay)", "Postman / Swagger OpenAPI"],
        "alternatives": [
            "Deep Packet Payload Inspection (DPI) vs Flow Statistics: DPI fails on modern encrypted HTTPS/TLS traffic and requires high compute; flow-level statistical modeling accurately detects attacks based on temporal flow behavior without inspecting encrypted payloads.",
            "Rule-based Snort vs Machine Learning IDS: Snort only catches known signature strings; machine learning generalizes to detect novel attack variants and zero-day anomaly distributions.",
            "Batch Log Analysis vs Real-Time Stream Processing: Batch analysis delays detection by minutes or hours; real-time streaming detects and neutralizes active network intrusions within milliseconds.",
        ],
        "rationale": (
            "The architecture focuses on high-speed flow statistical feature extraction, resilient machine learning anomaly detection, "
            "and instant visual alerting. Flow-level modeling handles high bandwidth without stalling, while FastAPI and WebSockets "
            "deliver immediate threat telemetry to security analysts."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. Packet Capture Tier: Scapy / flow parser groups incoming packets into 5-tuple bidirectional flows and extracts statistical features.\n"
            "2. AI Inference Engine: Random Forest / XGBoost evaluates flow feature vectors in microseconds, achieving high precision across multi-class cyber attacks.\n"
            "3. Incident Logging & Persistence: TimescaleDB stores high-volume flow time-series metrics with automated data retention policies.\n"
            "4. Operational Security Console: React frontend connects via WebSockets to display instant alert banners and attack severity distributions."
        ),
        "limitations": [
            "Attacks that mimic normal human browsing cadence with low packet volume (low-and-slow attacks) are harder to detect.",
            "Hardware network interface cards without ring buffer optimization may drop packets under extreme multi-gigabit flooding.",
            "Model requires retraining when major new enterprise protocols or business software are deployed on the network.",
        ],
    },
}


def get_domain_profile(idea: str) -> tuple[str, dict[str, Any]]:
    text = idea.lower()
    for domain_id, profile in DOMAINS_CATALOG.items():
        if any(k in text for k in profile["keywords"]):
            return domain_id, profile

    # Dynamic synthesizer for novel or unlisted project ideas
    topic = _extract_topic(idea)
    return "custom", {
        "title": f"{topic}: Intelligent Real-Time Analysis & Decision Support System",
        "problem_statement": (
            f"Operational workflows in {idea.strip().lower()} frequently suffer from manual oversight, unpredictable error rates, "
            f"and delayed decision latency due to lack of real-time telemetry and automated intelligence. Conventional approaches "
            f"rely on static, fragmented procedures that lead to inefficiencies, resource wastage, and elevated operational risks."
        ),
        "skills": [
            "Python 3.12 & Modern Software Architecture",
            "FastAPI / Asynchronous REST Service Design",
            "Machine Learning / Computational Modeling",
            "Modern React.js & Responsive State Management",
            "SQL Database Schema Design & Pydantic Validation",
            "Automated Testing & Continuous Integration (CI)",
        ],
        "resources": [
            "Open-source domain benchmark datasets (Kaggle / UCI Machine Learning)",
            "Standard development workstation with CPU/GPU acceleration",
            "Version control repository via Git/GitHub with automated test pipelines",
            "Cloud compute or Google Colab for baseline experimental evaluation",
        ],
        "challenges": [
            "Noisy data inputs and class distribution imbalances in the target domain",
            "Maintaining low-latency real-time response times under concurrent user requests",
            "Rigorous verification and empirical ablation studies required for capstone viva defense",
            "Seamless data contract integration between the backend AI service and frontend interface",
        ],
        "recommendations": [
            "Establish an automated baseline model in Phase 2 before introducing advanced deep architectures.",
            "Construct modular service endpoints with strict Pydantic v2 contract validation.",
            "Incorporate real-time event notifications and interactive telemetry visualization.",
            "Document experimental metrics, failure modes, and architectural trade-offs continuously.",
        ],
        "assumptions": [
            "Required input data or simulated telemetry is accessible through standard protocols.",
            "Team members can dedicate 10-15 hours per week toward execution and testing.",
            "System operates within standard academic prototype evaluation specifications.",
        ],
        "target_users": [
            "Domain practitioners and operational field technicians",
            "Academic evaluators, project mentors, and research faculty",
            "System administrators monitoring live operational health and diagnostic logs",
        ],
        "functional_requirements": [
            f"Real-time input data acquisition, validation, and streaming pipeline for {topic}",
            f"Domain-specific computational / predictive algorithmic core utilizing optimized machine learning models for {topic}",
            "Continuous anomaly detection, rule compliance evaluation, and automated threshold-based event alerting",
            "Interactive operational control dashboard presenting live telemetry streams, performance analytics, and diagnostic logs",
            "Automated remediation workflow triggering actionable recommendations and closed-loop process adjustments",
            "Comprehensive audit logging, historical trend aggregation, and exportable academic performance evaluation reporting",
        ],
        "non_functional_requirements": [
            "End-to-end processing and decision response latency under 350ms for live transactions/telemetry",
            "High availability >= 99.5% with graceful offline caching and automatic reconnect",
            "System throughput capable of processing up to 500 concurrent events per second",
            "Strict data protection compliance with end-to-end encryption for stored records and transit payloads",
        ],
        "mvp_features": [
            f"Core predictive or analytical processing pipeline verified against representative benchmark test datasets for {topic}",
            "Interactive user interface demonstrating real-time data submission, live processing, and result rendering",
            "Automated threshold alert mechanism triggering visual notifications upon anomalous conditions",
            "Complete academic documentation including system architecture diagrams and empirical evaluation methodology",
        ],
        "out_of_scope": [
            "Enterprise multi-region distributed cloud clustering infrastructure",
            "Custom physical hardware silicon fabrication or proprietary chip design",
            "Commercial billing, subscription payment gateways, and advertising management",
        ],
        "deliverables": [
            "Fully tested and documented source code repository with reproducible environment setup",
            "Comprehensive Project Synopsis and System Architecture Specification",
            "Empirical Evaluation Report with confusion matrices, loss curves, or benchmark graphs",
            "Live presentation slides and functional prototype demonstration video",
        ],
        "success_criteria": [
            "Achievement of target evaluation metrics (e.g., F1-score >= 0.85 or system response < 500ms)",
            "Zero critical security or data validation vulnerabilities in core routes",
            "Successful end-to-end demonstration during final faculty viva / academic evaluation",
            "Delivery of all project artifacts within the allocated timeframe",
        ],
        "frontend": ["React.js", "Vite", "TailwindCSS / Modern CSS", "Lucide Icons", "Recharts"],
        "backend": ["FastAPI (Python 3.12)", "Uvicorn ASGI Server", "Pydantic v2", "asyncio"],
        "database": ["PostgreSQL / Supabase", "SQLite (Local development)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["Scikit-Learn", "NumPy & Pandas", "PyTorch 2.x"],
        "deployment": ["Docker", "Vercel / Netlify (Frontend)", "Render / Railway (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI", "Ruff / Black"],
        "alternatives": [
            "Flask / Django vs FastAPI: Flask lacks native async support and automatic OpenAPI documentation; FastAPI provides high-speed asynchronous execution and strict Pydantic validation.",
            "MongoDB vs PostgreSQL/SQLite: Document databases lack ACID foreign key constraints; relational schema ensures data integrity and structured reporting.",
            "TensorFlow vs PyTorch: TensorFlow graph abstractions are more verbose; PyTorch provides dynamic computation graphs and wider contemporary research paper support.",
        ],
        "rationale": (
            "The recommended stack balances developer velocity, academic rigor, and execution reliability. "
            "FastAPI provides native asynchronous endpoints with strict Pydantic contract validation, making it ideal "
            "for bridging AI model execution with frontend consumers. React with Vite delivers fast hot-reloading and modular "
            "component rendering. PyTorch and Scikit-Learn provide mature, reproducible scientific computing foundations."
        ),
        "reasoning": (
            "Architectural Reasoning Output:\n"
            "1. Presentation Tier: React + Vite minimizes bundling overhead and ensures an interactive, responsive UI.\n"
            "2. Service Tier: FastAPI in Python 3.12 avoids runtime overhead, offers automatic Swagger OpenAPI documentation, and integrates natively with scientific Python libraries.\n"
            "3. Persistence Tier: PostgreSQL (or local SQLite) provides strong consistency, referential integrity, and JSON column support.\n"
            "4. AI/ML Engine: Verified benchmark algorithms with broad academic precedent and robust error handling.\n"
            "5. Tooling: Pytest and Docker ensure cross-platform reproducibility across team member workstations."
        ),
        "limitations": [
            "Deep learning model training requires dedicated GPU compute (CUDA) or Google Colab runtime.",
            "Free-tier cloud deployments may experience cold start delays on idle backend instances.",
            "Local SQLite database is single-writer; transition to PostgreSQL required for concurrent multi-user load.",
        ],
    }


def _detect_domains(idea: str) -> set[str]:
    text = idea.lower()
    domains = set()
    if any(k in text for k in ["vision", "image", "video", "detect", "cnn", "camera", "photo", "face", "ocr", "yolo", "segregat"]):
        domains.add("computer_vision")
    if any(k in text for k in ["nlp", "text", "language", "sentiment", "summariz", "chat", "llm", "spam", "translat"]):
        domains.add("nlp")
    if any(k in text for k in ["fraud", "finance", "stock", "market", "money", "transaction", "payment", "bank"]):
        domains.add("finance")
    if any(k in text for k in ["health", "medic", "disease", "patient", "clinical", "drug", "doctor", "prescript"]):
        domains.add("healthcare")
    if any(k in text for k in ["iot", "sensor", "hardware", "arduino", "raspberry", "embedded", "drone", "uav", "waste", "bin", "trash", "telemetry"]):
        domains.add("iot")
    if any(k in text for k in ["web", "portal", "platform", "system", "app", "dashboard"]):
        domains.add("web")
    if not domains:
        domains.add("software_engineering")
    return domains


def fallback_feasibility(
    project_idea: str,
    duration_weeks: int,
    team_size: int | None,
    skills: list[str] | None = None,
) -> FeasibilityResult:
    cleaned = project_idea.strip()
    topic = _extract_topic(cleaned)
    domain_id, profile = get_domain_profile(cleaned)

    # Calculate feasibility based on duration, team size, and complexity
    if duration_weeks < 4:
        feasibility_rating = "Low"
        complexity_rating = "Advanced"
    elif duration_weeks >= 8 and team_size is not None and team_size >= 3:
        feasibility_rating = "High"
        complexity_rating = "Intermediate"
    else:
        feasibility_rating = "Medium"
        complexity_rating = "Intermediate"

    req_skills = list(profile["skills"])
    if skills:
        for s in skills:
            if s not in req_skills:
                req_skills.append(s)

    team_capacity = (
        f"a team of {team_size} students"
        if team_size is not None
        else "an unspecified student team whose capacity should be confirmed"
    )
    reasoning = (
        f"The proposed project '{profile['title']}' spans {duration_weeks} weeks with {team_capacity}. "
        f"Given the technical domain requirements ({domain_id}), a timeline of {duration_weeks} weeks provides sufficient "
        f"runway for data acquisition, core algorithmic implementation, backend API integration, and academic validation. "
        f"Tasks should be assigned according to the confirmed team capacity across data engineering, model development, "
        f"frontend dashboard design, and empirical viva documentation, making the project {feasibility_rating} feasibility "
        f"with {complexity_rating} complexity."
    )

    return FeasibilityResult(
        project_title=profile["title"],
        problem_statement=profile["problem_statement"],
        feasibility=feasibility_rating,
        economic_feasibility="Medium",
        economic_reasoning=(
            "Estimate costs for required data, compute, hosting, and any specialized equipment; "
            "prefer free academic tiers and open-source tools within the student project budget."
        ),
        operational_feasibility="Medium",
        operational_reasoning=(
            "Validate the proposed workflow with intended users and ensure the project can be "
            "operated and demonstrated with the available team, devices, and campus resources."
        ),
        complexity=complexity_rating,
        required_skills=req_skills[:8],
        required_resources=profile["resources"],
        potential_challenges=profile["challenges"],
        recommendations=profile["recommendations"],
        assumptions=profile["assumptions"],
        reasoning=reasoning,
    )


def fallback_scope(
    project_idea: str,
    feasibility: dict[str, Any],
    duration_weeks: int,
    team_size: int | None,
) -> ScopeResult:
    domain_id, profile = get_domain_profile(project_idea)
    title = feasibility.get("project_title") or profile["title"]

    return ScopeResult(
        project_title=title,
        project_objective=(
            f"Design, implement, and empirically validate an academic system for '{title}' "
            f"demonstrating real-time responsiveness, engineering rigor, and structured documentation."
        ),
        proposed_solution=(
            f"Build a scoped, testable system for '{title}' using the recommended technologies, "
            "then validate it with representative data and documented evaluation criteria."
        ),
        target_users=profile["target_users"],
        functional_requirements=profile["functional_requirements"],
        non_functional_requirements=profile["non_functional_requirements"],
        mvp_features=profile["mvp_features"],
        out_of_scope=profile["out_of_scope"],
        deliverables=profile["deliverables"],
        success_criteria=profile["success_criteria"],
    )


def fallback_technology(
    project_idea: str,
    feasibility: dict[str, Any],
    scope: dict[str, Any],
    skills: list[str] | None = None,
) -> TechnologyResult:
    domain_id, profile = get_domain_profile(project_idea)

    return TechnologyResult(
        frontend=profile["frontend"],
        backend=profile["backend"],
        database=profile["database"],
        ai_ml=profile["ai_ml"],
        deployment=profile["deployment"],
        development_tools=profile["development_tools"],
        alternatives=profile["alternatives"],
        rationale=profile["rationale"],
        limitations=profile["limitations"],
        reasoning=profile["reasoning"],
    )


def fallback_planning(
    project_idea: str,
    duration_weeks: int,
    team_size: int | None,
    scope: dict[str, Any],
    technology: dict[str, Any],
) -> PlanningResult:
    cleaned = project_idea.strip()
    words = [w for w in re.findall(r"[A-Za-z0-9]+", cleaned) if len(w) > 2]
    topic = " ".join(words[:4]).title() if words else "Academic Software Project"
    domains = _detect_domains(cleaned)

    # 1. Domain-specific contextual terminology
    if "computer_vision" in domains:
        domain_label = "Computer Vision & Image Processing"
        data_spec = "image datasets, bounding box/class annotations, and augmentation pipelines"
        model_spec = "deep convolutional / YOLO detection backbone with feature pyramid networks"
        eval_spec = "mAP (Mean Average Precision), precision-recall curves, and inference latency"
    elif "nlp" in domains:
        domain_label = "Natural Language Processing (NLP)"
        data_spec = "text corpora, tokenization vocabularies, and cleaned intent labels"
        model_spec = "transformer encoder / LLM fine-tuning with attention mechanisms"
        eval_spec = "BLEU/ROUGE scores, classification F1-score, and perplexity"
    elif "iot" in domains:
        domain_label = "IoT Telemetry & Embedded Systems"
        data_spec = "sensor telemetry logs, ADC voltage streams, and hardware payload schemas"
        model_spec = "edge filtering algorithms, threshold heuristics, and embedded anomaly classifiers"
        eval_spec = "sensor response latency, packet loss rate, and battery/power profiles"
    elif "finance" in domains:
        domain_label = "Financial Analytics & Risk Modeling"
        data_spec = "financial time-series matrices, OHLCV feeds, and technical indicators"
        model_spec = "LSTM recurrent networks / gradient boosted decision trees (XGBoost)"
        eval_spec = "Sharpe ratio, Mean Squared Error (MSE), and directional accuracy"
    elif "healthcare" in domains:
        domain_label = "Healthcare & Clinical Diagnosis"
        data_spec = "clinical record cohorts, patient diagnostic features, and sanitized biometric tables"
        model_spec = "interpretable ensemble models with SHAP feature importance analysis"
        eval_spec = "Sensitivity, Specificity, AUC-ROC curve, and clinical fairness metrics"
    else:
        domain_label = "Intelligent Software Engineering"
        data_spec = "entity-relational schemas, validation rules, and structured test payloads"
        model_spec = "core computational algorithms, automated decision heuristics, and business logic"
        eval_spec = "throughput transactions/sec, error rate, and unit test code coverage"

    # 2. Master progressive catalog of 12 distinct academic milestone stages
    master_stages = [
        {
            "phase": 1,
            "title": f"Problem Formulation, Literature Survey & {domain_label} Scoping",
            "objective": f"Formalize academic research scope, study contemporary literature, and catalog benchmarks for {topic}.",
            "tasks": [
                f"Conduct systematic literature review across IEEE, ACM, and arXiv publications relevant to {topic}",
                "Formulate formal problem statement, project scope boundaries, and core research hypotheses",
                "Set up Git repository, configure collaborative branching model, and initialize virtual environments",
            ],
            "deliverable": "Project Synopsis Document & Literature Survey Matrix",
        },
        {
            "phase": 1,
            "title": f"Data Acquisition, Schema Contract Design & Storage Architecture",
            "objective": f"Acquire primary data sources, establish validation schemas, and structure persistent storage for {topic}.",
            "tasks": [
                f"Source raw datasets or sample telemetry required for {data_spec}",
                "Design JSON/SQL schema contracts with strict Pydantic validation models and type hints",
                "Audit data provenance, verify licensing compliance, and organize raw dataset directory archives",
            ],
            "deliverable": "Data Acquisition Log & Validated Schema Contracts",
        },
        {
            "phase": 1,
            "title": "Exploratory Data Analysis (EDA) & Data Cleansing",
            "objective": "Profile statistical distributions, identify class imbalances, and clean corrupted records.",
            "tasks": [
                "Execute exploratory data analysis (EDA) profiling summary statistics, distributions, and outliers",
                "Implement cleaning scripts to handle missing values, duplicates, and malformed inputs",
                "Generate correlation heatmaps, class balance visualizations, and summary distribution charts",
            ],
            "deliverable": "Exploratory Data Analysis (EDA) Report & Data Cleansing Scripts",
        },
        {
            "phase": 1,
            "title": "Data Preprocessing & Feature Engineering Pipeline",
            "objective": f"Build automated transformation pipelines and feature extraction routines for {topic}.",
            "tasks": [
                f"Construct automated preprocessing pipeline to normalize and transform {data_spec}",
                "Engineer domain-specific features, numerical embeddings, and categorical encodings",
                "Implement reproducible stratified train, validation, and test dataset splits with fixed random seeds",
            ],
            "deliverable": "Automated Preprocessing Pipeline & Feature Manifest",
        },
        {
            "phase": 2,
            "title": "Baseline Model Implementation & Benchmark Establishment",
            "objective": "Build standard reference baselines and log comparative performance thresholds.",
            "tasks": [
                "Implement naive baseline algorithms and standard heuristic benchmarks for comparison",
                f"Log baseline performance metrics including {eval_spec}",
                "Analyze baseline confusion matrices and identify early failure patterns on edge-case samples",
            ],
            "deliverable": "Baseline Model Weights & Benchmark Evaluation Metrics Log",
        },
        {
            "phase": 2,
            "title": f"Core Algorithmic Design & {model_spec.split('/')[0].strip()} Development",
            "objective": f"Construct the primary computational architecture for {topic}.",
            "tasks": [
                f"Implement target {model_spec} incorporating architectural constraints",
                "Configure custom loss functions, learning rate schedulers, and optimization routines",
                "Execute preliminary training/evaluation passes and verify numerical gradient stability",
            ],
            "deliverable": "Core Model Implementation Artifacts & Training Convergence Plots",
        },
        {
            "phase": 2,
            "title": "Hyperparameter Optimization & Comparative Ablation Study",
            "objective": "Systematically optimize model parameters and quantify component contributions.",
            "tasks": [
                "Conduct systematic hyperparameter tuning (learning rate, regularization, layer depth/width)",
                "Execute ablation study experiments isolating the performance impact of each sub-module",
                f"Generate comparative evaluation tables demonstrating improvement over the baseline (target: {eval_spec})",
            ],
            "deliverable": "Optimized Model Checkpoints & Comprehensive Ablation Study Report",
        },
        {
            "phase": 3,
            "title": "Backend Service Layer & Asynchronous REST API Construction",
            "objective": f"Encapsulate the core engine into production-ready FastAPI endpoints for {topic}.",
            "tasks": [
                "Implement FastAPI REST routes for model inference, status telemetry, and data ingestion",
                "Incorporate Pydantic request/response serializers, rate-limiting, and error handlers",
                "Write backend unit tests verifying endpoint response times under 500ms for standard payloads",
            ],
            "deliverable": "Functional FastAPI Backend with Swagger OpenAPI Documentation",
        },
        {
            "phase": 3,
            "title": "Interactive Frontend Dashboard & Telemetry Visualization",
            "objective": "Develop an accessible, responsive user interface with interactive data visualization.",
            "tasks": [
                "Construct modular React dashboard components, parameter input forms, and status cards",
                "Implement interactive visualization charts for real-time outputs, metrics, and progress logs",
                "Design client-side state management, async fetch handlers, and accessible loading skeletons",
            ],
            "deliverable": "Responsive Frontend Web Application & Component Library",
        },
        {
            "phase": 3,
            "title": "Full-Stack System Integration & End-to-End Pipeline Wiring",
            "objective": "Connect frontend client components directly to backend APIs and verify data flow.",
            "tasks": [
                "Wire frontend components with backend service endpoints including authentication headers",
                "Conduct end-to-end user journey tests from initial input submission to results rendering",
                "Implement graceful error boundaries, offline notices, and input validation alert banners",
            ],
            "deliverable": "Integrated Full-Stack Working Prototype",
        },
        {
            "phase": 4,
            "title": "System Hardening, Stress Testing & Edge-Case Security Audit",
            "objective": "Profile latency under concurrent load, verify test coverage, and harden against invalid inputs.",
            "tasks": [
                "Run automated pytest regression test suite ensuring test coverage >= 80% on critical modules",
                "Execute latency profiling, memory consumption audits, and multi-request stress simulations",
                "Audit input sanitation routines and verify graceful degradation under adversarial or corrupt inputs",
            ],
            "deliverable": "System Verification Report & Automated Test Suite (80%+ Coverage)",
        },
        {
            "phase": 4,
            "title": "Academic Thesis Documentation, Slide Deck & Final Viva Defense Preparation",
            "objective": f"Complete the formal academic report, prepare presentation slides, and rehearse the final viva for {topic}.",
            "tasks": [
                "Draft comprehensive academic project thesis following institutional guidelines and formatting",
                "Design professional viva presentation slide deck with system architecture and results charts",
                "Record a high-definition backup demonstration video and conduct mock oral defense rehearsal",
            ],
            "deliverable": "Final Academic Project Thesis, Presentation Deck & Recorded Demo Video",
        },
    ]

    total_stages = len(master_stages)
    w_count = max(1, duration_weeks)

    weekly_milestones: list[WeeklyMilestone] = []
    seen_tasks = set()

    for w in range(1, w_count + 1):
        if w_count == 1:
            idx = 0
        else:
            idx = int(round((w - 1) * (total_stages - 1) / (w_count - 1)))
        idx = max(0, min(idx, total_stages - 1))
        stage = master_stages[idx]

        m_title = f"Week {w}: {stage['title']}"
        m_obj = [stage["objective"]]

        raw_tasks = stage["tasks"]
        unique_tasks = []
        for t in raw_tasks:
            task_str = t
            if task_str in seen_tasks:
                task_str = f"{t} (Phase {w})"
            seen_tasks.add(task_str)
            unique_tasks.append(task_str)

        m_deliv = [f"Week {w} Deliverable: {stage['deliverable']}"]

        weekly_milestones.append(
            WeeklyMilestone(
                week_number=w,
                milestone_title=m_title,
                objectives=m_obj,
                tasks=unique_tasks,
                deliverables=m_deliv,
            )
        )

    phase_templates = [
        (
            "Phase 1: Research, Data Architecture & Feature Engineering",
            [
                f"Conduct systematic literature review and define research boundaries for {topic}",
                f"Acquire, inspect, and preprocess primary {data_spec}",
                "Initialize repository structure, branch rules, and CI configuration",
            ],
            [
                "Project Synopsis & Literature Review Matrix",
                "Exploratory Data Analysis (EDA) Report & Data Dictionary",
                "Automated Preprocessing & Feature Engineering Pipeline",
            ],
        ),
        (
            "Phase 2: Algorithmic Modeling, Training & Optimization",
            [
                "Implement reference baseline models and log comparative benchmark metrics",
                f"Develop target {model_spec} with custom training routines",
                f"Conduct hyperparameter tuning and ablation studies (evaluating {eval_spec})",
            ],
            [
                "Baseline and Optimized Model Weights",
                "Comprehensive Ablation Study & Convergence Curves",
                "Algorithmic Methodology Chapter Draft",
            ],
        ),
        (
            "Phase 3: Backend API, User Interface & System Integration",
            [
                "Build asynchronous FastAPI endpoints with Pydantic request/response validation",
                "Construct interactive React dashboard views and telemetry visualization charts",
                "Connect frontend client state with backend APIs and handle error boundaries",
            ],
            [
                "Functional FastAPI Backend with Swagger OpenAPI Documentation",
                "Interactive React User Interface",
                "Integrated End-to-End System Prototype",
            ],
        ),
        (
            "Phase 4: System Verification, Academic Thesis & Viva Defense",
            [
                "Execute automated test suites ensuring >= 80% coverage on critical modules",
                "Draft comprehensive academic project thesis following university guidelines",
                "Create viva presentation slides and rehearse live system demonstration",
            ],
            [
                "Complete Academic Project Thesis Document",
                "Automated Test Execution Summary (Code Coverage >= 80%)",
                "Academic Viva Slide Deck & Demonstration Recording",
            ],
        ),
    ]
    phase_count = min(len(phase_templates), w_count)
    base_phase_weeks, extra_phase_weeks = divmod(w_count, phase_count)
    phase_lengths = [
        base_phase_weeks + (index < extra_phase_weeks)
        for index in range(phase_count)
    ]
    phases = []
    start_week = 1
    for index, (phase_name, tasks, deliverables) in enumerate(phase_templates[:phase_count]):
        duration = phase_lengths[index]
        phases.append(PlannedPhase(
            phase_name=phase_name,
            start_week=start_week,
            duration_weeks=duration,
            tasks=tasks,
            deliverables=deliverables,
            dependencies=[phase_templates[index - 1][0]] if index else [],
        ))
        start_week += duration

    return PlanningResult(
        total_duration_weeks=duration_weeks,
        phases=phases,
        weekly_milestones=weekly_milestones,
    )



def fallback_risks(
    project_idea: str,
    feasibility: dict[str, Any],
    scope: dict[str, Any],
    technology: dict[str, Any],
    planning: dict[str, Any],
) -> RiskResult:
    domain_id, profile = get_domain_profile(project_idea)

    if domain_id == "smart_waste":
        risks = [
            ProjectRisk(
                risk="Ultrasonic Sensor Noise: Irregular waste accumulation shapes inside bins causing erratic distance readings.",
                likelihood="High",
                impact="Medium",
                mitigation="Implement rolling median and kalman filtering across consecutive readings to smooth physical debris anomalies.",
                contingency_plan="Incorporate a secondary load-cell weight sensor to cross-verify bin fill percentage before dispatching alerts.",
            ),
            ProjectRisk(
                risk="Outdoor Edge Telemetry Dropout: Intermittent cellular or Wi-Fi signal in dense urban collection alleys.",
                likelihood="Medium",
                impact="High",
                mitigation="Buffer telemetry records locally in SQLite or Flash memory on the edge microcontroller and transmit upon reconnect.",
                contingency_plan="Configure MQTT Quality of Service (QoS 1) with persistent broker queues to ensure zero telemetry packet loss.",
            ),
            ProjectRisk(
                risk="Visual Classification Degradation: Dirty, crumpled, or overlapping recyclable objects reducing YOLOv8 accuracy.",
                likelihood="Medium",
                impact="High",
                mitigation="Apply heavy data augmentation (rotation, color jitter, motion blur, cutmix) during training on real-world trash sets.",
                contingency_plan="Flag low-confidence classifications for secondary sorting and trigger confidence alerts on the operator dashboard.",
            ),
            ProjectRisk(
                risk="Vehicle Routing Solver Latency: Dynamic traveling salesperson (VRP) computational scaling under live road closures.",
                likelihood="Low",
                impact="Medium",
                mitigation="Partition municipal wards into independent geographic clusters before running Google OR-Tools route optimization.",
                contingency_plan="Fall back to greedy nearest-neighbor heuristic routing if graph solver exceeds 3-second compute timeout.",
            ),
        ]
    elif domain_id == "face_attendance":
        risks = [
            ProjectRisk(
                risk="Classroom Lighting & Pose Variation: Dim ambient illumination and oblique seating angles degrading face detection.",
                likelihood="Medium",
                impact="High",
                mitigation="Deploy multi-scale RetinaFace with adaptive histogram equalization (CLAHE) preprocessing on incoming video frames.",
                contingency_plan="Prompt instructor to activate auxiliary room lighting or trigger manual student verification for flagged seats.",
            ),
            ProjectRisk(
                risk="Presentation Attack Vulnerability: Proxy attendance attempted using printed portraits or smartphone screen replays.",
                likelihood="Medium",
                impact="High",
                mitigation="Incorporate passive micro-texture frequency analysis and eye-blink tracking into the live camera stream.",
                contingency_plan="Log suspected presentation attempts with frame snapshots and alert the instructor console for manual sign-off.",
            ),
            ProjectRisk(
                risk="Simultaneous Check-In Bottleneck: Video stream frame rate drops during mass classroom arrival peaks.",
                likelihood="Medium",
                impact="Medium",
                mitigation="Batch facial embedding extractions on GPU and utilize Faiss HNSW vector indexing for sub-50ms matching.",
                contingency_plan="Drop non-key video frames and process face recognition at 10 FPS instead of 30 FPS during peak classroom bursts.",
            ),
            ProjectRisk(
                risk="Student Biometric Data Privacy Concerns: Compliance risks under student data protection regulations.",
                likelihood="Low",
                impact="High",
                mitigation="Store only irreversible 512-dimensional vector embeddings; encrypt raw enrollment portraits with AES-256 at rest.",
                contingency_plan="Provide faculty with student biometric opt-out workflow and standard PIN/manual check-in capability.",
            ),
        ]
    elif domain_id == "healthcare_prescription":
        risks = [
            ProjectRisk(
                risk="Cursive Handwriting Ambiguity: Severely degraded prescription handwriting causing character recognition hallucinations.",
                likelihood="High",
                impact="High",
                mitigation="Fine-tune TrOCR on real-world handwritten prescription corpora and apply language model beam search decoding.",
                contingency_plan="Mandate licensed pharmacist interactive verification with side-by-side original image comparison for every field.",
            ),
            ProjectRisk(
                risk="Look-Alike Sound-Alike (LASA) Drug Confusion: Similar phonetic medication names mapped to incorrect pharmacological entities.",
                likelihood="Medium",
                impact="High",
                mitigation="Implement Levenshtein distance combined with clinical dosage context matching against the official RxNorm database.",
                contingency_plan="Highlight ambiguous drug candidate pairs with explicit warning banners on the pharmacist review dashboard.",
            ),
            ProjectRisk(
                risk="Drug Interaction Omission: Rare or newly published adverse drug combinations absent from local screening rules.",
                likelihood="Low",
                impact="High",
                mitigation="Synchronize local PostgreSQL contraindication tables periodically with authoritative OpenFDA and RxNorm registries.",
                contingency_plan="Display explicit clinical disclaimer stating tool is an assistive screening aid and provide direct links to drug monographs.",
            ),
            ProjectRisk(
                risk="Protected Health Information (PHI) Exposure: Scanned patient names and clinic identifiers exposed in transit.",
                likelihood="Low",
                impact="High",
                mitigation="Enforce client-side bounding box redaction of patient identification headers before sending image data to backend OCR.",
                contingency_plan="Execute automated memory scrubbers on API workers to prevent persisting raw unencrypted document buffers.",
            ),
        ]
    elif domain_id == "disaster_assessment":
        risks = [
            ProjectRisk(
                risk="Severe Weather Obstruction: Heavy cloud cover, smoke, or rain compromising optical RGB aerial drone survey visibility.",
                likelihood="Medium",
                impact="High",
                mitigation="Integrate multispectral / thermal aerial bands and pre-process imagery with de-hazing and contrast stretching.",
                contingency_plan="Utilize secondary ground-level reconnaissance reports to fill in blind spots on the emergency operations map.",
            ),
            ProjectRisk(
                risk="Gigapixel Memory Exhaustion: Gigabyte-sized orthomosaic drone maps exhausting GPU VRAM during segmentation passes.",
                likelihood="High",
                impact="Medium",
                mitigation="Implement a streaming spatial tile pyramid pipeline processing non-overlapping 512x512 pixel chunks sequentially.",
                contingency_plan="Downsample input imagery to medium resolution for fast initial damage overview before running full-res tiles.",
            ),
            ProjectRisk(
                risk="Stale Road Network Topography: Base OpenStreetMap layers failing to reflect newly collapsed bridges or flash flooding.",
                likelihood="Medium",
                impact="High",
                mitigation="Dynamically update pgRouting edge traversal costs to infinity whenever segmentation detects flood water on road geometry.",
                contingency_plan="Allow field rescue operators to draw manual hazard barricades directly on the GIS interface to reroute convoys.",
            ),
            ProjectRisk(
                risk="Field Backhaul Blackout: Complete loss of cellular and internet connectivity across the disaster disaster zone.",
                likelihood="High",
                impact="High",
                mitigation="Package the frontend as an offline Progressive Web App (PWA) with pre-cached local vector map tiles.",
                contingency_plan="Deploy backend services on a portable ruggedized edge server operating an ad-hoc local Wi-Fi mesh.",
            ),
        ]
    elif domain_id == "finance_fraud":
        risks = [
            ProjectRisk(
                risk="Severe Class Imbalance Skew: Fraudulent transactions comprising less than 0.1% of training data causing model bias.",
                likelihood="High",
                impact="High",
                mitigation="Train cost-sensitive XGBoost with scale_pos_weight parameter and optimize Precision-Recall AUC rather than ROC-AUC.",
                contingency_plan="Apply SMOTE oversampling on historical fraud patterns and maintain an active hard-negative mining loop.",
            ),
            ProjectRisk(
                risk="Payment Authorization Latency Spikes: Feature lookup or model scoring exceeding 50ms payment gateway SLA.",
                likelihood="Medium",
                impact="High",
                mitigation="Maintain rolling velocity features in-memory within Redis and deploy model inference via ONNX Runtime.",
                contingency_plan="Implement an asynchronous fallback rule engine that approves low-amount transactions if ML scoring times out.",
            ),
            ProjectRisk(
                risk="Concept Drift & Adversarial Evasion: Fraud syndicates adapting transaction behaviors to evade established model decision boundaries.",
                likelihood="High",
                impact="Medium",
                mitigation="Implement Population Stability Index (PSI) monitoring to detect distribution shifts in transaction attributes daily.",
                contingency_plan="Trigger automated model retraining pipelines whenever PSI exceeds the 0.20 drift alert threshold.",
            ),
            ProjectRisk(
                risk="Regulatory Non-Compliance on Declines: Failure to provide legally mandated adverse action notices explaining card declines.",
                likelihood="Low",
                impact="High",
                mitigation="Compute real-time TreeSHAP feature attributions for every blocked transaction and persist explanation codes.",
                contingency_plan="Provide human compliance officers with a dedicated dispute review console displaying SHAP contribution plots.",
            ),
        ]
    else:
        risks = [
            ProjectRisk(
                risk="Dataset Scarcity & Quality Skew: Insufficient labeled data or noisy ground truth distributions in target domain.",
                likelihood="Medium",
                impact="High",
                mitigation="Utilize established benchmark datasets (e.g. Kaggle, Hugging Face), apply data augmentation, or employ transfer learning.",
                contingency_plan="Fall back to synthetic data generation and pre-trained foundation models with zero/few-shot prompting.",
            ),
            ProjectRisk(
                risk="Model Latency & Throughput Bottlenecks: Real-time inference exceeding acceptable interactive response thresholds.",
                likelihood="Medium",
                impact="Medium",
                mitigation="Quantize model weights to INT8/FP16, utilize ONNX Runtime, and implement asynchronous backend worker queues.",
                contingency_plan="Introduce in-memory Redis response caching for frequent query patterns to eliminate redundant computation.",
            ),
            ProjectRisk(
                risk="Integration & Schema Contract Mismatches: Inconsistent serialization or payload mismatches between frontend and API.",
                likelihood="Low",
                impact="Medium",
                mitigation="Enforce strict Pydantic v2 schemas and OpenAPI contracts between backend routes and frontend client types.",
                contingency_plan="Provide structured JSON mock fallbacks to unblock UI development during backend debugging.",
            ),
            ProjectRisk(
                risk="Compute Resource & Deployment Quota Exhaustion: Limited GPU access or API quota throttling during experimental evaluation.",
                likelihood="Medium",
                impact="High",
                mitigation="Implement local caching of model responses, use lightweight architectures, and utilize Google Colab free tier.",
                contingency_plan="Perform local CPU inference using distilled models (e.g. MobileNet, DistilBERT, or small specialized models).",
            ),
        ]

    return RiskResult(risks=risks)
