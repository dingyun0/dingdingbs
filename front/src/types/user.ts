export interface User {
  id: number;
  username: string;
  password: string;
  email: string;
  phone: string;
  roles: string[];
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
