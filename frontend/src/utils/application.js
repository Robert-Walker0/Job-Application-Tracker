const MILLISECONDS_PER_SECOND = 1000;
const SECONDS_PER_MINUTE = 60;
const MINUTES_PER_HOUR = 60
const HOURS_PER_DAY = 24;
const MILLISECONDS_PER_DAY = MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY;
const INACTIVE_DAYS_THRESHOLD = 14;

export function validateJobApplication(application) {
    if (application.company === "") return false;
    if (application.jobTitle === "") return false;
    if (application.dateApplied === "") return false;
    if (application.payType === "") return false;
    return true;
}

export function isInactiveApplication(dateApplied) {
    const appliedDate = new Date(dateApplied);
    const todaysDate = new Date();
    const millisecondDifference = todaysDate - appliedDate;
    const diffDays = millisecondDifference / MILLISECONDS_PER_DAY;
    return diffDays >= INACTIVE_DAYS_THRESHOLD;
}

export function formatDate(date) {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString();
}