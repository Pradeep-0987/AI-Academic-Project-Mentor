from typing import Any
import re
from ai_engine.schemas import (
    PlanningResult,
    PlannedPhase,
    WeeklyMilestone,
)
from ai_engine.agents.heuristic_fallback import _detect_domains

def generate_progressive_planning(
    project_idea: str,
    duration_weeks: int,
    team_size: int,
    scope: dict[str, Any],
    technology: dict[str, Any],
) -> PlanningResult:
    cleaned = project_idea.strip()
    words = [w for w in re.findall(r"[A-Za-z0-9]+", cleaned) if len(w) > 2]
    topic = " ".join(words[:4]).title() if words else "Academic Software Project"
    domains = _detect_domains(cleaned)

    # 1. Domain-specific contextual nouns
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

    # 2. Master progressive catalog of 12 distinct academic phases
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
            "title": f"Exploratory Data Analysis (EDA) & Data Cleansing",
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
            "title": f"Data Preprocessing & Feature Engineering Pipeline",
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
            "title": f"Baseline Model Implementation & Benchmark Establishment",
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
        # Map w (1..w_count) to an index in master_stages (0..total_stages - 1)
        if w_count == 1:
            idx = 0
        else:
            idx = int(round((w - 1) * (total_stages - 1) / (w_count - 1)))
        idx = max(0, min(idx, total_stages - 1))
        stage = master_stages[idx]

        # Make title clean without repeating 'Week X: Week X:'
        m_title = f"Week {w}: {stage['title']}"
        m_obj = [stage["objective"]]
        
        # Ensure tasks are distinct even if two weeks map to the same stage
        raw_tasks = stage["tasks"]
        unique_tasks = []
        for t in raw_tasks:
            task_str = t
            if task_str in seen_tasks:
                task_str = f"{t} (Iteration {w})"
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

    # 4 balanced phases for duration_weeks
    p1_len = max(1, w_count // 4)
    p2_len = max(1, w_count // 4)
    p3_len = max(1, w_count // 4)
    p4_len = w_count - (p1_len + p2_len + p3_len)
    if p4_len < 1:
        p4_len = 1
        p3_len = max(1, p3_len - 1)

    phases = [
        PlannedPhase(
            phase_name="Phase 1: Research, Data Architecture & Feature Engineering",
            start_week=1,
            duration_weeks=p1_len,
            tasks=[
                f"Conduct systematic literature review and define research boundaries for {topic}",
                f"Acquire, inspect, and preprocess primary {data_spec}",
                "Initialize repository structure, branch rules, and CI configuration",
            ],
            deliverables=[
                "Project Synopsis & Literature Review Matrix",
                "Exploratory Data Analysis (EDA) Report & Data Dictionary",
                "Automated Preprocessing & Feature Engineering Pipeline",
            ],
            dependencies=[],
        ),
        PlannedPhase(
            phase_name="Phase 2: Algorithmic Modeling, Training & Optimization",
            start_week=p1_len + 1,
            duration_weeks=p2_len,
            tasks=[
                "Implement reference baseline models and log comparative benchmark metrics",
                f"Develop target {model_spec} with custom training routines",
                f"Conduct hyperparameter tuning and ablation studies (evaluating {eval_spec})",
            ],
            deliverables=[
                "Baseline and Optimized Model Weights",
                "Comprehensive Ablation Study & Convergence Curves",
                "Algorithmic Methodology Chapter Draft",
            ],
            dependencies=["Phase 1: Research, Data Architecture & Feature Engineering"],
        ),
        PlannedPhase(
            phase_name="Phase 3: Backend API, User Interface & System Integration",
            start_week=p1_len + p2_len + 1,
            duration_weeks=p3_len,
            tasks=[
                "Build asynchronous FastAPI endpoints with Pydantic request/response validation",
                "Construct interactive React dashboard views and telemetry visualization charts",
                "Connect frontend client state with backend APIs and handle error boundaries",
            ],
            deliverables=[
                "Functional FastAPI Backend with Swagger OpenAPI Documentation",
                "Interactive React User Interface",
                "Integrated End-to-End System Prototype",
            ],
            dependencies=["Phase 2: Algorithmic Modeling, Training & Optimization"],
        ),
        PlannedPhase(
            phase_name="Phase 4: System Verification, Academic Thesis & Viva Defense",
            start_week=p1_len + p2_len + p3_len + 1,
            duration_weeks=p4_len,
            tasks=[
                "Execute automated test suites ensuring >= 80% coverage on critical modules",
                "Draft comprehensive academic project thesis following university guidelines",
                "Create viva presentation slides and rehearse live system demonstration",
            ],
            deliverables=[
                "Complete Academic Project Thesis Document",
                "Automated Test Execution Summary (Code Coverage >= 80%)",
                "Academic Viva Slide Deck & Demonstration Recording",
            ],
            dependencies=["Phase 3: Backend API, User Interface & System Integration"],
        ),
    ]

    return PlanningResult(
        total_duration_weeks=duration_weeks,
        phases=phases,
        weekly_milestones=weekly_milestones,
    )

# Test for 8 weeks with Smart Waste Management
plan = generate_progressive_planning("Smart Waste Management", 8, 4, {}, {})
print("--- 8 WEEKS TEST ---")
all_tasks = []
for m in plan.weekly_milestones:
    print(f"\n{m.milestone_title}")
    print(f"  Objective: {m.objectives[0]}")
    print(f"  Deliverable: {m.deliverables[0]}")
    for t in m.tasks:
        all_tasks.append(t)
        print(f"   * {t}")

print(f"\nTotal tasks: {len(all_tasks)}, Unique: {len(set(all_tasks))}")
assert len(all_tasks) == len(set(all_tasks)), "DUPLICATE TASKS FOUND!"
print("PASSED: 100% UNIQUE TASKS ACROSS ALL WEEKS!")
