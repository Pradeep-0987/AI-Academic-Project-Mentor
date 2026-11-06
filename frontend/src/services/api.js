import { getStoredSession } from './auth';

export const PRESET_SKILLS = [
  'Python', 'Java', 'C++', 'JavaScript', 'React', 'SQL',
  'Machine Learning', 'AI', 'Web Development', 'Data Structures'
];

export const PRESET_INTERESTS = [
  { id: 'ai_ml', title: 'AI & Machine Learning', description: 'Neural networks, LLMs, computer vision, and predictive models', iconName: 'Brain' },
  { id: 'web_dev', title: 'Web Development', description: 'Full-stack modern web apps, APIs, microservices, and design systems', iconName: 'Globe' },
  { id: 'app_dev', title: 'Mobile App Development', description: 'Native & cross-platform applications for iOS and Android', iconName: 'Smartphone' },
  { id: 'data_science', title: 'Data Science & Analytics', description: 'Big data processing, statistical modeling, and insights dashboards', iconName: 'BarChart3' },
  { id: 'cybersecurity', title: 'Cybersecurity', description: 'Vulnerability assessment, network defense, cryptography, and audits', iconName: 'ShieldCheck' },
  { id: 'cloud_devops', title: 'Cloud & DevOps', description: 'Containerization, CI/CD pipelines, AWS/GCP architecture, and Docker', iconName: 'Cloud' },
  { id: 'iot_robotics', title: 'IoT & Embedded Systems', description: 'Arduino, Raspberry Pi, sensor networks, robotics, and edge computing', iconName: 'Cpu' },
  { id: 'nlp_speech', title: 'NLP & Language Tech', description: 'Text mining, summarization, sentiment analysis, and conversational agents', iconName: 'MessageSquare' }
];

export const DEPARTMENTS = [
  'Computer Science & Engineering (CSE)',
  'Information Technology (IT)',
  'Artificial Intelligence and Machine Learning (AIML)',
  'Artificial Intelligence & Data Science (AI & DS)',
  'Electronics & Communication Engineering (ECE)',
  'Electrical & Electronics Engineering (EEE)',
  'Mechanical Engineering',
  'Civil Engineering',
  'Biotechnology / Biomedical',
  'Other / Interdisciplinary'
];

export const SEMESTERS = [
  'Semester 1 (Year 1)', 'Semester 2 (Year 1)', 'Semester 3 (Year 2)',
  'Semester 4 (Year 2)', 'Semester 5 (Year 3)', 'Semester 6 (Year 3)',
  'Semester 7 (Final Year)', 'Semester 8 (Final Year)',
  'Postgraduate / Masters (Year 1)', 'Postgraduate / Masters (Year 2)'
];

export const GRADUATION_YEARS = ['2025', '2026', '2027', '2028', '2029', '2030'];

async function authenticatedRequest(path, options = {}) {
  const { token } = getStoredSession();
  if (!token) throw new Error('Your session has expired. Please log in again.');

  let response;
  try {
    response = await fetch(path, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        Authorization: `Bearer ${token}`,
        ...options.headers
      }
    });
  } catch {
    throw new Error('Unable to connect to the project server. Check that the backend is running.');
  }

  let responseBody;
  try {
    responseBody = await response.json();
  } catch {
    responseBody = null;
  }
  if (!response.ok) {
    const detail = responseBody?.detail;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).filter(Boolean).join('; ')
      : detail;
    throw new Error(message || `Request failed (${response.status}).`);
  }
  return responseBody;
}

export async function saveStudentProfileOnboarding(profileData) {
  if (!profileData.fullName || !profileData.email || !profileData.institution || !profileData.department) {
    throw new Error('Please fill in all required profile fields.');
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profileData.email)) {
    throw new Error('Please provide a valid institutional or personal email address.');
  }
  await authenticatedRequest('/api/students/profile', {
    method: 'POST',
    body: JSON.stringify({
      institution: profileData.institution.trim(),
      department: profileData.department.trim(),
      semester: profileData.semester,
      graduation_year: Number(profileData.graduationYear)
    })
  });
  return {
    success: true,
    isBackendConnected: true,
    data: { ...profileData, updatedAt: new Date().toISOString() },
    message: 'Profile details saved successfully.'
  };
}

export async function submitStudentSkillAssessment(assessmentData) {
  if (!assessmentData.skills?.length) {
    throw new Error('Please select or add at least one technical skill.');
  }
  if (!assessmentData.interests?.length) {
    throw new Error('Please choose at least one area of interest for your project.');
  }
  await authenticatedRequest('/api/students/skills', {
    method: 'POST',
    body: JSON.stringify({
      skills: assessmentData.skills.map((skill) => ({
        name: skill.name,
        level: skill.level || 'Intermediate',
        isCustom: Boolean(skill.isCustom)
      })),
      interests: assessmentData.interests
    })
  });
  return {
    success: true,
    isBackendConnected: true,
    data: { ...assessmentData, submittedAt: new Date().toISOString() },
    message: 'Skills and project interests saved successfully.'
  };
}

export function listProjects() {
  return authenticatedRequest('/api/projects');
}

export function createProject(project) {
  return authenticatedRequest('/api/projects', {
    method: 'POST',
    body: JSON.stringify(project)
  });
}

export function getProjectBlueprint(projectId) {
  return authenticatedRequest(`/api/projects/${encodeURIComponent(projectId)}/blueprint`);
}

export function generateProjectBlueprint(projectId) {
  return authenticatedRequest(`/api/projects/${encodeURIComponent(projectId)}/blueprint`, {
    method: 'POST'
  });
}

export function updateMilestoneStatus(projectId, weekNumber, status) {
  return authenticatedRequest(
    `/api/projects/${encodeURIComponent(projectId)}/milestones/${weekNumber}`,
    { method: 'PATCH', body: JSON.stringify({ status }) }
  );
}

export function sendProjectMentorMessage(projectId, message, history) {
  return authenticatedRequest(`/api/projects/${encodeURIComponent(projectId)}/chat`, {
    method: 'POST',
    body: JSON.stringify({ message, history })
  });
}

export function saveStudentProfile(profile) {
  return authenticatedRequest('/api/students/profile', {
    method: 'POST',
    body: JSON.stringify({
      institution: profile.institution,
      department: profile.department,
      semester: profile.semester,
      graduation_year: Number(profile.graduationYear)
    })
  });
}
