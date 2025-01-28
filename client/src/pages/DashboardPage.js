import React from "react";

function DashboardPage({message,errors,users}){
    return(
        <>
       <h2>Hi, {message}</h2>
      {errors && <p style={{ color: "red" }}>{errors}</p>}
      <table border="1" style={{ width: "100%", marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user._id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
        </>
    )
}
export default DashboardPage