const INACTIVE_DAYS_THRESHOLD = 14;

export function isInactiveJobApplication(dateApplied) {
    const applicationDate = new Date(dateApplied);
    const fourteenDaysAgo = new Date();
    fourteenDaysAgo.setDate(fourteenDaysAgo.getDate() - INACTIVE_DAYS_THRESHOLD);
    return applicationDate <= fourteenDaysAgo;
}