export interface User {
  id: number;
  username: string;
  password: string;
  email: string;
  phone: string;
  sno: string | null;
  roles: string[];
  date: string;
}

export interface Register {
  username: string;
  password: string;
  confirmPassword: string;
  sno: string;
}

export interface Login {
  username: string;
  password: string;
}
