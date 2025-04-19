import request from "@/utils/request";

export const getImageUrl = (formData: FormData) => {
  return request({
    url: "/image_url/upload",
    method: "post",
    data: formData,
  });
};
