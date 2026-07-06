
export default function FormSelect ({label, value, onChange, options, required=false}) {
    return (
        <div>
            <label>{label}</label>
            <select
                value={value}
                onChange={onChange}
                required={required}
            >
                {options.map(option => (
                    <option key={option} value={option}>{option}</option>
                ))}
            </select>
        </div>
    )
}