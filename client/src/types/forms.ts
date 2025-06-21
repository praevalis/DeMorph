export interface CustomFormData {
	[key: string]: string | number | undefined;
}

export interface RegisterFormData extends CustomFormData {
	first_name: string;
	last_name?: string;
	username: string;
	email: string;
}

export interface LoginFormData extends CustomFormData {
	username: string;
	password: string;
}
