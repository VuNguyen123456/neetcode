function AccountForm() {
    const [formData, setFormData] = useState({
        name: '',
        balance: '',
        isActivate: false,
    });

    // a handler that handle change when form data is changed (usually through a button)
    function handleChange(e) {
        const {name, value, type, checked} = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value,
        }));
    }

    // a handler that handle the submit
    function handleSumit(e) {
        e.preventDefault(); // stops the browser from doing a full page reload
        console.log(formData);
    }

    return(
        <form onSubmit={handleSubmit}>
            <input
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Account name"
            />
            <input
                name="balance"
                type="number"
                value={formData.balance}
                onChange={handleChange}
                placeholder="Balance"
            />
            <label>
                <input
                name="isActive"
                type="checkbox"
                checked={formData.isActive}
                onChange={handleChange}
                />
                Active
            </label>
            <button type="submit">Save</button>
        </form>
    );
}