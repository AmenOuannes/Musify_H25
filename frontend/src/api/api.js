const configuredUrl = import.meta.env.VITE_API_URL

export const URL = configuredUrl
  ? configuredUrl.replace(/\/$/, '')
  : (import.meta.env.DEV ? '/api' : '')
