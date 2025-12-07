import { SignIn } from "@clerk/nextjs";

const SignInPage = () => {
  return (
    <div className="min-h-screen flex justify-center items-center">
      <p>
        Please use <br /> Email address: trendy.testing.7@gmail.com and <br />{" "}
        password: Testingme123
      </p>
      <SignIn />
    </div>
  );
};

export default SignInPage;
