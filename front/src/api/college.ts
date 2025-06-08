import request from "@/utils/request";

export const getCollegeList = () => {
  return request({
    url: "/college/get_college_list",
    method: "get",
  });
};

export const addCollegeReq = (data: any) => {
  return request({
    url: "/college/save_college",
    method: "post",
    data,
  });
};

export const updateCollegeReq = (data: any) => {
  return request({
    url: "/college/update_college",
    method: "put",
    data,
  });
};

export const deleteCollegeReq = (id: number) => {
  return request({
    url: `/college/delete_college/${id}`,
    method: "delete",
  });
};
