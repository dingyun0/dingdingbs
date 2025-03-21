import request from "@/utils/request";

export function addActivityReq(data: any) {
  return request({
    url: "/activity/addActivity",
    method: "post",
    data: data,
  });
}

export function updateActivityReq(data: any) {
  return request({
    url: "/activity/updateActivity",
    method: "put",
    data: data,
  });
}

export function deleteActivityReq(id: number) {
  return request({
    url: `/activity/delete/${id}`,
    method: "delete",
  });
}

export function getActivityListReq(params: {
  page: number;
  page_size: number;
}) {
  return request({
    url: "/activity/activityList",
    method: "get",
    params,
  });
}

export function applyActivityReq(data: any) {
  return request({
    url: "/activity/applyActivity",
    method: "post",
    data: data,
  });
}
