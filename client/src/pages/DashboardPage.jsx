import { useState } from "react";

const DashboardPage = ({ message, users, filteredUsers, success, handleDeleteEmployee, handleEditEmployee, isSearchActive, handleSort, notfound }) => {
  const role = localStorage.getItem("role");
  const email = localStorage.getItem("email");
  const [sortState, setSortState] = useState({ column: null, order: "default" });

  const displayedUsers = filteredUsers.length > 0 ? filteredUsers : users;

  const handleSortClick = (column) => {
    let newOrder = "asc"; // Default sorting order

    if (sortState.column === column) {
      // Toggle between 'asc', 'desc', and 'default'
      if (sortState.order === "asc") newOrder = "desc";
      else if (sortState.order === "desc") newOrder = "default";
    }

    setSortState({ column, order: newOrder });
    handleSort(column, newOrder); // Send sorting request to backend
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="p-4">
        {success && <p className="text-green-500">{success}</p>}
        {message && <h1 className="text-2xl font-bold mb-4">{message}</h1>}
        {role==="Employee" && <button className="mr-2 px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                          onClick={() => handleEditEmployee(email)}> Edit </button>}
        <div className="overflow-x-auto bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Users</h2>
          {notfound ? <p className="text-2xl mb-4">No Employees found</p> :
          <table className="min-w-full table-auto border-collapse border border-gray-300">
            <thead className="bg-gray-200">
              <tr>
                {["name", "email", "role", "department", "designation", "address", "contact"].map((column) => (
                  <th
                    key={column}
                    className="border px-4 py-2 text-left text-gray-600 cursor-pointer hover:bg-gray-300"
                    onClick={() => handleSortClick(column)}
                  >
                    {column.charAt(0).toUpperCase() + column.slice(1)}
                  </th>
                ))}
                {role === "Admin" && <th className="border px-4 py-2 text-left text-gray-600">Actions</th>}
              </tr>
            </thead>

            <tbody>
              {displayedUsers.length > 0 ? (
                displayedUsers.map((user, index) => (
                  <tr key={user._id || user.id || index} className="even:bg-gray-50 odd:bg-white">
                    <td className="border px-4 py-2">{user.name}</td>
                    <td className="border px-4 py-2">{user.email}</td>
                    <td className="border px-4 py-2">{user.role}</td>
                    <td className="border px-4 py-2">{user.department}</td>
                    <td className="border px-4 py-2">{user.designation}</td>
                    <td className="border px-4 py-2 truncate">{user.address}</td>
                    <td className="border px-4 py-2">{user.contact}</td>
                    {role === "Admin" && (
                      <td className="border px-4 py-2">
                        <button className="mr-2 px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                          onClick={() => handleEditEmployee(user.email)}> Edit </button>
                        <button className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                          onClick={() => handleDeleteEmployee(user.email)}> Delete </button>
                      </td>
                    )}
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-gray-500">
                    {isSearchActive ? "No Users Found." : "No Employees Available."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
