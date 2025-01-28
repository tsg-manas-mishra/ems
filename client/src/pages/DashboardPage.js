import React from "react";

function DashboardPage({message,errors}){
    return(
        <>
        <h1>Dashboard</h1>
       <h2>{message}</h2>
      {errors && <p style={{ color: "red" }}>{errors}</p>}
        </>
    )
}
export default DashboardPage