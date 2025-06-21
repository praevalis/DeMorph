import { useState } from 'react';
import { Link } from 'react-router-dom';

import type { RegisterFormData } from '../types/forms';

import Page from '../components/Page';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';

const SignUp = () => {
	const [regData, setRegData] = useState<RegisterFormData>({
		first_name: '',
		last_name: '',
		username: '',
		email: '',
	});

	return (
		<Page className='bg-black'>
			<div className='flex flex-col gap-10 w-full max-w-md px-4'>
				<h3 className='font-kaisei text-white text-2xl text-center'>
					Sign Up with DeMorph
				</h3>
				<div className='flex flex-col gap-6'>
					<div className='flex gap-4 w-full justify-between'>
						<Input
							label='FIRST NAME'
							inputName='first_name'
							data={regData}
							setData={setRegData}
							className='w-1/2'
						/>
						<Input
							label='LAST NAME'
							inputName='last_name'
							data={regData}
							setData={setRegData}
							className='w-1/2'
						/>
					</div>
					<div className='flex flex-col gap-6'>
						<Input
							label='USERNAME'
							inputName='username'
							data={regData}
							setData={setRegData}
						/>
						<Input
							label='EMAIL'
							inputName='email'
							data={regData}
							setData={setRegData}
						/>
					</div>
				</div>
				<Link to='/sign-in'>
					<p className='font-kanit text-ultra-moss hover:text-walk-park text-md md:text-lg'>
						Already a DeMorphian? Sign In.
					</p>
				</Link>
				<Button className='self-end'>SUBMIT</Button>
			</div>
		</Page>
	);
};

export default SignUp;
