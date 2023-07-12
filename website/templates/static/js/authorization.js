// Check if access token and refresh token are present in localStorage
const accessToken = localStorage.getItem('access_token');
const refreshToken = localStorage.getItem('refresh_token');

// Get the current page URL
const currentPageUrl = window.location.href;

if ((!accessToken || !refreshToken) && !currentPageUrl.includes('/login')) {
  // Access token or refresh token is missing and the current page is not the login page,
  // redirect to the login page
  window.location.href = loginUrl;
} else {
  // Function to check if the access token is expired
  function isAccessTokenExpired() {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      const [, payloadBase64] = accessToken.split('.');
      const payload = JSON.parse(atob(payloadBase64));
      const expirationTime = payload.exp * 1000; // Convert expiration time to milliseconds
      const currentTime = new Date().getTime();
      return currentTime >= expirationTime;
    }
    return true; // Access token is not set, consider it expired
  }

  // Check if access token is expired
  if (isAccessTokenExpired()) {
    // Access token is expired, renew it using the refresh token
    // Send a request to your Django backend to renew the access token
    // Example using fetch API:
    fetch('/api/user/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Retrieve the new access token and its expiration time
        const { access } = data;
        if (access) {
          // Update the access token and its expiration time in localStorage
          localStorage.setItem('access_token', access);
        } else {
          // Failed to renew the access token, redirect to the login page
          window.location.href = '/login';
        }
      })
      .catch((error) => {
        console.error('Error renewing access token:', error);
        // Failed to renew the access token, redirect to the login page
        window.location.href = '/login';
      });
  }
}
