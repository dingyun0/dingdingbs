import request from "@/utils/request";

export const saveScoreReq = (prama: any) => {
  console.log("API层发送数据:", JSON.stringify(prama, null, 2));
  return request({
    url: "/scores/save",
    method: "post",
    data: prama,
  });
};

export const getScoreAll = (data: any) => {
  return request({
    url: "/scores/all",
    method: "get",
    data: data,
  });
};

export const getRecordedClassesReq = () => {
  return request({
    url: "/scores/recorded-classes",
    method: "get",
  });
};

export const getInputtedCollege = () => {
  return request({
    url: "/scores/inputted-college",
    method: "get",
  });
};

export const getScoreReviewReq = (data: any) => {
  return request({
    url: "/scores/review_score",
    method: "post",
    data: data,
  });
};

export const getScoreReviewList = () => {
  return request({
    url: "/scores/get_review_score_list",
    method: "get",
  });
};

export const submitScoreReviewResult = (data: any) => {
  return request({
    url: "/scores/submit_score_review_result",
    method: "post",
    data: data,
  });
};

export const getScoreReviewResult = (student_sno: any) => {
  return request({
    url: "/scores/get_score_review_result",
    method: "get",
    params: { student_sno },
  });
};

export const getCollegeScores = (data) => {
  return request({
    method: "get",
    url: "/scores/get_college_scores",
    params: data,
  });
};
