import { beforeEach, describe, expect, it } from 'vitest';
import { SESSION_STORAGE_KEY, readStoredSession, writeStoredSession } from './sessionStorage';

describe('sessionStorage', () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  it('stores only recognized session and user fields', () => {
    const session = JSON.parse(
      '{"token":"access-token","user":{"id":"patient-1","email":"patient@example.test","role":"patient","mfaEnabled":false,"isAdmin":true,"__proto__":{"polluted":true}},"isAdmin":true}'
    );

    writeStoredSession(session);

    expect(sessionStorage.getItem(SESSION_STORAGE_KEY)).toBe(
      JSON.stringify({
        token: 'access-token',
        user: {
          id: 'patient-1',
          email: 'patient@example.test',
          role: 'patient',
          mfaEnabled: false,
        },
      })
    );
    expect(readStoredSession()).toEqual({
      token: 'access-token',
      user: {
        id: 'patient-1',
        email: 'patient@example.test',
        role: 'patient',
        mfaEnabled: false,
      },
    });
  });

  it('rejects sessions without the expected authentication fields', () => {
    expect(() => writeStoredSession({ token: '', user: { role: 'patient' } })).toThrow(
      'Invalid patient portal session.'
    );
    expect(sessionStorage.getItem(SESSION_STORAGE_KEY)).toBeNull();
  });

  it('ignores malformed or invalid sessions already in browser storage', () => {
    sessionStorage.setItem(SESSION_STORAGE_KEY, '{"token":"access-token","user":[]}');

    expect(readStoredSession()).toBeNull();
  });
});
