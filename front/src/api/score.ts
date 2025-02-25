import request from "@/utils/request";

export const saveScoreReq = (prama: any) => {
  console.log("API层发送数据:", JSON.stringify(prama, null, 2));
  return request({
    url: "/scores/save",
    method: "post",
    data: prama,
  });
};

export const getScoreAll = () => {
  return request({
    url: "/scores/all",
    method: "get",
  });
};
