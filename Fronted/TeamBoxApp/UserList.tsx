import React, { useEffect, useState } from "react";
import { View, Text, FlatList, Button, StyleSheet } from "react-native";
import { api } from "./client";
import { User } from "./user";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "./App";

type UserListNavigationProp = NativeStackNavigationProp<RootStackParamList, "UserList">;

type Props = {
  navigation: UserListNavigationProp;
};

export default function UserList({ navigation }: Props) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get<User[]>("/users");
        setUsers(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <View style={styles.container}>
      <Button title="Crear Usuario" onPress={() => navigation.navigate("UserForm")} />
      <Button title="Crear Clase" onPress={() => navigation.navigate("ClassForm")} />
      <Button title="Crear Comentario" onPress={() => navigation.navigate("CommentForm")} />

      <Text style={styles.title}>Usuarios</Text>
      {loading ? (
        <Text>Cargando...</Text>
      ) : (
        <FlatList
          data={users}
          keyExtractor={(i) => i.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text>{item.name}</Text>
              <Text>{item.email}</Text>
              <Text>Puntos: {item.points}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: "#eee" },
  title: { fontSize: 20, fontWeight: "700", marginVertical: 12 },
  card: { padding: 8, borderBottomWidth: 1, borderColor: "#ccc" },
});
