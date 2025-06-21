import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import '@fontsource/kaisei-decol/index.css';
import '@fontsource/pirata-one/index.css';
import '@fontsource/kanit/index.css';
import './index.css';

import { routes } from './utils/appConfig';
import { AuthProvider } from './context/AuthContext';

const App = () => {
	return (
		<AuthProvider>
			<RouterProvider router={createBrowserRouter(routes)} />
		</AuthProvider>
	);
};

createRoot(document.getElementById('root')!).render(
	<StrictMode>
		<App />
	</StrictMode>,
);
