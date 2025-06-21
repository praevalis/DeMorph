import { useState } from 'react';
import { Link } from 'react-router-dom';

import type { LoginFormData } from '../types/forms';

import Page from '../components/Page';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const SignIn = () => {
	const [loginData, setLoginData] = useState<LoginFormData>({
		username: '',
		password: '',
	});

	return (
		<Page className='bg-black'>
			<div className='flex flex-col gap-10 w-full max-w-md px-4'>
				<h3 className='font-kaisei text-white text-2xl text-center'>
					Sign In to DeMorph
				</h3>
				<div className='flex flex-col gap-6'>
					<Input
						label='USERNAME'
						inputName='username'
						data={loginData}
						setData={setLoginData}
					/>
					<Input
						label='PASSWORD'
						inputName='password'
						data={loginData}
						setData={setLoginData}
					/>
				</div>
				<Link to='/sign-up'>
					<p className='font-kanit text-ultra-moss hover:text-walk-park text-md md:text-lg'>
						Not a DeMorphian? Sign Up.
					</p>
				</Link>
				<Button className='self-end'>SUBMIT</Button>
			</div>
		</Page>
	);
};

export default SignIn;
