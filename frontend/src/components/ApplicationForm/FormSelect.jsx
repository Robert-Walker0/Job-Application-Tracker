export default function FormSelect({
  label,
  value,
  onChange,
  options,
  required = false,
}) {
  return (
    <div className="form-field">
      <label>{label}</label>
      <select value={value} onChange={onChange} required={required}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}
