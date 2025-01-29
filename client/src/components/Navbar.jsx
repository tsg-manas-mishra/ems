import React from "react";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  };

  return (
    <nav className="bg-blue-500 text-white shadow-md p-4">
      <div className="flex justify-between items-center max-w-7xl mx-auto">
        <h1 className="text-2xl font-semibold">Employee Management System</h1>
        <div className="flex items-center space-x-4">
          <button
            className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-medium rounded"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
