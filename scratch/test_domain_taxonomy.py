import re
from typing import Any

def _extract_topic(idea: str) -> str:
    cleaned = idea.strip()
    words = [w for w in re.findall(r"[A-Za-z0-9]+", cleaned) if len(w) > 2]
    return " ".join(words[:4]).title() if words else "Academic Software Project"

DOMAINS_CATALOG = {
    "smart_waste": {
        "keywords": ["waste", "garbage", "trash", "recycle", "segregat", "bin", "dumpster", "clean city", "sanitation"],
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
            "Leaflet.js GIS Mapping"
        ],
        "resources": [
            "ESP32 / Raspberry Pi edge development board with Wi-Fi / GSM module",
            "HC-SR04 ultrasonic distance sensors & HX711 load-cell amplifiers",
            "Kaggle Waste Classification / TACO benchmark dataset for visual segregation",
            "OpenStreetMap / Leaflet GIS routing service or Google OR-Tools"
        ],
        "challenges": [
            "Irregular waste accumulation geometry inside bins causing ultrasonic reflection noise",
            "Battery consumption optimization and intermittent outdoor cellular/Wi-Fi connectivity",
            "Accurate visual segregation under poor lighting or soiled material conditions",
            "Multi-vehicle dynamic traveling salesperson (VRP) computational scaling under live traffic"
        ],
        "recommendations": [
            "Implement rolling median filtering on ultrasonic sensor readings to discard erroneous spikes from uneven trash piles.",
            "Deploy a lightweight quantized YOLOv8-Nano model on edge hardware to maintain real-time inference under 250ms.",
            "Formulate the vehicle routing problem using Google OR-Tools with bin fill-level capacity constraints.",
            "Incorporate edge-side SQLite buffering to ensure zero telemetry data loss during network dropouts."
        ],
        "assumptions": [
            "Municipal bins can be fitted with standardized waterproof sensor enclosures.",
            "Garbage collection drivers have access to smartphone screens for viewing optimized pickup turn-by-turn routes.",
            "City road network topology data is accessible via OpenStreetMap."
        ],
        "target_users": [
            "Municipal sanitation workers and garbage collection truck drivers",
            "City ward waste management supervisors and route dispatchers",
            "Municipal urban planning administrators and environmental audit officers",
            "Local citizens reporting localized overflow or illegal dumping"
        ],
        "functional_requirements": [
            "Real-time ultrasonic & weight sensor telemetry ingestion with automated bin fill-percentage calculation and threshold alerting (>85% capacity)",
            "Dynamic vehicle route optimization engine calculating shortest pickup paths using Dijkstra/A* graph algorithms or Google OR-Tools",
            "Computer vision waste classification module segregating recyclable, organic, and hazardous waste categories using YOLOv8/CNN",
            "Municipal operations GIS map dashboard displaying color-coded bin statuses, collection vehicle locations, and historical fill patterns",
            "Citizen incident reporting portal supporting geolocated photo uploads, automated categorization, and dispatch status tracking",
            "Automated scheduled dispatch reports and fuel/time efficiency analytics generated for city sanitation supervisors"
        ],
        "non_functional_requirements": [
            "Real-time telemetry ingestion latency < 1000ms from sensor broadcast to dashboard update",
            "Edge camera waste classification inference time < 300ms per frame",
            "Route optimization re-computation executed within 3.0 seconds for up to 100 municipal collection points",
            "System availability >= 99.5% with offline edge SQLite telemetry buffering during network dropouts"
        ],
        "mvp_features": [
            "Working ultrasonic sensor prototype transmitting fill levels via MQTT to local backend broker",
            "YOLOv8 inference pipeline accurately identifying 3 waste classes on test images with >80% accuracy",
            "Interactive GIS map showing simulated bins with dynamic route visualization",
            "Automated threshold alert notifications triggered when bin fill reaches critical levels"
        ],
        "out_of_scope": [
            "Physical hydraulic bin-lifting mechanical truck retrofits",
            "Nationwide multi-city cellular roaming telecommunication infrastructure",
            "Commercial resident billing, payment gateways, and municipal tax penalty enforcement"
        ],
        "deliverables": [
            "Working sensor telemetry prototype and edge vision segregation model codebase",
            "Full-stack GIS route optimization dashboard with live MQTT telemetry feed",
            "Empirical performance report documenting route length reduction and model classification accuracy",
            "CapStone thesis document, architecture blueprints, and viva demonstration slides"
        ],
        "success_criteria": [
            ">= 85% waste segregation classification accuracy on held-out test dataset",
            "Demonstrated >= 15% reduction in simulated collection route travel distance compared to static routing",
            "Telemetry pipeline latency verified under 1000ms end-to-end",
            "Zero data loss during simulated 15-minute network disconnect using edge caching"
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
            "YOLOv8 vs Faster R-CNN: YOLOv8 selected for single-stage real-time edge inference suitable for low-power edge compute at 30+ FPS."
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
            "Edge computer vision requires dedicated local hardware acceleration (e.g. Coral TPU or Raspberry Pi 4/5) to achieve 20+ FPS."
        ]
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
            "React.js & WebRTC Video Streaming"
        ],
        "resources": [
            "High-definition RTSP IP Camera or USB 1080p wide-angle camera",
            "Standard face benchmark datasets (LFW, CelebA, WiderFace) for validation",
            "CUDA-capable GPU workstation or cloud instance for face embedding extraction",
            "Student identity roster with enrolled baseline reference portraits"
        ],
        "challenges": [
            "Variations in ambient classroom illumination, side-angles, and motion blur",
            "Partial face occlusions caused by spectacles, facial masks, hair, or leaning postures",
            "Vulnerability to presentation attacks using printed photographs or smartphone screen replays",
            "Sub-second verification latency when comparing multiple faces simultaneously against hundreds of student embeddings"
        ],
        "recommendations": [
            "Employ RetinaFace for robust multi-scale face localization capable of detecting small or angled faces across classroom rows.",
            "Integrate ArcFace additive angular margin loss embeddings for superior discriminative feature separation.",
            "Deploy a lightweight passive liveness detector (eye-blink and texture frequency analysis) to eliminate photo/screen spoofing.",
            "Utilize Faiss or pgvector for sub-50ms nearest-neighbor vector similarity search across the student roster."
        ],
        "assumptions": [
            "Classroom is equipped with a camera positioned with adequate frontal view coverage of student seating areas.",
            "Students participate in an initial one-time enrolment capture under standardized lighting conditions.",
            "Institution complies with local student biometric privacy and data protection policies."
        ],
        "target_users": [
            "Course instructors and teaching assistants managing daily lectures",
            "Department academic coordinators and attendance compliance auditors",
            "Enrolled students tracking their real-time attendance percentages and absence records",
            "Institutional IT administrators configuring camera nodes and student rosters"
        ],
        "functional_requirements": [
            "Real-time multi-face detection and landmark alignment from live classroom RTSP/webcam video feeds using RetinaFace",
            "512-dimensional facial embedding extraction and cosine similarity verification against registered student database using ArcFace",
            "Anti-spoofing liveness detection (blink detection, micro-movement, and texture analysis) to prevent static photo and screen replay fraud",
            "Automated lecture attendance logging with timestamped entry/exit tracking and duplicate check-in suppression",
            "Instructor dashboard displaying live classroom head-count, recognized student cards, and manual attendance override controls",
            "Automated export of attendance compliance reports formatted for university ERP systems (CSV/Excel/PDF)"
        ],
        "non_functional_requirements": [
            "Multi-face detection and embedding matching latency < 350ms per video frame for up to 30 simultaneous faces",
            "Face verification accuracy >= 98.5% True Positive Rate under normal classroom illumination",
            "Presentation attack detection (anti-spoofing) error rate < 2.0%",
            "GDPR / FERPA compliant biometric security: facial embeddings stored as one-way vectors with raw face images encrypted at rest"
        ],
        "mvp_features": [
            "Webcam-based student enrollment module generating stored 512-d ArcFace embeddings",
            "Real-time multi-face detection and recognition loop recognizing enrolled students on live webcam stream",
            "Automated attendance check-in table updating dynamically upon successful facial verification",
            "Faculty lecture session management interface with attendance summary export"
        ],
        "out_of_scope": [
            "Campus-wide 24/7 continuous CCTV public surveillance tracking outside academic lecture halls",
            "Hardware manufacturing of proprietary biometric turnstiles or electromagnetic door lock actuators",
            "Off-campus student location tracking via mobile GPS"
        ],
        "deliverables": [
            "Complete face recognition pipeline source code with RetinaFace, ArcFace, and anti-spoofing modules",
            "Instructor React web dashboard with real-time video feed and attendance status tables",
            "Empirical evaluation report documenting recognition accuracy, latency, and spoof rejection benchmarks",
            "Final capstone documentation, architecture diagrams, and recorded live demo"
        ],
        "success_criteria": [
            "Achieve >= 98% recognition accuracy on enrolled student test cohort",
            "Maintain average processing latency below 400ms per frame on standard GPU compute",
            "100% rejection rate against static printed photo presentation attacks",
            "Eliminate 100% of proxy attendance during simulated lecture sessions"
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
            "FaceNet vs InsightFace: InsightFace selected for its integrated high-speed detection, 2D/3D alignment, and quantized ONNX runtime support."
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
            "Running multi-stream RTSP decoding concurrently requires dedicated GPU VRAM (>= 4GB)."
        ]
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
            "PostgreSQL Relational Schema Design"
        ],
        "resources": [
            "Standard clinical prescription handwriting datasets (IAM / synthetic prescription images)",
            "OpenFDA and RxNorm pharmaceutical interaction database APIs",
            "GPU compute environment for fine-tuned Vision-Encoder-Decoder OCR inference",
            "Standard medical terminology dictionaries (SNOMED-CT / ICD-10)"
        ],
        "challenges": [
            "Severe cursive handwriting irregularities, variable ink pressure, and skewed camera angles",
            "Distinguishing between look-alike and sound-alike (LASA) pharmaceutical drug names",
            "Complex multi-drug regimen interaction combinatorial matrix evaluation",
            "Stringent patient health information (PHI) confidentiality and HIPAA compliance requirements"
        ],
        "recommendations": [
            "Utilize transformer-based TrOCR fine-tuned on cursive medical text to outperform traditional rule-based OCR engines.",
            "Implement Levenshtein distance and phonetic matching against the RxNorm drug catalog to rectify OCR character errors.",
            "Pre-cache common drug-drug interaction contraindication tables locally to enable sub-50ms pharmacist screening alerts.",
            "Enforce client-side image redaction of sensitive patient identifiers before cloud processing."
        ],
        "assumptions": [
            "Input prescription images have sufficient resolution (>= 300 DPI) and minimal physical tearing.",
            "Clinical interaction rules follow standardized medical authority guidelines.",
            "System is operated as an assistive validation tool with mandatory licensed pharmacist sign-off."
        ],
        "target_users": [
            "Licensed clinical and retail hospital pharmacists",
            "Outpatient dispensary staff and pharmacy technicians",
            "General physicians reviewing patient multi-medication histories",
            "Healthcare quality and patient safety audit officers"
        ],
        "functional_requirements": [
            "High-resolution prescription image ingestion, perspective correction, binarization, and noise reduction",
            "Handwritten text recognition (HTR) pipeline extracting medicine names, dosage frequencies, and duration using TrOCR / Tesseract",
            "Entity extraction and normalization mapping brand names to standardized generic RxNorm / ATC pharmacological codes",
            "Real-time drug-drug interaction (DDI) contraindication screening engine querying clinical pharmaceutical databases",
            "Pharmacist review portal highlighting detected medicines with confidence scores, extracted dosage tags, and red-flag interaction warnings",
            "Digital prescription validation audit trail and patient dosage summary PDF export"
        ],
        "non_functional_requirements": [
            "Prescription OCR and entity extraction response time < 2500ms per standard document page",
            "Drug-drug interaction screening evaluation latency < 100ms once entities are normalized",
            "Drug name character recognition accuracy >= 94% on legible handwriting benchmarks",
            "Zero persistence of unencrypted Protected Health Information (PHI) to non-volatile storage"
        ],
        "mvp_features": [
            "Prescription image upload portal with automated crop and contrast enhancement",
            "TrOCR inference pipeline identifying at least 3 distinct prescribed medicines with confidence metrics",
            "Interactive dosage and drug interaction validation table alerting user of high-risk drug pairs",
            "Exportable pharmacist review summary verification sheet"
        ],
        "out_of_scope": [
            "Direct automated dispensing robotics or physical pill-counting machinery hardware",
            "Automated electronic health insurance reimbursement billing workflows",
            "Full electronic health record (EHR) hospital system replacement"
        ],
        "deliverables": [
            "End-to-end prescription OCR and clinical entity extraction pipeline codebase",
            "Pharmacist validation web application with interactive bounding-box document viewer",
            "Empirical evaluation report documenting OCR character accuracy, entity recall, and interaction latency",
            "Complete academic thesis report, architecture specifications, and oral viva slides"
        ],
        "success_criteria": [
            ">= 92% Top-1 drug entity recognition accuracy on held-out test prescription set",
            "100% detection rate of known high-severity drug interaction pairs in benchmark test cases",
            "End-to-end document processing pipeline completed in under 3.0 seconds",
            "Validated against at least 100 real-world or synthetic handwritten prescription samples"
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
            "Live External API vs Local RxNorm Database: Local PostgreSQL RxNorm tables eliminate cloud API rate-limiting and ensure sub-50ms contraindication query latency."
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
            "Drug interaction engine coverage depends on completeness of the underlying RxNorm/OpenFDA open-source datasets."
        ]
    }
}

def detect_domain(idea: str) -> tuple[str, dict[str, Any]]:
    text = idea.lower()
    for domain_id, profile in DOMAINS_CATALOG.items():
        if any(k in text for k in profile["keywords"]):
            return domain_id, profile
    # Return dynamic fallback profile
    topic = _extract_topic(idea)
    return "custom", {
        "title": f"{topic}: Intelligent Real-Time Analysis & Decision Support System",
        "problem_statement": (
            f"Operational workflows in {idea.strip().lower()} frequently suffer from manual oversight, unpredictable error rates, "
            f"and delayed decision latency due to lack of real-time telemetry and automated intelligence. Conventional approaches "
            f"rely on static, fragmented procedures that lead to inefficiencies, resource wastage, and elevated operational risks."
        ),
        "skills": ["Python 3.12", "FastAPI / Asynchronous REST", "Machine Learning / Predictive Modeling", "Modern React.js", "SQL Database Schema Design"],
        "resources": ["Benchmark research datasets (Kaggle / UCI)", "Development workstation with CPU/GPU compute", "Version control via Git/GitHub"],
        "challenges": ["Noisy data inputs and class imbalance in target domain", "Maintaining low-latency real-time response times", "Integration across distributed software layers"],
        "recommendations": ["Establish a verified baseline model early.", "Construct modular service endpoints with strict Pydantic validation.", "Incorporate real-time event notifications."],
        "assumptions": ["Required input telemetry is accessible through standard protocols.", "System operates within academic prototype evaluation standards."],
        "target_users": ["Domain operators and field technicians", "Academic evaluators and project mentors", "System administrators monitoring live health"],
        "functional_requirements": [
            f"Real-time input telemetry acquisition and validation pipeline for {topic}",
            f"Domain-specific computational / predictive algorithmic core utilizing optimized machine learning models for {topic}",
            "Continuous anomaly detection, rule compliance evaluation, and automated threshold-based event alerting",
            "Interactive operational control dashboard presenting live telemetry streams, performance analytics, and diagnostic logs",
            "Automated remediation workflow triggering actionable recommendations and closed-loop process adjustments",
            "Comprehensive audit logging, historical trend aggregation, and exportable academic performance evaluation reporting"
        ],
        "non_functional_requirements": [
            "End-to-end processing and decision response latency under 350ms for live transactions/telemetry",
            "High availability >= 99.5% with graceful offline caching and automatic reconnect",
            "System throughput capable of processing up to 500 concurrent events per second",
            "Strict data protection compliance with end-to-end encryption for stored records and transit payloads"
        ],
        "mvp_features": [
            f"Core predictive or analytical processing pipeline verified against representative benchmark test datasets for {topic}",
            "Interactive user interface demonstrating real-time data submission, live processing, and result rendering",
            "Automated threshold alert mechanism triggering visual notifications upon anomalous conditions",
            "Complete academic documentation including system architecture diagrams and empirical evaluation methodology"
        ],
        "out_of_scope": [
            "Enterprise multi-region distributed cloud clustering infrastructure",
            "Custom physical hardware silicon fabrication or proprietary chip design",
            "Commercial billing, subscription payment gateways, and advertising management"
        ],
        "deliverables": [
            "Fully tested and documented source code repository with reproducible environment setup",
            "Comprehensive Project Synopsis and System Architecture Specification",
            "Empirical Evaluation Report with confusion matrices, loss curves, or benchmark graphs",
            "Live presentation slides and functional prototype demonstration video"
        ],
        "success_criteria": [
            "Achievement of target evaluation metrics (e.g., F1-score >= 0.85 or system response < 500ms)",
            "Zero critical security or data validation vulnerabilities in core routes",
            "Successful end-to-end demonstration during final faculty viva / academic evaluation",
            "Delivery of all project artifacts within the allocated timeframe"
        ],
        "frontend": ["React.js", "Vite", "TailwindCSS / Modern CSS", "Lucide Icons", "Recharts"],
        "backend": ["FastAPI (Python 3.12)", "Uvicorn ASGI Server", "Pydantic v2", "asyncio"],
        "database": ["PostgreSQL / Supabase", "SQLite (Local development)", "SQLAlchemy 2.0 ORM"],
        "ai_ml": ["Scikit-Learn", "NumPy & Pandas", "PyTorch 2.x"],
        "deployment": ["Docker", "Vercel / Netlify (Frontend)", "Render / Railway (Backend)"],
        "development_tools": ["Git & GitHub", "Pytest", "Postman / Swagger OpenAPI"],
        "alternatives": [
            "Flask / Django: Evaluated but FastAPI selected for automatic OpenAPI docs, asynchronous I/O, and Pydantic validation.",
            "MongoDB: Evaluated but PostgreSQL/SQLite selected for relational schema integrity, ACID compliance, and foreign key relations.",
            "TensorFlow/Keras: Evaluated but PyTorch selected for dynamic computation graph, Pythonic debugging, and wider contemporary research paper support."
        ],
        "rationale": "The recommended stack balances developer velocity, academic rigor, and execution reliability.",
        "reasoning": "Architectural Reasoning Output: Multi-tiered decoupled architecture for academic rigor and reliability.",
        "limitations": ["Requires GPU compute for heavy deep learning passes.", "Cold-start latency on free-tier cloud instances."]
    }

def test_runner():
    test_ideas = [
        "Smart waste management system using IoT and machine learning",
        "AI-based automated attendance system using facial recognition",
        "Medical prescription OCR and drug interaction checker",
        "Quantum key distribution security protocol simulator"
    ]
    for idea in test_ideas:
        dom_id, prof = detect_domain(idea)
        print("========================================")
        print(f"Idea: {idea}")
        print(f"Detected Domain: {dom_id}")
        print(f"Project Title: {prof['title']}")
        print(f"Problem Statement:\n  {prof['problem_statement'][:120]}...")
        print(f"Functional Reqs (count: {len(prof['functional_requirements'])}):")
        for i, fr in enumerate(prof['functional_requirements'], 1):
            print(f"  {i}. {fr}")
        print(f"Tech Stack Frontend: {prof['frontend'][:3]}")
        print(f"Tech Stack AI/ML: {prof['ai_ml'][:3]}")

if __name__ == "__main__":
    test_runner()
