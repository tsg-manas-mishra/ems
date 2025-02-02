import React from "react";

const EmployeeModal = ({ employee, setEmployee, onSave, onClose }) => {
    const handleChange = (e) => {
        setEmployee({ ...employee, [e.target.name]: e.target.value });
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>{employee.email ? "Edit Employee" : "Add Employee"}</h2>
                <input name="name" placeholder="Name" value={employee.name} onChange={handleChange} />
                <input name="email" placeholder="Email" value={employee.email} onChange={handleChange} disabled={!!employee.email} />
                <input name="role" placeholder="Role" value={employee.role} onChange={handleChange} />
                <input name="department" placeholder="Department" value={employee.department} onChange={handleChange} />
                <input name="designation" placeholder="Designation" value={employee.designation} onChange={handleChange} />
                <input name="address" placeholder="Address" value={employee.address} onChange={handleChange} />
                <input name="contact" placeholder="Contact" value={employee.contact} onChange={handleChange} />
                <button onClick={onSave}>Save</button>
                <button onClick={onClose}>Cancel</button>
            </div>
        </div>
    );
};

export default EmployeeModal;
