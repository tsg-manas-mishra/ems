const API_URL = "http://127.0.0.1:8000";

export const searchUsers = async (field, value) => {
    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Authorization error: No token provided.");
    }

    try {
        const response = await fetch(`${API_URL}/search-employee/?${field}=${(value)}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            return errorData;
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error(error.message);
        throw error;
    }
};
