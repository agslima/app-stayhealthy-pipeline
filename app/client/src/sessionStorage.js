/**
 * Canonical browser storage key for patient portal session state.
 *
 * @type {string}
 */
export const SESSION_STORAGE_KEY =
  import.meta.env.VITE_PATIENT_PORTAL_SESSION_STORAGE_KEY || 'patient_portal_session';

const isPlainObject = (value) => {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
};

const normalizeSession = (session) => {
  if (!isPlainObject(session) || typeof session.token !== 'string' || !session.token.trim()) {
    return null;
  }

  const { user } = session;
  if (!isPlainObject(user) || typeof user.role !== 'string' || !user.role.trim()) {
    return null;
  }

  const sanitizedUser = {};
  for (const field of ['id', 'email']) {
    if (field in user) {
      if (typeof user[field] !== 'string') return null;
      sanitizedUser[field] = user[field];
    }
  }
  sanitizedUser.role = user.role;
  if ('mfaEnabled' in user) {
    if (typeof user.mfaEnabled !== 'boolean') return null;
    sanitizedUser.mfaEnabled = user.mfaEnabled;
  }

  return { token: session.token, user: sanitizedUser };
};

/**
 * Read and deserialize the stored patient session.
 *
 * @returns {object|null} Parsed session data, or `null` when missing or invalid.
 */
export function readStoredSession() {
  try {
    const raw = sessionStorage.getItem(SESSION_STORAGE_KEY);
    return raw ? normalizeSession(JSON.parse(raw)) : null;
  } catch {
    return null;
  }
}

/**
 * Persist the current patient session payload.
 *
 * @param {object} session - Session data to serialize into sessionStorage.
 */
export function writeStoredSession(session) {
  const sanitizedSession = normalizeSession(session);
  if (!sanitizedSession) {
    throw new TypeError('Invalid patient portal session.');
  }
  sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(sanitizedSession));
}

/**
 * Remove any stored patient session state.
 */
export function clearStoredSession() {
  sessionStorage.removeItem(SESSION_STORAGE_KEY);
}

/**
 * Replace the access token within an existing stored session.
 *
 * @param {string} token - Fresh access token to persist.
 * @returns {object|null} Updated session payload, or `null` when no session exists.
 */
export function updateStoredSessionToken(token) {
  const currentSession = readStoredSession();
  if (!currentSession) {
    return null;
  }

  const nextSession = {
    ...currentSession,
    token,
  };
  writeStoredSession(nextSession);
  return nextSession;
}
