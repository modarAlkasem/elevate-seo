export type SignUpPayload = {
  email: string;
  password: string;
};

export type SignUpResponse = APIUser;

export type SignInPayload = SignUpPayload;

export type SignInResponse = {
  user: APIUser;
  tokens: {
    access: string;
    refresh: string;
  };
};

export type SignInSocialPayload = {
  email: string;
  id_token: string;
  access_token: string;
  provider: "GOOGLE";
};

export type SignInSocialResponse = SignInResponse;

export type RefreshTokenPayload = {
  refresh: string;
};

export type RefreshTokenResponse = {
  refresh: string;
  access: string;
};

export type SignOutPayload = {
  refresh: string;
};
