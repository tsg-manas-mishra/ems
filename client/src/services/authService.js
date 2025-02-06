const BASEURL=process.env.REACT_APP_API_URL;
export const login = async (email, password) => {
    const response = await fetch(`${BASEURL}/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }
    return response.json();
};