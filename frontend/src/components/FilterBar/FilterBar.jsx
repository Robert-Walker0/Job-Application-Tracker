import { useState } from "react";
import FormInput from "../ApplicationForm/FormInput";
import FormSelect from "../ApplicationForm/FormSelect";
import "./FilterBar.css";

export default function FilterBar({ filters, onFilterChange, onClear }) {
    const [isOpen, setIsOpen] = useState(false);

    function handleChange(field, value) {
        onFilterChange(prev => ({ ...prev, [field]: value }));
    }

    return (
        <div className="filter-bar-container">
            <button className="filter-toggle-btn" onClick={() => setIsOpen(previousState => !previousState)}>
                {isOpen ? "Hide Filters ▲" : "Show Filters  ▼"}
            </button>
    
        {isOpen && (
            <div className="filter-bar">
                <FormSelect
                    label="Status"
                    value={filters.status}
                    onChange={e => handleChange("status", e.target.value)}
                    options={["", "Applied", "Interview", "Offer", "Rejected", "Withdrawn"]}
                />

                <FormInput
                    label="Search"
                    value={filters.searchText}
                    onChange={e => handleChange("searchText", e.target.value)}
                    placeholder="Company or job title"
                />

                <FormSelect
                    label="Priority"
                    value={filters.priority}
                    onChange={e => handleChange("priority", e.target.value)}
                    options={["", "None", "Low", "Medium", "High"]}
                />

                <FormSelect
                    label="Outdated"
                    value={filters.isInactive ? "Include Out of Date" : "All"}
                    onChange={e => {
                        const selected = e.target.value;
                        const newValue = selected === "Include Out of Date" ? true : false;
                        handleChange("isInactive", newValue);
                    }}
                    options={["All", "Include Out of Date"]}
                    type="boolean"
                />

                <FormInput
                    label="Min Pay"
                    value={filters.minPay}
                    onChange={e => handleChange("minPay", e.target.value)}
                    type="number"
                />

                <FormInput
                    label="Max Pay"
                    value={filters.maxPay}
                    onChange={e => handleChange("maxPay", e.target.value)}
                    type="number"
                />

                <FormInput
                    label="Date From"
                    value={filters.dateFrom}
                    onChange={e => handleChange("dateFrom", e.target.value)}
                    type="date"
                />

                <FormInput
                    label="Date To"
                    value={filters.dateTo}
                    onChange={e => handleChange("dateTo", e.target.value)}
                    type="date"
                />

                <button className="filter-clear-btn" onClick={onClear}>
                    Clear Filters
                </button>
            </div>
        )}
       </div>
    );
}