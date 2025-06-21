const Section = ({
	id,
	children,
	className,
}: {
	id: string;
	children: React.ReactNode;
	className?: string;
}) => {
	return (
		<section id={id} className={`${className} w-[80vw] px-[5vw] mx-auto`}>
			{children}
		</section>
	);
};

export default Section;
