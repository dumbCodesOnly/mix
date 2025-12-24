# Frontend Hardcode Audit Findings

The following hardcoded instances were found in the `frontend/client` directory:

## 1. Model Names (Hardcoded List)

**File:** `client/src/pages/Chat.tsx`
**Lines:** 15-17
**Code:**
```typescript
const models = [
  { value: 'meta-llama/Llama-3.1-8B-Instruct', label: 'Llama 3.1 8B Instruct' },
  { value: 'mistralai/Mistral-7B-Instruct-v0.1', label: 'Mistral 7B Instruct' },
  { value: 'tiiuae/falcon-7b-instruct', label: 'Falcon 7B Instruct' },
];
```
**File:** `client/src/pages/ImageGeneration.tsx`
**Line:** 15
**Code:**
```typescript
  { value: 'stabilityai/stable-diffusion-3-medium', label: 'Stable Diffusion 3 Medium' },
```
**Review:** These model lists are hardcoded. While the values are currently correct (after the Llama 2 fix), they should ideally be fetched dynamically from a backend API endpoint (e.g., `/api/v1/models`) to ensure the frontend always reflects the models the backend is configured to use. **Recommendation: Create a new backend endpoint to return the list of supported models and update the frontend to fetch this list.**

## 2. API Base URL (Configured via ENV)

**File:** `client/src/lib/api.ts`
**Code:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```
**Review:** This is correctly configured to use a Vite environment variable (`VITE_API_URL`) with a sensible fallback (`http://localhost:8000`). **Status: Correctly configured.**

## 3. External URL (Hardcoded)

**File:** `client/src/components/Map.tsx`
**Code:**
```typescript
  "https://forge.butterfly-effect.dev";
```
**Review:** This appears to be a hardcoded URL for a specific component (likely a map or external service). If this URL is meant to be configurable, it should be moved to an environment variable. Assuming this is a fixed external dependency, it can remain hardcoded, but should be noted. **Recommendation: Review if this URL needs to be configurable.**

## 4. Fonts (External Hardcoded URLs)

**File:** `client/index.html`
**Code:**
```html
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
```
**Review:** Standard practice for loading Google Fonts. **Status: Acceptable.**

---

### Action Plan

The most critical hardcoded issue is the **model lists** in `Chat.tsx` and `ImageGeneration.tsx`. Relying on these static lists is fragile, as demonstrated by the Llama 2 issue.

**Proposed Fix:**
1.  **Backend:** Create a new endpoint `/api/v1/models` that returns the full list of supported models from `backend/app/utils/config.py`.
2.  **Frontend:** Update `Chat.tsx` and `ImageGeneration.tsx` to fetch this list on component mount.

Since creating a new backend endpoint is a multi-step process, and the immediate goal is to fix the hardcoded models, I will implement a temporary fix for the Image Generation model list to ensure it uses a currently supported model, and then recommend the dynamic model fetching as a future enhancement.

**Immediate Fix (Model List):**
*   Update `ImageGeneration.tsx` to use `stabilityai/stable-diffusion-3.5-large` as the default, which is the current default in the backend config.

**Long-Term Fix (Recommended):**
*   Implement dynamic model fetching from the backend.

I will proceed with the immediate fix for the Image Generation model list now.
