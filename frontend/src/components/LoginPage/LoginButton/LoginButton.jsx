import React, { useEffect, useState } from "react";
import { PublicClientApplication } from "@azure/msal-browser";
import './LoginButton.modules.css'

const msalConfig = {
  auth: {
    clientId: "YOUR_AZURE_APP_CLIENT_ID", // Replace with your Azure App Client ID
    authority: "https://login.microsoftonline.com/common", // Multi-tenant
    redirectUri: window.location.origin,
  },
};

const msalInstance = new PublicClientApplication(msalConfig);

const LoginButton = () => {
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const initializeMsal = async () => {
      await msalInstance.initialize();
      setIsInitialized(true);
    };
    initializeMsal();
  }, []);

  const handleLogin = async () => {
    if (!isInitialized) {
      console.error("MSAL is not initialized yet");
      return;
    }

    try {
      const loginResponse = await msalInstance.loginPopup({
        scopes: ["user.read"],
      });
      console.log("Login Success:", loginResponse);
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <>
      <button
        onClick={handleLogin}
        disabled={!isInitialized}
        className="sign-in-btn"
      >
        {isInitialized ? "Sign in with Microsoft" : "Initializing..."}
      </button>
    </>
  );
};

export default LoginButton;
