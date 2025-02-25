import request from "@/utils/request";

export const saveComprehensiveTestReq = (data: any) => {
  return request({
    url: "/comprehensive-tests/save",
    method: "post",
    data,
  });
};

export const getComprehensiveTestAll = () => {
  return request({
    url: "/comprehensive-tests/all",
    method: "get",
  });
};
