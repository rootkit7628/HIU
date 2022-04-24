import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";

// layouts

import Admin from "layouts/Admin.js";
import "./i18n.js";
// views without layouts

import Index from "views/Index.js";
import Erreur from "views/Erreur.js";
import Auth from "views/auth/Auth.js"; 

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      {/* add routes with layouts */}
      <Route path="/admin" component={Admin} />
      {/* add routes without layouts */}
      <Route path="/" exact component={Index} />
      <Route path="/authentification" exact component={Auth} />
      {/**Page d'erreur */}
      <Route path="/error" exact component={Erreur} />
      {/* add redirect for first page */}
      <Redirect from="*" to="/error" />
    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
);
