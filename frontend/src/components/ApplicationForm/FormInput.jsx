export default function FormInput({
  label,
  value,
  onChange,
  type = "text",
  placeholder = "",
  required = false,
}) {
  return (
    <div className="form-field">
      <label>{label}</label>
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
      />
    </div>
  );
}
