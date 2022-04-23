import React from "react";
import { Switch, Redirect } from "react-router-dom";


// views
import Statistiques from "views/admin/Statistiques.js";
import Settings from "views/admin/Settings.js";
import Liste from "views/admin/Liste.js";
import Kanban from "views/admin/Kanban.js";
import Add from "views/admin/Add";
import AdminRoute from "private/AdminRoute";

// private

export default function Admin() {
  return (
    <>
          <Switch> 
            <AdminRoute path="/admin/statistique" exact>
                <Statistiques />
            </AdminRoute>
            <AdminRoute path="/admin/settings" exact>
                <Settings />
            </AdminRoute>
            <AdminRoute path="/admin/liste" exact>
                <Liste />
            </AdminRoute>
            <AdminRoute path="/admin/kanban" exact c>
                <Kanban />
            </AdminRoute>
            <AdminRoute path="/admin/add" exact >
                <Add />
            </AdminRoute>
            <Redirect from="/admin" to="/erreur" />
          </Switch>
    </>
  );
}
