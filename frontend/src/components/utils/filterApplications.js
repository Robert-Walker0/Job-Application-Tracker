const filterDefinitions = [
    { key: "status", matches: (app, value) => app.status === value },
    { key: "searchText", matches: (app, value) =>
            app.company.toLowerCase().includes(value.toLowerCase()) ||
            app.jobTitle.toLowerCase().includes(value.toLowerCase())
    },
    { key: "priority", matches: (app, value) => app.priority === value },
    { key: "isInactive", matches: (app, value) => {
        if (value == true) return Boolean(app.isInactive) === true;
        
        return true;
        }
    },
    { key: "minPay", matches: (app, value) => Number(app.payAmount) >= Number(value) },
    { key: "maxPay",  matches: (app, value) => Number(app.payAmount) <= Number(value) },
    { key: "dateFrom", matches: (app, value) => app.dateApplied >= value },
    { key: "dateTo", matches: (app, value) => app.dateApplied <= value }
];


// TODO: Add inactive filter, inactivity has an application.isInactive property.

export function filterApplications(applications, filters) {
    return applications.filter(app =>
        filterDefinitions.every(def => {
            const value = filters[def.key];
            if (value === undefined || value === null || value === "") return true;
            if ((def.key === "minPay" || def.key === "maxPay") && Number(value) === 0) {
                return true;
            }

            return def.matches(app, value);
        })
    );
}