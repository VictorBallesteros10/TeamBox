import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { api } from "./client";

export default function CommentForm() {
  const [userId, setUserId] = useState("");
  const [classId, setClassId] = useState("");
  const [content, setContent] = useState("");
  const [rating, setRating] = useState("");

  const handleSubmit = async () => {
    try {
      const payload: any = {
        user_id: Number(userId),
        class_id: Number(classId),
      };
      if (content.trim() !== "") payload.content = content;
      if (rating.trim() !== "") payload.rating = Number(rating);

      const res = await api.post("/comments", payload);
      Alert.alert("Comentario creado", `ID: ${res.data.id}`);
      setUserId(""); setClassId(""); setContent(""); setRating("");
    } catch (err: any) {
      Alert.alert("Error", err.response?.data?.detail || err.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Crear Comentario</Text>
      <TextInput placeholder="ID Usuario" value={userId} onChangeText={setUserId} style={styles.input} keyboardType="numeric" />
      <TextInput placeholder="ID Clase" value={classId} onChangeText={setClassId} style={styles.input} keyboardType="numeric" />
      <TextInput placeholder="Comentario (opcional)" value={content} onChangeText={setContent} style={styles.input} />
      <TextInput placeholder="Rating (opcional)" value={rating} onChangeText={setRating} style={styles.input} keyboardType="numeric" />
      <Button title="Crear Comentario" onPress={handleSubmit} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 20, fontWeight: "700", marginBottom: 12 },
  input: { borderWidth: 1, borderColor: "#ccc", padding: 8, marginBottom: 12, borderRadius: 4 },
});
