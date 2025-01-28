import React from "react";

function DashboardPage({ message, errors, users }) {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-blue-500 text-white shadow-lg">
        <div className="container mx-auto p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Dashboard</h1>
          <button
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/";
            }}
            className="bg-red-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-red-700"
          >
            Logout
          </button>
        </div>
      </nav>
      <div className="container mx-auto p-4">
        <h2 className="text-2xl font-bold mb-4">Hi, {message}</h2>
        {errors && <p className="text-red-500">{errors}</p>}

        <div className="overflow-x-auto">
          <table className="table-auto w-full border-collapse border border-gray-300 bg-white rounded-lg shadow">
            <thead className="bg-gray-200">
              <tr>
                <th className="border border-gray-300 p-2 text-left">Name</th>
                <th className="border border-gray-300 p-2 text-left">Email</th>
                <th className="border border-gray-300 p-2 text-left">Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user._id} className="hover:bg-gray-100">
                  <td className="border border-gray-300 p-2">{user.name}</td>
                  <td className="border border-gray-300 p-2">{user.email}</td>
                  <td className="border border-gray-300 p-2">{user.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
