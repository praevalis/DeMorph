export const handleLogout = () => {
	localStorage.removeItem('auth_token');
	localStorage.removeItem('refresh_token');
};
