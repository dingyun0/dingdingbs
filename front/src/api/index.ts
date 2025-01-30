import request from "../utils/request";

export const loginReq = (loginInfo: any) => {
  return request({
    url: "/auth/login",
    method: "post",
    data: loginInfo,
  });
};

export const userInfoReq = () => {
  return request({
    url: "/users/getInfo",
    method: "get",
  });
};
export const getRouterReq = () => {
  return request({
    url: "/users/getRoutes",
    method: "get",
  });
};

export const registerReq = (registerInfo: any) => {
  return request({
    url: "/users/register",
    method: "post",
    data: registerInfo,
  });
};
