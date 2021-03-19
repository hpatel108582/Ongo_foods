import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { GoogleLogin } from 'react-google-login';
import { Socket } from './Socket';
import './loginstyle.css';
import { Cal_comp } from './CalenderComp.jsx';
import { HomePage } from './LogedInHome';

export default function Login() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [ccode, setCcode] = useState([-1]);

  function loginUser(response) {
    const name = response.getBasicProfile().getName();
    const email = response.getBasicProfile().getEmail();
    const idToken = response.getAuthResponse().id_token;
    Socket.emit('new google user', {
      name: name,
      email: email,
      idtoken: idToken
    });
  }

  function loginUserFail() {
    return false;
  }

  function verifiedSession() {
    React.useEffect(() => {
      Socket.on('Verified', (data) => {
        setLoggedIn(true);
        setUsername(data.name);
        setCcode(data.ccodes);
      });
    }, []);
  }

  verifiedSession();

  if (loggedIn && ccode[0] != -1) {
    return (
      <div className="outermost">
        <h1 className="header">OnGo Foods</h1>
      </div>
    );
  }
  return (
    <div className="outermost">
      <h1 className="header">Calglomerate</h1>
      <div className="container">
        <GoogleLogin
          clientId="485584606209-5go07kokk5om8brvuia3odge09ie8dfr.apps.googleusercontent.com"
          buttonText="Login"
          onSuccess={loginUser}
          onFailure={loginUserFail}
          cookiePolicy="single_host_origin"
        />
      </div>
    </div>
  );
}
