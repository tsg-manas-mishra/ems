const BASEURL=process.env.REACT_APP_API_URL;
export const fetchDashboardData = async (token) => {
    if (!token) {
        console.error("Token is missing. Please log in.");
        return null;
    }

    try {
        const response = await fetch(`${BASEURL}/dashboard/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            if (response.status === 401) throw new Error("Unauthorized: Token expired or invalid");
            if (response.status === 403) throw new Error("Forbidden: Insufficient permissions");
            throw new Error("Failed to fetch dashboard data");
        }

        const dashboardData = await response.json();
        return dashboardData;
    } catch (error) {
        console.error("Error fetching dashboard data:", error.message);
        return null;
    }
};
