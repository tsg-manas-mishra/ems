import React from "react";

const DashboardPage = ({ message, errors, users, success, handleDeleteEmployee, handleEditEmployee }) => {
  const role = localStorage.getItem("role"); // Get the role from localStorage

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="p-4">
        {errors && <p className="text-red-500">{errors}</p>}
        {success && <p className="text-green-500">{success}</p>}
        {message && <h1 className="text-2xl font-bold mb-4">{message}</h1>}

        <div className="overflow-x-auto bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Users</h2>
          <table className="min-w-full table-auto border-collapse border border-gray-300">
            <thead className="bg-gray-200">
              <tr>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Name</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Email</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Type</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Department</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Designation</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Address</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">Phone</th>
                <th className="border border-gray-300 px-4 py-2 text-left text-gray-600">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {users.length > 0 ? (
                users.map((user) => (
                  <tr
                    key={user._id}
                    className="even:bg-gray-50 odd:bg-white"
                  >
                    <td className="border border-gray-300 px-4 py-2">{user.name}</td>
                    <td className="border border-gray-300 px-4 py-2">{user.email}</td>
                    <td className="border border-gray-300 px-4 py-2">{user.role}</td>
                    <td className="border border-gray-300 px-4 py-2">{user.department}</td>
                    <td className="border border-gray-300 px-4 py-2">{user.designation}</td>
                    <td className="border border-gray-300 px-4 py-2 truncate">{user.address}</td>
                    <td className="border border-gray-300 px-4 py-2">{user.contact}</td>
                    <td className="border border-gray-300 px-4 py-2">
                      {/* Edit Button */}
                      {(role === "Admin" || localStorage.getItem("email") === user.email) && (
                        <button
                          className="mr-2 px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                          onClick={() => handleEditEmployee(user.email)}
                        >
                          Edit
                        </button>
                      )}

                      {/* Delete Button (Admin Only) */}
                      {role === "Admin" && (
                        <button
                          className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                          onClick={() => handleDeleteEmployee(user.email)}
                        >
                          Delete
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-gray-500">
                    No users found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
