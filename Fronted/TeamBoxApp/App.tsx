import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import UserList from "./UserList";
import UserForm from "./UserForm";
import ClassForm from "./ClassForm";
import CommentForm from "./CommentForm";

export type RootStackParamList = {
  UserList: undefined;
  UserForm: undefined;
  ClassForm: undefined;
  CommentForm: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="UserList">
        <Stack.Screen
          name="UserList"
          component={UserList}
          options={{ title: "Lista de Usuarios" }}
        />
        <Stack.Screen
          name="UserForm"
          component={UserForm}
          options={{ title: "Crear Usuario" }}
        />
        <Stack.Screen
          name="ClassForm"
          component={ClassForm}
          options={{ title: "Crear Clase" }}
        />
        <Stack.Screen
          name="CommentForm"
          component={CommentForm}
          options={{ title: "Crear Comentario" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
