import request from "@/utils/request";
import {
  SessionOptionsResponse,
  FilteredCoursesResponse,
} from "@/types/session";

export const saveSessionReq = (data: any) => {
  return request({
    url: "/sessions/saveSession",
    method: "post",
    data,
  });
};
export const getSessionAll = () => {
  return request({
    url: "/sessions/allSession",
    method: "get",
  });
};

// 获取课程选项
export const getSessionOptionsReq = (): Promise<SessionOptionsResponse> => {
  return request({
    url: "/sessions/options",
    method: "get",
  }).then((response) => response.data);
};

export const getFilteredCoursesReq = (params: {
  department: string;
  major: string;
  grade: string;
}) => {
  return request<FilteredCoursesResponse>({
    url: "/sessions/filtered-courses",
    method: "get",
    params: params,
  });
};
