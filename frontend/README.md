# NEXTSTEP AI — Academic Project Planning & Mentorship Platform

**Every Step Builds Success.** NEXTSTEP AI is an AI-powered academic project planning, tracking, and mentorship platform. It guides students from initial project planning through blueprint generation, dynamic weekly milestones, progress tracking, risk analysis, and personalized AI mentorship. The React frontend integrates with the existing authenticated FastAPI APIs and AI orchestration engine (`ai_engine.skill_assessment`).

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```
Open [http://localhost:5173/](http://localhost:5173/) in your browser.

### 3. Production Build
```bash
npm run build
```
Generates optimized static assets in `dist/`.

---

## 🎨 Theme Customization

The design system uses centralized CSS custom properties in `src/index.css`. The team can adjust color tokens, borders, and typography instantly without touching component JSX:

```css
:root {
  /* Brand Accent — Currently neutral slate with tasteful indigo/blue */
  --color-primary: #4f46e5;
  --color-primary-hover: #4338ca;
  --color-primary-light: #eef2ff;

  /* Surfaces */
  --color-bg-app: #f8fafc;
  --color-surface-card: #ffffff;
  --color-border: #e2e8f0;
}
```

---

## 📁 Architecture & File Structure

```
frontend/
├── index.html                   # NEXTSTEP AI application metadata and favicon
├── package.json                 # React 19 + Vite + Lucide icons
├── src/
│   ├── main.jsx                 # React root mounting
│   ├── App.jsx                  # Main layout, navbar, step manager & footer
│   ├── App.css                  # Minimal responsive helpers
│   ├── index.css                # Centralized CSS design system & tokens
│   ├── context/
│   │   └── OnboardingContext.jsx # Shared form state, validation, step navigation
│   ├── services/
│   │   └── api.js               # Authenticated backend API services
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.jsx       # Reusable button with loading & icon states
│   │   │   ├── Input.jsx        # Floating/accessible input with inline errors
│   │   │   ├── Select.jsx       # Custom styled accessible dropdown
│   │   │   ├── Badge.jsx        # Pill badges (primary, success, neutral, warning)
│   │   │   ├── Card.jsx         # Card surface container
│   │   │   ├── Alert.jsx        # Notification & feedback banners
│   │   │   ├── Navbar.jsx       # Top brand bar with Sample Data quick-fill
│   │   │   └── StepIndicator.jsx# Visual stepper with animated progress
│   │   ├── onboarding/
│   │   │   └── ProfileForm.jsx  # Page One: Student Profile Setup
│   │   └── skills/
│   │       ├── SkillSelector.jsx     # Preset skill chips + custom skill adder
│   │       ├── SelectedSkillList.jsx # Selected skills with Beginner/Intermediate/Advanced
│   │       ├── EmptySkillState.jsx   # Clean empty state graphic
│   │       └── InterestSelector.jsx  # Multi-select project interest cards
│   └── pages/
│       ├── StudentOnboardingPage.jsx # Page 1 wrapper
│       ├── SkillAssessmentPage.jsx   # Page 2 wrapper
│       └── CompletionPage.jsx        # Staged review & Integration JSON payload export
```

---

## 🔄 User Flow & Form State

1. **Step 1: Student Profile**
   - Full Name (required, min 2 chars)
   - Email Address (required, RFC email regex validation)
   - College / Institution (required)
   - Department / Branch (required dropdown)
   - Current Semester (required dropdown)
   - Expected Graduation Year (required dropdown)
   - Validates on submit attempt and clears errors upon input.

2. **Step 2: Skill & Interest Assessment**
   - Preset popular skills (Python, Java, C++, JavaScript, React, SQL, Machine Learning, AI, Web Development, Data Structures)
   - Custom skill input (e.g. Docker, Flutter, PyTorch)
   - Independent proficiency segmented control per skill:
     - **Beginner**: Basics & coursework
     - **Intermediate**: Comfortable building projects
     - **Advanced**: Production / complex systems
   - Multi-select project interest cards with interactive check states
   - **Back Navigation**: Clicking "Back to Profile" preserves 100% of the entered form data.

3. **Step 3: Staged Review & Payload Export**
   - Summarizes the complete academic profile and skills matrix.
   - Provides a "Copy Integration JSON" button for API developers to test the payload directly against the AI subsystem.

---

## 🔌 Backend Integration Contract

All mock network calls are encapsulated in `src/services/api.js`:
- `mockSaveStudentProfile(profileData)` → maps to `POST /api/v1/students/profile`
- `mockSubmitSkillAssessment(assessmentData)` → maps to `POST /api/v1/students/skills`

The output data structure matches the input required by `ai_engine/skill_assessment.py`:
```json
{
  "project_idea": "<user_project_idea>",
  "self_reported_skills": ["Python", "React", "Machine Learning", "Docker"],
  "experience_level": "intermediate"
}
```
