# Sprint 9 Planning (1 Week)

**Sprint window:** 7 days
**Goal:** Ship authenticated access. Users sign in through Supabase before reaching the dashboard, the API rejects anonymous traffic, and every PR into main is blocked unless the test suite passes.

## Why this sprint
The platform has been open to anyone with the URL. Before adding customer-facing analytics, access needs an identity layer. Supabase gives hosted auth (email/password now, OAuth later) without running our own user database.

## Assigned Tickets
- **[AB-501]** Add Supabase project + env plumbing (frontend and backend) (2 points)
- **[AB-502]** Build Login/Signup UI matching glass theme (3 points)
- **[AB-503]** Gate the dashboard behind a Supabase session (3 points)
- **[AB-504]** Verify Supabase JWTs in FastAPI, protect /api/stats and /api/me (5 points)
- **[AB-505]** Repair broken unit tests, add API auth tests (3 points)
- **[AB-506]** PR validation: run tests on pull requests, block merge on failure (2 points)
- **[AB-507]** Frontend lint + build job in CI (1 point)
- **[AB-508]** Rewrite README to reflect the real architecture (2 points)

**Total committed:** 21 points

## Day-by-day
| Day | Focus |
|-----|-------|
| 1 | Supabase project setup, env vars in both apps (AB-501) |
| 2 | Login/Signup component + session lifecycle (AB-502, AB-503) |
| 3 | Backend JWT verification dependency, protect endpoints (AB-504) |
| 4 | Fix test suite, add auth API tests (AB-505) |
| 5 | Pipeline PR trigger + frontend job, set branch policy (AB-506, AB-507) |
| 6 | README rewrite, docs pass (AB-508) |
| 7 | Buffer: end-to-end auth walkthrough on the live ACA deployment, retro notes |

## Definition of Done
- Anonymous GET /api/stats returns 401
- Signing in on the deployed frontend lands on the dashboard
- A PR with a failing test cannot merge into main
- README quickstart works on a clean machine
