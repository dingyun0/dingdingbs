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

export function getReviewListReq() {
  return request({
    url: "/activity/getReviewActivity",
    method: "get",
  });
}

export function reviewActivity(data: any) {
  return request({
    url: "/activity/handleReviewActivity",
    method: "post",
    data: data,
  });
}

export function getReviewMessageReq(data: any) {
  return request({
    url: "/activity/getReviewMessage",
    method: "get",
    data: data,
  });
}

// 获取审核消息
export function getReviewMessage(student_sno: string) {
  return request({
    url: "/activity/getReviewMessage",
    method: "get",
    params: { student_sno },
  });
}
