const BASEURL=process.env.REACT_APP_API_URL;


export const searchUsers = async (field, value) => {
    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Authorization error: No token provided.");
    }

    try {
        const response = await fetch(`${BASEURL}/search-employee/?${field}=${(value)}`, {
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
