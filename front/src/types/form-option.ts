export interface FormOption {
  list: FormOptionList[];
  labelWidth?: number | string;
  span?: number;
  change?: any;
}

export interface FormOptionList {
  prop: string;
  label: string;
  type: string;
  options?: Array<{ label: string; value: string }>;
  placeholder?: string;
  disabled?: boolean;
  opts?: any[];
  format?: string;
  activeValue?: any;
  inactiveValue?: any;
  activeText?: string;
  inactiveText?: string;
  required?: boolean;
  change?: (value: any) => void; // 添加这一行
}
