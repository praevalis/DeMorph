import { createContext, useContext, useState, useEffect } from 'react';

import type { User } from '../types/api';

interface AuthContextType {
	user: User | null;
	setUser: React.Dispatch<React.SetStateAction<User | null>>;
	authenticated: boolean;
	setAuthenticated: React.Dispatch<React.SetStateAction<boolean>>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
	const [user, setUser] = useState<User | null>(null);
	const [authenticated, setAuthenticated] = useState<boolean>(false);

	useEffect(() => {
		const authToken = localStorage.getItem('auth_token');
		setAuthenticated(!!authToken);
	}, []);

	return (
		<AuthContext.Provider
			value={{ user, setUser, authenticated, setAuthenticated }}
		>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const context = useContext(AuthContext);
	if (!context) {
		throw new Error('useAuth must be used inside AuthProvider.');
	}

	return context;
};
