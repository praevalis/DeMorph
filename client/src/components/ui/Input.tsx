import type { CustomFormData } from '../../types/forms';

interface InputProps<T extends CustomFormData>
	extends React.InputHTMLAttributes<HTMLInputElement> {
	label: string;
	className?: string;
	inputName: keyof T;
	data: T;
	setData: React.Dispatch<React.SetStateAction<T>>;
	variant?: 'input' | 'textarea';
}

const Input = <T extends CustomFormData>({
	label,
	className,
	inputName,
	data,
	setData,
	variant = 'input',
	...defaultProps
}: InputProps<T>) => {
	const handleValueChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
	) => {
		const rawVal = e.target.value;
		const parsedVal =
			defaultProps.type === 'number'
				? rawVal === ''
					? ''
					: Number(rawVal)
				: rawVal;

		setData((prev: T) => ({ ...prev, [inputName]: parsedVal }));
	};

	const baseProps = {
		id: `${String(inputName)}`,
		name: String(inputName),
		placeholder: label,
		value: data[inputName] ?? '',
		onChange: handleValueChange,
		className: `border border-white p-3 outline-none font-kanit text-white placeholder:text-white focus:placeholder:opacity-50 rounded-xl ${
			className ?? ''
		}`,
	};

	if (variant === 'textarea') {
		const textareaProps: React.TextareaHTMLAttributes<HTMLTextAreaElement> =
			{
				...baseProps,
				...(defaultProps as unknown as React.TextareaHTMLAttributes<HTMLTextAreaElement>),
			};
		return <textarea {...textareaProps} />;
	}

	const inputProps: React.InputHTMLAttributes<HTMLInputElement> = {
		...baseProps,
		...defaultProps,
	};
	return <input {...inputProps} />;
};

export default Input;
