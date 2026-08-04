/**
 * Admin utility functions.
 * Pure helpers only — no API calls.
 */

/** Format an ISO date string to a readable format. */
export function formatDate(isoString: string): string {
  return new Date(isoString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
