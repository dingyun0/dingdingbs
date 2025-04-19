export interface SessionOptionsResponse {
  code: number;
  message: string;
  data: {
    colleges: string[];
    majors: string[];
    grades: string[];
  };
}

export interface CollegeData {
  name: string;
  majors: string[];
}

// 添加课程列表响应类型
export interface CourseItem {
  course_id: string;
  course_name: string;
}

export interface FilteredCoursesResponse {
  code: number;
  message: string;
  data: CourseItem[];
}
