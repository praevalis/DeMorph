import { useState } from 'react';
import { GoHome } from 'react-icons/go';
import { IoMenuSharp } from 'react-icons/io5';
import { MdLogin, MdLogout } from 'react-icons/md';
import { Link, useLocation } from 'react-router-dom';

import type { NavLink } from '../types/constants';

import { handleLogout } from '../utils/helpers';
import { useAuth } from '../context/AuthContext';

const Navbar = ({ links }: { links: NavLink[] }) => {
	const { authenticated } = useAuth();
	const [mobileNav, setMobileNav] = useState(false);
	const { pathname } = useLocation();

	const toggleMobileNav = () => {
		setMobileNav((prev) => !prev);
	};

	const scrollIntoView = (linkText: string) => {
		const sectionId = `#${linkText.toLowerCase()}`;
		const sectionNode = document.querySelector(sectionId);

		if (!sectionNode) return;

		sectionNode.scrollIntoView({
			behavior: 'smooth',
			block: 'nearest',
			inline: 'center',
		});
	};

	return (
		<nav className='flex flex-row lg:flex-col lg:gap-6 items-center justify-between w-full lg:w-[80vw] px-4 lg:px-[10vw] py-3 lg:mx-auto bg-black'>
			<IoMenuSharp
				aria-label={`${mobileNav ? 'Close' : 'Open'} Navbar`}
				onClick={toggleMobileNav}
				className='lg:hidden text-white w-[25px] h-[25px]'
			/>

			<h3 className='font-pirata-one text-gray-200 text-center text-lg md:text-2xl'>
				DeMorph
			</h3>

			<div className='flex lg:w-full items-center justify-between'>
				<Link to='/'>
					<GoHome
						aria-label='Home'
						className='text-white hover:text-walk-park transition-colors w-[25px] h-[25px]'
					/>
				</Link>

				<ul
					className={`flex-col lg:flex-row gap-3 lg:gap-7 items-start justify-between absolute top-14 left-4 lg:static ${
						mobileNav ? 'flex' : 'hidden lg:flex'
					} font-kaisei text-white text-sm lg:text-md transform translate-y duration-300 transition-all z-20`}
				>
					{links.map((link, idx) => (
						<li key={idx} className='hover:text-ultra-moss'>
							<Link
								to={link.href}
								onClick={(e) => {
									if (link.href.startsWith('#')) {
										e.preventDefault();
										scrollIntoView(link.text);
									}
								}}
								className={`${
									pathname === link.href ? 'text-red-700' : ''
								}`}
							>
								{link.text}
							</Link>
						</li>
					))}
				</ul>

				{authenticated ? (
					<MdLogout
						onClick={handleLogout}
						aria-label='sign out'
						className='text-white hover:text-walk-park transition-colors w-[25px] h-[25px]'
					/>
				) : (
					<Link to='/sign-in'>
						<MdLogin
							aria-label='sign in'
							className='text-white hover:text-walk-park transition-colors w-[25px] h-[25px]'
						/>
					</Link>
				)}
			</div>
		</nav>
	);
};

export default Navbar;
