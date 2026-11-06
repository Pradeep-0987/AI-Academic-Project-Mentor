/**
 * Authentication Service Layer for NEXTSTEP AI
 *
 * Confirmed backend contract:
 * POST /api/auth/login
 * Request:  { "email": string, "password": str }
 * Response: { "access_token": string, "token_type": "bearer", "user": { "id": string, "name": string, "email": string, "created_at": string } }
 *
 * Error codes:
 * - 401 Unauthorized: { "detail": "Invalid email or password" }
 * - 422 Unprocessable Entity: validation errors
 */

export const TOKEN_STORAGE_KEY = 'acad_access_token';
export const USER_STORAGE_KEY = 'acad_user_profile';

/**
 * Persist authentication session in localStorage.
 * @param {string} token
 * @param {object} user
 */
export function saveSession(token, user) {
  try {
    if (token) localStorage.setItem(TOKEN_STORAGE_KEY, token);
    if (user) localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
  } catch (err) {
    console.warn('[Auth Service] Could not save session to localStorage:', err);
  }
}

/**
 * Retrieve saved session from localStorage.
 * @returns {{ token: string | null, user: object | null }}
 */
export function getStoredSession() {
  try {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    const userRaw = localStorage.getItem(USER_STORAGE_KEY);
    const user = userRaw ? JSON.parse(userRaw) : null;
    return { token, user };
  } catch {
    return { token: null, user: null };
  }
}

/**
 * Clear authentication session.
 */
export function clearSession() {
  try {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
  } catch (err) {
    console.warn('[Auth Service] Could not clear session:', err);
  }
}

/**
 * Perform login against the backend API endpoint.
 *
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{ access_token: string, token_type: string, user: { id: string, name: string, email: string, created_at: string } }>}
 */
export async function loginUser(email, password) {
  const payload = {
    email: email.trim(),
    password: password
  };

  let response;

  // Try relative endpoint through Vite proxy first (/api/auth/login),
  // fallback to direct backend host if proxy fails.
  try {
    response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  } catch {
    try {
      response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });
    } catch {
      throw new Error(
        'Unable to connect to the authentication server. Please verify the backend is running at http://localhost:8000.'
      );
    }
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    // Non-JSON response
  }

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error(data?.detail || 'Invalid email or password.');
    }

    if (response.status === 422) {
      if (Array.isArray(data?.detail)) {
        const message = data.detail.map((err) => err.msg || err.type).join('; ');
        throw new Error(`Input validation error: ${message}`);
      }
      throw new Error(data?.detail || 'Invalid input format.');
    }

    if (response.status === 500) {
      throw new Error(
        data?.detail || 'We’re having trouble signing you in right now. Please try again in a few minutes.).'
      );
    }

    throw new Error(data?.detail || `Login request failed with status ${response.status}.`);
  }

  if (!data?.access_token) {
    throw new Error('Server responded successfully but no access token was returned.');
  }

  return data;
}

/**
 * Register a new user against the backend API endpoint.
 *
 * @param {string} name
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{ access_token: string, token_type: string, user: { id: string, name: string, email: string, created_at: string } }>}
 */
export async function registerUser(name, email, password) {
  const payload = {
    name: name.trim(),
    email: email.trim(),
    password: password
  };

  let response;

  try {
    response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  } catch {
    try {
      response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });
    } catch {
      throw new Error(
        'Unable to connect to the authentication server. Please verify the backend is running at http://localhost:8000.'
      );
    }
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    // Non-JSON response
  }

  if (!response.ok) {
    if (response.status === 409) {
      throw new Error(data?.detail || 'This email address is already registered. Please log in instead.');
    }

    if (response.status === 422) {
      if (Array.isArray(data?.detail)) {
        const message = data.detail.map((err) => err.msg || err.type).join('; ');
        throw new Error(`Validation error: ${message}`);
      }
      throw new Error(data?.detail || 'Invalid registration details.');
    }

    if (response.status === 500) {
      throw new Error(
        data?.detail || 'Server error occurred during account registration. Please try again.'
      );
    }

    throw new Error(data?.detail || `Registration failed with status ${response.status}.`);
  }

  if (!data?.access_token) {
    throw new Error('Server responded successfully but no access token was returned.');
  }

  return data;
}
