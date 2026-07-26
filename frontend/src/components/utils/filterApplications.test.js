import { describe, test, expect } from "vitest";
import { filterApplications } from "./filterApplications";

const applications = [
    { id: 1, company: "Google", jobTitle: "Frontend Lead", status: "Interview", priority: "High", payAmount: 120000, dateApplied: "2026-07-26", isInactive: false},
    { id: 2, company: "Meta", jobTitle: "Backend Engineer", status: "Applied", priority: "Low", payAmount: 90000, dateApplied: "2026-07-15", isInactive: false},
    { id: 3, company: "Netflix", jobTitle: "Software Engineer", status: "Interview", priority: "Low", payAmount: 150000, dateApplied: "2026-07-20", isInactive: false, },
    { id: 4, company: "Test Company 4", jobTitle: " Engineer", status: "Interview", priority: "Low", payAmount: 150000, dateApplied: "2026-07-20", isInactive: false},
    { id: 5, company: "Microsoft", jobTitle: "System Lead", status: "Applied", priority: "Low", payAmount: 150000, dateApplied: "2026-05-20", isInactive: true }
];

const emptyFilters = {
    status: "", searchText: "", priority: "",
    minPay: 0, maxPay: 0, dateFrom: "", dateTo: ""
};

describe("filterApplications", () => {
    test("returns all applications when filter is not active", () => {
        const result = filterApplications(applications, emptyFilters);
        expect(result).toHaveLength(5);
    });

    test("returns an empty array when no applications matches the filters", () => {
        const result = filterApplications(applications, {...emptyFilters, status: "offer"});
        expect(result).toEqual([]);
        expect(result).toHaveLength(0);
    });

    test("returns an empty array when combined filters and valid but mutual exclusive", () => {
        const result = filterApplications(applications, {...emptyFilters, status: "Interview", maxPay: 100});
        expect(result).toEqual([]);
        expect(result).toHaveLength(0);
    });

    test("filter by status only", () => {
        const result = filterApplications(applications, {...emptyFilters, status: "Interview"});
        expect(result).toHaveLength(3);
    });

    test("filters by old applications", () => {
        const result = filterApplications(applications, {...emptyFilters, isInactive: true});
        expect(result).toHaveLength(1);
        expect(result[0].id).toBe(5);
    });

    test("searching matches company or job title", () => {
        const byCompany = filterApplications(applications, {...emptyFilters, searchText: "goog"});
        expect(byCompany).toHaveLength(1);

        const byTitle = filterApplications(applications, {...emptyFilters, searchText: "engineer"});
        expect(byTitle.map(appliction => appliction.id)).toEqual([2, 3, 4]);
    });

    test("combines status AND priority AND minPay", () => {
        const result = filterApplications(applications, {...emptyFilters, status: "Interview", priority: "High", minPay: 120000});
        expect(result).toHaveLength(1);
        expect(result[0].id).toBe(1);
    });

    test("minPay and maxPay exclude applications outside the range", () => {
        const result = filterApplications(applications, { ...emptyFilters, minPay: 100000, maxPay: 140000 });
        expect(result.map(a => a.id)).toEqual([1]);
    });

});