import request from "@/utils/request";

export function addAnnouncementReq(data: any) {
  return request({
    url: "/announcement/add",
    method: "post",
    data,
  });
}
export function updateAnnouncementReq(data: any) {
  return request({
    url: "/announcement/update",
    method: "put",
    data,
  });
}

export function deleteAnnouncementReq(id: number) {
  return request({
    url: `/announcement/delete/${id}`,
    method: "delete",
  });
}

export function getAnnouncementListReq(params: {
  page: number;
  page_size: number;
}) {
  return request({
    url: "/announcement/list",
    method: "get",
    params,
  });
}
