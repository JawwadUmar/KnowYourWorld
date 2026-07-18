import dotenv from "dotenv";
import express from "express";
import axios from "axios";
import { GoogleGenAI } from "@google/genai";

dotenv.config();

const app = express();

const ai = new GoogleGenAI({
  apiKey: process.env.GOOGLE_API_KEY,
});

const PYTHON_API = "http://127.0.0.1:8000/extract";

const PROMPT_TEMPLATE = `
Generate 5 challenging UPSC questions based on the study material provided.

Requirements:
- Questions should test conceptual understanding.
- Number the questions.
- After all questions, provide detailed solutions.
- Return the response in clean Markdown.
- Use headings, bullet points, and code blocks only if necessary.
`;

app.get("/", async (req, res) => {
  try {
    const { data: studyMaterial } = await axios.get(PYTHON_API);

    const prompt = `${studyMaterial}\n\n${PROMPT_TEMPLATE}`;

    const response = await generateContent(prompt);

    res.send(response);
  } catch (error) {
    console.error("Error:", error.message);

    res.status(500).json({
      success: false,
      message: "Failed to generate questions.",
    });
  }
});

async function generateContent(prompt) {
  const response = await ai.models.generateContent({
    model: "gemini-3.5-flash",
    contents: prompt,
  });

  return response.text;
}

export default app;