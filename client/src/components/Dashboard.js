import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardPage from "../pages/DashboardPage";

const Dashboard = () => {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      //redirect to login if no token is found
      navigate("/");
      return;
    }

    fetch("http://127.0.0.1:8000/dashboard/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`, 
    },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else if (response.status === 401) {
          throw new Error("Unauthorized: Token is invalid or expired");
        } else if (response.status === 403) {
          throw new Error("Access forbidden: Insufficient permissions");
        } else {
          throw new Error("An unknown error occurred");
        }
      })
      .then((data) => {
        setMessage(data.message);
      })
      .catch((err) => {
        console.error(err);
        setError("Something went wrong! Try again");
        localStorage.removeItem("token");
        navigate("/");
      });
  }, [navigate]);

  return (
    <div>
      <DashboardPage message={message} errors={error}/>
    </div>
  );
};

export default Dashboard;
