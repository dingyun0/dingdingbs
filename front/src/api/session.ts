import request from "@/utils/request";

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
