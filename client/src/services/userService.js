export const fetchDashboardData = async (token) => {
    const response = await fetch("http://127.0.0.1:8000/dashboard/", {
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
  
    return response.json();
  };
  
  export const fetchUsers = async (token) => {
    const response = await fetch("http://127.0.0.1:8000/users/", {
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
  
    return response.json();
  };
  