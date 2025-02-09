import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { fetchDashboardData } from "../services/userService";
import DashboardPage from "../pages/DashboardPage";
import SearchBar from "./Searchbar";
import { searchUsers } from "../services/api";
const BASEURL=process.env.REACT_APP_API_URL;
const fetchUsers = async () => { 
  const token = localStorage.getItem("token");
  if (!token) {
      console.error("Token is missing. Please log in.");
      localStorage.clear();
      window.location.href = "/";
      return [];
  }

  try {
      const response = await fetch(`${BASEURL}/users/`, {
          method: "GET",
          headers: {
              Authorization: `Bearer ${token}`,
          },
      });

      if (!response.ok) {
          if (response.status === 401) throw new Error("Unauthorized: Token expired or invalid");
          if (response.status === 403) throw new Error("Forbidden: Insufficient permissions");
          throw new Error("An unknown error occurred");
      }

      const data = await response.json();

      return data || [];  
  } catch (error) {
      console.error("Error fetching users:", error.message);
      return [];
  }
};




const Dashboard = () => {
  const [message, setMessage] = useState("");
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [errors, setErrors] = useState("");
  const [users, setUsers] = useState([]);
  const [numcheck, setNumcheck] = useState("");
  const [notfound,setNotfound] = useState(false);
  const [emailCheck, setEmailcheck] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [isSearchActive,setActive] = useState(0);
  const [isEdit, setIsEdit] = useState(false);
  const [isDataUpdated, setIsDataUpdated] = useState(false);
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
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();
  const role = localStorage.getItem("role"); 

  const loadUsers = async () => {
    try {
        const usersData = await fetchUsers();
        setUsers(usersData);
    } catch (error) {
        console.error("Error fetching users:", error);
        setErrors(error.message);
    }
};


  useEffect(() => {
    const token = localStorage.getItem("token");
    const name = localStorage.getItem("name");
    if (!token) {
        navigate("/");
        return;
    }

    fetchDashboardData(token)
        .then(() => setMessage(`Welcome, ${name}`))
        .catch((err) => {
            setErrors(err.message);
            localStorage.clear();
            navigate("/");
        });

    loadUsers();
}, [navigate, isDataUpdated]);


  //adding data on form
  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Update employee details dynamically
    setNewEmployee((prev) => ({ ...prev, [name]: value }));

    // Clear specific error messages when the input becomes valid
    if (name === "email") {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      setEmailcheck(
        emailPattern.test(value) ? "" : "Please enter a valid email address"
      );
    }
    if (name === "contact") {
      const phonePattern = /^\d{10,}$/;
      setNumcheck(
        phonePattern.test(value)
          ? ""
          : "Please enter a valid 10-digit phone number."
      );
    }
    if (value.trim() !== "") {
      setErrors(""); // Remove the general "All fields are required" error when user starts typing
    }
  };

  //for sorting
  const handleSort = async (column, order) => {
    if (order === "default") {
      loadUsers(); // Reset to original data
      return;
    }
  
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("Token missing. Please log in.");
      return;
    }
  
    try {
      const response = await fetch(`${BASEURL}/users?column=${column}&order=${order}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        throw new Error("Failed to fetch sorted users");
      }
  
      const sortedUsers = await response.json();
      setUsers(sortedUsers);
    } catch (error) {
      console.error("Error sorting users:", error.message);
    }
  };
  

  const handleSearch = async (field, value) => {
    try {
        if (!value.trim()) {
            setNotfound(false);
            await loadUsers();
            setFilteredUsers([]);
            setActive(false);
            return;
        }

        const data = await searchUsers(field, value);
        if(data?.employees?.length===0){
          setNotfound(true);
          return;
        }
        setNotfound(false);
        if (data?.employees?.length > 0) {
            setFilteredUsers(data.employees);
            setActive(true);
        } else {
            setFilteredUsers([]);
            setActive(true);
        }
    } catch (err) {
        setFilteredUsers([]);
        setActive(true);
    }
};


  const handleDeleteEmployee = (id) => {
    const token = localStorage.getItem("token");

    const confirmDelete = window.confirm(
      `Are you sure you want to delete employee ${id}?`
    );
    if (!confirmDelete) return;

    fetch(`${BASEURL}/delete-employee/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          setErrors("Failed to delete the Employee");
        }
        return response.json();
      })
      .then(() => {
        return fetch(`${BASEURL}/users`, {
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
        setTimeout(()=>setSuccess(""),3000);
      })
      .catch((err) => {
        setErrors("Try again");
        throw new Error("Try again")
      });
  };

  const handleSaveEmployee = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setErrors("Session expired. Please log in again.");
      localStorage.clear();
      navigate("/");
      return;
    }

    // Validate required fields
    if (
      !newEmployee.email ||
      !newEmployee.name ||
      !newEmployee.role ||
      !newEmployee.department ||
      !newEmployee.designation ||
      !newEmployee.address ||
      !newEmployee.contact
    ) {
      setErrors("All fields are required. Please fill them out.");
      return;
    }

    // Email Validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(newEmployee.email)) {
      setEmailcheck("Please enter a valid email address.");
      return;
    } else {
      setEmailcheck(""); // Clear error if valid
    }

    // Phone Number Validation (10-digit numbers only)
    const phonePattern = /^\d{10}$/;
    if (!phonePattern.test(newEmployee.contact)) {
      setNumcheck("Please enter a valid 10-digit phone number.");
      return;
    } else {
      setNumcheck(""); // Clear error if valid
    }

    // Prepare employee data
    const updatedEmployee = {
      email: newEmployee.email,
      name: newEmployee.name,
      password: newEmployee.password,
      role: newEmployee.role,
      department: newEmployee.department,
      designation: newEmployee.designation,
      address: newEmployee.address,
      contact: newEmployee.contact,
    };

    const endpoint = isEdit
      ? `${BASEURL}/edit-employee/${selectedEmployee.email}`
      : `${BASEURL}/add`;

    try {
      const response = await fetch(endpoint, {
        method: isEdit ? "PUT" : "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updatedEmployee),
      });

      if (!response.ok) {
        if (response.status === 422) {
          setErrors("Please fill out all the fields correctly.");
          return;
        }
        setErrors("Failed to save employee. Please log in and try again");
        return;
      }

      await response.json();
      await loadUsers();

      setSuccess(
        isEdit
          ? "Employee Data edited successfully"
          : "Employee Added Successfully"
      );
      handleCloseModal();
      setTimeout(()=>setSuccess(""),3000);
    } catch (err) {
      setErrors("An unexpected error occurred. Please try again.");
    }
  };

  const handleEditEmployee = (email) => {
    setSelectedEmployee(null);
    const employee = users.find((user) => user.email === email);

    if (!employee) {
      return;
    }

    setSelectedEmployee(employee);
    setIsEdit(true);
    setNewEmployee(employee);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setIsEdit(false);
    setSelectedEmployee(null);
    setNewEmployee({
      name: "",
      password: "",
      email: "",
      role: "",
      department: "",
      designation: "",
      address: "",
      contact: "",
    });
    setErrors("");
    setIsDataUpdated(false);
  };

  return (
    <div>
      <Navbar />
      <SearchBar onSearch={handleSearch} />

      <div className="p-4">
        {role === "Admin" && (
          <button
            className="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => {
              setIsEdit(false);
              setNewEmployee({
                name: "",
                password: "",
                email: "",
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
          users={users}
          success={success}
          handleDeleteEmployee={handleDeleteEmployee}
          handleEditEmployee={handleEditEmployee}
          filteredUsers={filteredUsers}
          isSearchActive = {isSearchActive}
          handleSort={handleSort}
          notfound = {notfound}
        />

        {showModal && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-md w-96">
              <h2 className="text-xl font-semibold mb-4">
                {isEdit ? "Edit Employee" : "Add Employee"}
              </h2>
              <form>
                {[
                  {
                    label: "Email",
                    name: "email",
                    type: "email",
                    disabled: isEdit,
                  },
                  {
                    label: "Name",
                    name: "name",
                    type: "text",
                    disabled: role !== "Admin" && isEdit,
                  },
                  {
                    label: "Password",
                    name: "password",
                    type: "password",
                    disabled: true && isEdit,
                  },
                  {
                    label: "Role",
                    name: "role",
                    type: "text",
                    disabled: role !== "Admin" && isEdit,
                  },
                  {
                    label: "Department",
                    name: "department",
                    type: "text",
                    disabled: role !== "Admin" && isEdit,
                  },
                  {
                    label: "Designation",
                    name: "designation",
                    type: "text",
                    disabled: role !== "Admin" && isEdit,
                  },
                  {
                    label: "Address",
                    name: "address",
                    type: "text",
                    disabled: false,
                  },
                  {
                    label: "Phone",
                    name: "contact",
                    type: "tel",
                    disabled: false,
                  },
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
                      required={true}
                      disabled={disabled}
                      className={`mt-1 p-2 w-full border border-gray-300 rounded ${
                        disabled ? "bg-gray-200 cursor-not-allowed" : ""
                      }`}
                    />
                  </div>
                ))}
              </form>
              <span>{errors && <p className="text-red-500">{errors}</p>}</span>
              <span>
                {emailCheck && <p className="text-red-500">{emailCheck}</p>}
              </span>
              <span>
                {numcheck && <p className="text-red-500">{numcheck}</p>}
              </span>

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