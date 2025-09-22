import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { api } from "./client";

export default function ClassForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dateTime, setDateTime] = useState("");
  const [maxStudents, setMaxStudents] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await api.post("/create_classes", {
        title,
        description,
        date_time: dateTime,
        max_students: Number(maxStudents),
      });
      Alert.alert("Clase creada", `ID: ${res.data.id}`);
      setTitle(""); setDescription(""); setDateTime(""); setMaxStudents("");
    } catch (err: any) {
      Alert.alert("Error", err.response?.data?.detail || err.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Crear Clase</Text>
      <TextInput placeholder="Título" value={title} onChangeText={setTitle} style={styles.input} />
      <TextInput placeholder="Descripción" value={description} onChangeText={setDescription} style={styles.input} />
      <TextInput placeholder="Fecha y hora (YYYY-MM-DD HH:MM)" value={dateTime} onChangeText={setDateTime} style={styles.input} />
      <TextInput placeholder="Máx. estudiantes" value={maxStudents} onChangeText={setMaxStudents} style={styles.input} keyboardType="numeric"/>
      <Button title="Crear Clase" onPress={handleSubmit} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 20, fontWeight: "700", marginBottom: 12 },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 8, marginBottom: 12, borderRadius: 4 },
});
