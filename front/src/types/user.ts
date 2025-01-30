export interface User {
  id: number;
  name: string;
  password: string;
  email: string;
  phone: string;
  role: string;
  date: string;
}

export interface Register {
  username: string;
  password: string;
  confirmPassword: string;
}

export interface Login {
  username: string;
  password: string;
}
