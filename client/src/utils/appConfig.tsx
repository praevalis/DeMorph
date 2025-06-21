import Home from '../pages/Home';
import Error from '../pages/Error';
import SignUp from '../pages/SignUp';
import SignIn from '../pages/SignIn';

export const routes = [
	{
		path: '/',
		element: <Home />,
		errorElement: <Error />,
	},
	{
		path: '/sign-up',
		element: <SignUp />,
	},
	{
		path: '/sign-in',
		element: <SignIn />,
	},
];
