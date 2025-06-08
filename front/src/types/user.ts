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
  department: string;
  major: string;
  grade: string;
  class_name: string;
}

export interface Login {
  username: string;
  password: string;
}
