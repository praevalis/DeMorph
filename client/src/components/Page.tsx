import Navbar from './Navbar';
import Footer from './Footer';
import { navLinks } from '../utils/textConstants';

const Page = ({
	children,
	className,
}: {
	children: React.ReactNode;
	className?: string;
}) => {
	return (
		<div
			className={`${className} flex flex-col justify-between items-center min-h-screen`}
		>
			<Navbar links={navLinks} />

			{children}

			<Footer />
		</div>
	);
};

export default Page;
