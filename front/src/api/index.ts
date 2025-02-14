import request from "../utils/request";

export const loginReq = (loginInfo: any) => {
  console.log("loginInfo:", loginInfo);
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

// 获取所有用户信息
export const userAllInfoReq = (params: any) => {
  return request({
    url: "/users/getAllInfo",
    method: "get",
    params: params,
  });
};

// 用户管理相关接口
export const addUserReq = (data: any) => {
  return request({
    url: "/user/register",
    method: "post",
    data,
  });
};

export const updateUserReq = (data: any) => {
  return request({
    url: "/user/update",
    method: "put",
    data,
  });
};

export const deleteUserReq = (id: number) => {
  return request({
    url: `/users/${id}`,
    method: "delete",
  });
};

export const getUserDetailReq = (id: string) => {
  return request({
    url: `/user/detail/${id}`,
    method: "get",
  });
};

// 添加更新用户角色的API
export const updateUserRoleReq = (data: { id: number; roles: string }) => {
  return request({
    url: "/users/update",
    method: "put",
    data,
  });
};
