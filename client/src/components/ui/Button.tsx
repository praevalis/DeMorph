interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
	className?: string;
	children: React.ReactNode;
	color?: 'primary' | 'secondary';
}

const Button = ({
	className,
	children,
	color = 'primary',
	...defaultProps
}: ButtonProps) => {
	const colorMap = {
		primary: `
        bg-wet-concrete border-ultra-moss text-ultra-moss hover:bg-ultra-moss 
        hover:text-wet-concrete hover:shadow-[0_0_30px_theme('colors.ultra-moss')]
        active:bg-ultra-moss active:shadow-none
        `,
		secondary: `
		bg-wet-concrete border-white text-white hover:bg-gray-200 
        hover:text-wet-concrete hover:shadow-[0_0_30px_theme('colors.white')] 
        active:bg-gray-400 active:shadow-none
        `,
	};

	const colorClass = colorMap[color];

	return (
		<button
			type={defaultProps.type ?? 'button'}
			aria-label={
				typeof children === 'string'
					? children
					: defaultProps['aria-label']
			}
			className={`flex px-6 py-2 w-fit rounded-xl border font-kanit transition-all duration-200 ${colorClass} ${
				className ?? ''
			} disabled:opacity-50 disabled:cursor-not-allowed`}
			{...defaultProps}
		>
			{children}
		</button>
	);
};

export default Button;
