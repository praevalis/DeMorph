import { useState } from 'react';

interface FileInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
	files: FileList | null;
	setFiles: React.Dispatch<React.SetStateAction<FileList | null>>;
	className?: string;
}

const FileInput = ({
	setFiles,
	className,
	...defaultProps
}: FileInputProps) => {
	const [isDragging, setIsDragging] = useState(false);

	const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
		setIsDragging(true);
	};

	const handleDragLeave = () => {
		setIsDragging(false);
	};

	const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
		setIsDragging(false);
		if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
			setFiles(e.dataTransfer.files);
			e.dataTransfer.clearData();
		}
	};

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setFiles(e.target.files ?? null);
	};

	return (
		<div
			onDrop={handleDrop}
			onDragOver={handleDragOver}
			onDragLeave={handleDragLeave}
			className={`${className ?? ''} ${isDragging ? '' : ''}`}
		>
			<input
				type='file'
				onChange={handleChange}
				className=''
				{...defaultProps}
			/>
		</div>
	);
};

export default FileInput;
