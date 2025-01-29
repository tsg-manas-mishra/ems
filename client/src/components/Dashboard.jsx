import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { fetchDashboardData, fetchUsers } from "../services/userService";
import DashboardPage from "../pages/DashboardPage";

const Dashboard = () => {
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [newEmployee, setNewEmployee] = useState({
    name: "",
    email: "",
    role: "",
    department: "",
    designation: "",
    address: "",
    contact: "",
  });
  const [success,setSuccess] = useState("");
  const navigate = useNavigate();
  const role = localStorage.getItem("role");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    fetchDashboardData(token)
      .then((data) => setMessage(data.message))
      .catch((err) => {
        setError(err.message);
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("email");
        navigate("/");
      });

    fetchUsers(token)
      .then((data) => setUsers(data))
      .catch((err) => {
        setError(err.message);
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("email");
        navigate("/");
      });
  }, [navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEmployee({ ...newEmployee, [name]: value });
  };

  const handleDeleteEmployee = (id) => {
    const token = localStorage.getItem("token");
  
    const confirmDelete = window.confirm("Are you sure you want to delete this employee?");
    if (!confirmDelete) return;
  
    fetch(`http://127.0.0.1:8000/delete-employee/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to delete employee");
        }
        return response.json();
      })
      .then(() => {
        return fetch("http://127.0.0.1:8000/users", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch updated users");
        }
        return response.json();
      })
      .then((updatedUsers) => {
        setUsers(updatedUsers);
        setSuccess("Employee Deleted Successfully");
        setTimeout(() => {
          setSuccess("");
        }, 3000); // Clear success message after 3 seconds
      })
      .catch((err) => {
        setError(err.message);
      });
  };
  
  
  const handleSaveEmployee = () => {
    const token = localStorage.getItem("token");
    const endpoint = isEdit
      ? `http://127.0.0.1:8000/employees/${selectedEmployee.email}`
      : "http://127.0.0.1:8000/add";
  
    fetch(endpoint, {
      method: isEdit ? "PUT" : "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(newEmployee),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(isEdit ? "Failed to edit employee" : "Failed to add employee");
        }
        setSuccess(isEdit ? "Employee Data edited successfully" : "Employee Added Successfully");
        return response.json();
      })
      .then(() => {
        return fetch("http://127.0.0.1:8000/users", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch updated users");
        }
        return response.json();
      })
      .then((updatedUsers) => {
        setUsers(updatedUsers);
        setShowModal(false);
        setNewEmployee({
          name: "",
          password: "",
          email: "", // Ensure email is empty when adding
          role: "",
          department: "",
          designation: "",
          address: "",
          contact: "",
        });
      })
      .catch((err) => {
        setError(err.message);
      });
  };
  
  const handleEditEmployee = (email) => {
    const employee = users.find((user) => user.email === email);
    setSelectedEmployee(employee);
    setIsEdit(true);
    setNewEmployee(employee); // Prefill modal with selected employee data
    setShowModal(true);
  };
  
  return (
    <div>
      <Navbar />
      <div className="p-4">
        {role === "Admin" && (
          <button
            className="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => {
              setIsEdit(false);
              setNewEmployee({
                name: "",
                password: "",
                email: "", // Ensure email is empty for new employees
                role: "",
                department: "",
                designation: "",
                address: "",
                contact: "",
              });
              setShowModal(true);
            }}
          >
            Add Employee
          </button>
        )}
  
        <DashboardPage
          message={message}
          errors={error}
          users={users}
          success={success}
          handleDeleteEmployee={handleDeleteEmployee}
          handleEditEmployee={handleEditEmployee}
        />
  
        {showModal && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-md w-96">
              <h2 className="text-xl font-semibold mb-4">
                {isEdit ? "Edit Employee" : "Add Employee"}
              </h2>
              <form>
                {[
                  { label: "Email", name: "email", type: "email", disabled: isEdit }, // Always disabled
                  { label: "Name", name: "name", type: "text", disabled: role !== "Admin" && isEdit },
                  { label: "Password", name: "password", type: "password", disabled: role !== "Admin" },
                  { label: "Role", name: "role", type: "text", disabled: role !== "Admin" && isEdit },
                  { label: "Department", name: "department", type: "text", disabled: role !== "Admin" && isEdit },
                  { label: "Designation", name: "designation", type: "text", disabled: role !== "Admin" && isEdit },
                  { label: "Address", name: "address", type: "text", disabled: false },
                  { label: "Phone", name: "contact", type: "tel", disabled: false },
                ].map(({ label, name, type, disabled }) => (
                  <div key={name} className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                      {label}
                    </label>
                    <input
                      type={type}
                      name={name}
                      value={newEmployee[name] || ""}
                      onChange={handleInputChange}
                      disabled={disabled}
                      className={`mt-1 p-2 w-full border border-gray-300 rounded ${
                        disabled ? "bg-gray-200 cursor-not-allowed" : ""
                      }`}
                    />
                  </div>
                ))}
              </form>
              <div className="flex justify-end space-x-4">
                <button
                  className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                  onClick={handleSaveEmployee}
                >
                  {isEdit ? "Save Changes" : "Add Employee"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
  };
  
  export default Dashboard;
  