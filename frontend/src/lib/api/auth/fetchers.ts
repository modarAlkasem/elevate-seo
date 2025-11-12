import api from "@/lib/axios";
import {
  SignUpPayload,
  SignInPayload,
  SignInResponse,
  SignUpResponse,
  SignInSocialPayload,
  SignInSocialResponse,
  SignOutPayload,
  RefreshTokenPayload,
  RefreshTokenResponse,
} from "./types";

export const signUp = async ({
  email,
  password,
}: SignUpPayload): Promise<SignUpResponse> => {
  const response = (await api.post<APIResponse<SignUpResponse>>(
    "/auth/signup/",
    {
      email,
      password,
    }
  )) as unknown as APIResponse;

  return response.data;
};

export const signIn = async ({
  email,
  password,
}: SignInPayload): Promise<SignInResponse> => {
  const response = (await api.post<APIResponse<SignInResponse>>(
    "/auth/signin/",
    {
      email,
      password,
    }
  )) as unknown as APIResponse;

  return response.data;
};

export const signInSocial = async ({
  email,
  id_token,
  access_token,
  provider,
}: SignInSocialPayload): Promise<SignInResponse> => {
  const response = (await api.post<APIResponse<SignInResponse>>(
    "/auth/social/signin/",
    {
      email,
      id_token,
      access_token,
      provider,
    }
  )) as unknown as APIResponse;

  return response.data;
};

export const signOut = async ({ refresh }: SignOutPayload): Promise<void> => {
  const response = (await api.post<APIResponse<null>>("/auth/signout/", {
    refresh,
  })) as unknown as APIResponse;

  return response.data;
};

export const refreshToken = async ({
  refresh,
}: RefreshTokenPayload): Promise<RefreshTokenResponse> => {
  const response = (await api.post<APIResponse<RefreshTokenResponse>>(
    "auth/token/refresh/",
    {
      refresh,
    }
  )) as unknown as APIResponse;

  return response.data;
};
